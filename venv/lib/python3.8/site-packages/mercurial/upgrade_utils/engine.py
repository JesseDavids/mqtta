# upgrade.py - functions for in place upgrade of Mercurial repository
#
# Copyright (c) 2016-present, Gregory Szorc
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from __future__ import absolute_import

import stat

from ..i18n import _
from ..pycompat import getattr
from .. import (
    changelog,
    error,
    filelog,
    manifest,
    metadata,
    pycompat,
    requirements,
    revlog,
    scmutil,
    util,
    vfs as vfsmod,
)


def _revlogfrompath(repo, path):
    """Obtain a revlog from a repo path.

    An instance of the appropriate class is returned.
    """
    if path == b'00changelog.i':
        return changelog.changelog(repo.svfs)
    elif path.endswith(b'00manifest.i'):
        mandir = path[: -len(b'00manifest.i')]
        return manifest.manifestrevlog(repo.svfs, tree=mandir)
    else:
        # reverse of "/".join(("data", path + ".i"))
        return filelog.filelog(repo.svfs, path[5:-2])


def _copyrevlog(tr, destrepo, oldrl, unencodedname):
    """copy all relevant files for `oldrl` into `destrepo` store

    Files are copied "as is" without any transformation. The copy is performed
    without extra checks. Callers are responsible for making sure the copied
    content is compatible with format of the destination repository.
    """
    oldrl = getattr(oldrl, '_revlog', oldrl)
    newrl = _revlogfrompath(destrepo, unencodedname)
    newrl = getattr(newrl, '_revlog', newrl)

    oldvfs = oldrl.opener
    newvfs = newrl.opener
    oldindex = oldvfs.join(oldrl.indexfile)
    newindex = newvfs.join(newrl.indexfile)
    olddata = oldvfs.join(oldrl.datafile)
    newdata = newvfs.join(newrl.datafile)

    with newvfs(newrl.indexfile, b'w'):
        pass  # create all the directories

    util.copyfile(oldindex, newindex)
    copydata = oldrl.opener.exists(oldrl.datafile)
    if copydata:
        util.copyfile(olddata, newdata)

    if not (
        unencodedname.endswith(b'00changelog.i')
        or unencodedname.endswith(b'00manifest.i')
    ):
        destrepo.svfs.fncache.add(unencodedname)
        if copydata:
            destrepo.svfs.fncache.add(unencodedname[:-2] + b'.d')


UPGRADE_CHANGELOG = b"changelog"
UPGRADE_MANIFEST = b"manifest"
UPGRADE_FILELOGS = b"all-filelogs"

UPGRADE_ALL_REVLOGS = frozenset(
    [UPGRADE_CHANGELOG, UPGRADE_MANIFEST, UPGRADE_FILELOGS]
)


def getsidedatacompanion(srcrepo, dstrepo):
    sidedatacompanion = None
    removedreqs = srcrepo.requirements - dstrepo.requirements
    addedreqs = dstrepo.requirements - srcrepo.requirements
    if requirements.SIDEDATA_REQUIREMENT in removedreqs:

        def sidedatacompanion(rl, rev):
            rl = getattr(rl, '_revlog', rl)
            if rl.flags(rev) & revlog.REVIDX_SIDEDATA:
                return True, (), {}, 0, 0
            return False, (), {}, 0, 0

    elif requirements.COPIESSDC_REQUIREMENT in addedreqs:
        sidedatacompanion = metadata.getsidedataadder(srcrepo, dstrepo)
    elif requirements.COPIESSDC_REQUIREMENT in removedreqs:
        sidedatacompanion = metadata.getsidedataremover(srcrepo, dstrepo)
    return sidedatacompanion


def matchrevlog(revlogfilter, entry):
    """check if a revlog is selected for cloning.

    In other words, are there any updates which need to be done on revlog
    or it can be blindly copied.

    The store entry is checked against the passed filter"""
    if entry.endswith(b'00changelog.i'):
        return UPGRADE_CHANGELOG in revlogfilter
    elif entry.endswith(b'00manifest.i'):
        return UPGRADE_MANIFEST in revlogfilter
    return UPGRADE_FILELOGS in revlogfilter


def _perform_clone(
    ui,
    dstrepo,
    tr,
    old_revlog,
    unencoded,
    upgrade_op,
    sidedatacompanion,
    oncopiedrevision,
):
    """ returns the new revlog object created"""
    newrl = None
    if matchrevlog(upgrade_op.revlogs_to_process, unencoded):
        ui.note(
            _(b'cloning %d revisions from %s\n') % (len(old_revlog), unencoded)
        )
        newrl = _revlogfrompath(dstrepo, unencoded)
        old_revlog.clone(
            tr,
            newrl,
            addrevisioncb=oncopiedrevision,
            deltareuse=upgrade_op.delta_reuse_mode,
            forcedeltabothparents=upgrade_op.force_re_delta_both_parents,
            sidedatacompanion=sidedatacompanion,
        )
    else:
        msg = _(b'blindly copying %s containing %i revisions\n')
        ui.note(msg % (unencoded, len(old_revlog)))
        _copyrevlog(tr, dstrepo, old_revlog, unencoded)

        newrl = _revlogfrompath(dstrepo, unencoded)
    return newrl


def _clonerevlogs(
    ui,
    srcrepo,
    dstrepo,
    tr,
    upgrade_op,
):
    """Copy revlogs between 2 repos."""
    revcount = 0
    srcsize = 0
    srcrawsize = 0
    dstsize = 0
    fcount = 0
    frevcount = 0
    fsrcsize = 0
    frawsize = 0
    fdstsize = 0
    mcount = 0
    mrevcount = 0
    msrcsize = 0
    mrawsize = 0
    mdstsize = 0
    crevcount = 0
    csrcsize = 0
    crawsize = 0
    cdstsize = 0

    alldatafiles = list(srcrepo.store.walk())
    # mapping of data files which needs to be cloned
    # key is unencoded filename
    # value is revlog_object_from_srcrepo
    manifests = {}
    changelogs = {}
    filelogs = {}

    # Perform a pass to collect metadata. This validates we can open all
    # source files and allows a unified progress bar to be displayed.
    for unencoded, encoded, size in alldatafiles:
        if not unencoded.endswith(b'.i'):
            continue

        rl = _revlogfrompath(srcrepo, unencoded)

        info = rl.storageinfo(
            exclusivefiles=True,
            revisionscount=True,
            trackedsize=True,
            storedsize=True,
        )

        revcount += info[b'revisionscount'] or 0
        datasize = info[b'storedsize'] or 0
        rawsize = info[b'trackedsize'] or 0

        srcsize += datasize
        srcrawsize += rawsize

        # This is for the separate progress bars.
        if isinstance(rl, changelog.changelog):
            changelogs[unencoded] = rl
            crevcount += len(rl)
            csrcsize += datasize
            crawsize += rawsize
        elif isinstance(rl, manifest.manifestrevlog):
            manifests[unencoded] = rl
            mcount += 1
            mrevcount += len(rl)
            msrcsize += datasize
            mrawsize += rawsize
        elif isinstance(rl, filelog.filelog):
            filelogs[unencoded] = rl
            fcount += 1
            frevcount += len(rl)
            fsrcsize += datasize
            frawsize += rawsize
        else:
            error.ProgrammingError(b'unknown revlog type')

    if not revcount:
        return

    ui.status(
        _(
            b'migrating %d total revisions (%d in filelogs, %d in manifests, '
            b'%d in changelog)\n'
        )
        % (revcount, frevcount, mrevcount, crevcount)
    )
    ui.status(
        _(b'migrating %s in store; %s tracked data\n')
        % ((util.bytecount(srcsize), util.bytecount(srcrawsize)))
    )

    # Used to keep track of progress.
    progress = None

    def oncopiedrevision(rl, rev, node):
        progress.increment()

    sidedatacompanion = getsidedatacompanion(srcrepo, dstrepo)

    # Migrating filelogs
    ui.status(
        _(
            b'migrating %d filelogs containing %d revisions '
            b'(%s in store; %s tracked data)\n'
        )
        % (
            fcount,
            frevcount,
            util.bytecount(fsrcsize),
            util.bytecount(frawsize),
        )
    )
    progress = srcrepo.ui.makeprogress(_(b'file revisions'), total=frevcount)
    for unencoded, oldrl in sorted(filelogs.items()):
        newrl = _perform_clone(
            ui,
            dstrepo,
            tr,
            oldrl,
            unencoded,
            upgrade_op,
            sidedatacompanion,
            oncopiedrevision,
        )
        info = newrl.storageinfo(storedsize=True)
        fdstsize += info[b'storedsize'] or 0
    ui.status(
        _(
            b'finished migrating %d filelog revisions across %d '
            b'filelogs; change in size: %s\n'
        )
        % (frevcount, fcount, util.bytecount(fdstsize - fsrcsize))
    )

    # Migrating manifests
    ui.status(
        _(
            b'migrating %d manifests containing %d revisions '
            b'(%s in store; %s tracked data)\n'
        )
        % (
            mcount,
            mrevcount,
            util.bytecount(msrcsize),
            util.bytecount(mrawsize),
        )
    )
    if progress:
        progress.complete()
    progress = srcrepo.ui.makeprogress(
        _(b'manifest revisions'), total=mrevcount
    )
    for unencoded, oldrl in sorted(manifests.items()):
        newrl = _perform_clone(
            ui,
            dstrepo,
            tr,
            oldrl,
            unencoded,
            upgrade_op,
            sidedatacompanion,
            oncopiedrevision,
        )
        info = newrl.storageinfo(storedsize=True)
        mdstsize += info[b'storedsize'] or 0
    ui.status(
        _(
            b'finished migrating %d manifest revisions across %d '
            b'manifests; change in size: %s\n'
        )
        % (mrevcount, mcount, util.bytecount(mdstsize - msrcsize))
    )

    # Migrating changelog
    ui.status(
        _(
            b'migrating changelog containing %d revisions '
            b'(%s in store; %s tracked data)\n'
        )
        % (
            crevcount,
            util.bytecount(csrcsize),
            util.bytecount(crawsize),
        )
    )
    if progress:
        progress.complete()
    progress = srcrepo.ui.makeprogress(
        _(b'changelog revisions'), total=crevcount
    )
    for unencoded, oldrl in sorted(changelogs.items()):
        newrl = _perform_clone(
            ui,
            dstrepo,
            tr,
            oldrl,
            unencoded,
            upgrade_op,
            sidedatacompanion,
            oncopiedrevision,
        )
        info = newrl.storageinfo(storedsize=True)
        cdstsize += info[b'storedsize'] or 0
    progress.complete()
    ui.status(
        _(
            b'finished migrating %d changelog revisions; change in size: '
            b'%s\n'
        )
        % (crevcount, util.bytecount(cdstsize - csrcsize))
    )

    dstsize = fdstsize + mdstsize + cdstsize
    ui.status(
        _(
            b'finished migrating %d total revisions; total change in store '
            b'size: %s\n'
        )
        % (revcount, util.bytecount(dstsize - srcsize))
    )


def _files_to_copy_post_revlog_clone(srcrepo):
    """yields files which should be copied to destination after revlogs
    are cloned"""
    for path, kind, st in sorted(srcrepo.store.vfs.readdir(b'', stat=True)):
        # don't copy revlogs as they are already cloned
        if path.endswith((b'.i', b'.d', b'.n', b'.nd')):
            continue
        # Skip transaction related files.
        if path.startswith(b'undo'):
            continue
        # Only copy regular files.
        if kind != stat.S_IFREG:
            continue
        # Skip other skipped files.
        if path in (b'lock', b'fncache'):
            continue
        # TODO: should we skip cache too?

        yield path


def _replacestores(currentrepo, upgradedrepo, backupvfs, upgrade_op):
    """Replace the stores after current repository is upgraded

    Creates a backup of current repository store at backup path
    Replaces upgraded store files in current repo from upgraded one

    Arguments:
      currentrepo: repo object of current repository
      upgradedrepo: repo object of the upgraded data
      backupvfs: vfs object for the backup path
      upgrade_op: upgrade operation object
                  to be used to decide what all is upgraded
    """
    # TODO: don't blindly rename everything in store
    # There can be upgrades where store is not touched at all
    util.rename(currentrepo.spath, backupvfs.join(b'store'))
    util.rename(upgradedrepo.spath, currentrepo.spath)


def finishdatamigration(ui, srcrepo, dstrepo, requirements):
    """Hook point for extensions to perform additional actions during upgrade.

    This function is called after revlogs and store files have been copied but
    before the new store is swapped into the original location.
    """


def upgrade(ui, srcrepo, dstrepo, upgrade_op):
    """Do the low-level work of upgrading a repository.

    The upgrade is effectively performed as a copy between a source
    repository and a temporary destination repository.

    The source repository is unmodified for as long as possible so the
    upgrade can abort at any time without causing loss of service for
    readers and without corrupting the source repository.
    """
    assert srcrepo.currentwlock()
    assert dstrepo.currentwlock()

    ui.status(
        _(
            b'(it is safe to interrupt this process any time before '
            b'data migration completes)\n'
        )
    )

    with dstrepo.transaction(b'upgrade') as tr:
        _clonerevlogs(
            ui,
            srcrepo,
            dstrepo,
            tr,
            upgrade_op,
        )

    # Now copy other files in the store directory.
    for p in _files_to_copy_post_revlog_clone(srcrepo):
        srcrepo.ui.status(_(b'copying %s\n') % p)
        src = srcrepo.store.rawvfs.join(p)
        dst = dstrepo.store.rawvfs.join(p)
        util.copyfile(src, dst, copystat=True)

    finishdatamigration(ui, srcrepo, dstrepo, requirements)

    ui.status(_(b'data fully upgraded in a temporary repository\n'))

    backuppath = pycompat.mkdtemp(prefix=b'upgradebackup.', dir=srcrepo.path)
    backupvfs = vfsmod.vfs(backuppath)

    # Make a backup of requires file first, as it is the first to be modified.
    util.copyfile(srcrepo.vfs.join(b'requires'), backupvfs.join(b'requires'))

    # We install an arbitrary requirement that clients must not support
    # as a mechanism to lock out new clients during the data swap. This is
    # better than allowing a client to continue while the repository is in
    # an inconsistent state.
    ui.status(
        _(
            b'marking source repository as being upgraded; clients will be '
            b'unable to read from repository\n'
        )
    )
    scmutil.writereporequirements(
        srcrepo, srcrepo.requirements | {b'upgradeinprogress'}
    )

    ui.status(_(b'starting in-place swap of repository data\n'))
    ui.status(_(b'replaced files will be backed up at %s\n') % backuppath)

    # Now swap in the new store directory. Doing it as a rename should make
    # the operation nearly instantaneous and atomic (at least in well-behaved
    # environments).
    ui.status(_(b'replacing store...\n'))
    tstart = util.timer()
    _replacestores(srcrepo, dstrepo, backupvfs, upgrade_op)
    elapsed = util.timer() - tstart
    ui.status(
        _(
            b'store replacement complete; repository was inconsistent for '
            b'%0.1fs\n'
        )
        % elapsed
    )

    # We first write the requirements file. Any new requirements will lock
    # out legacy clients.
    ui.status(
        _(
            b'finalizing requirements file and making repository readable '
            b'again\n'
        )
    )
    scmutil.writereporequirements(srcrepo, upgrade_op.new_requirements)

    # The lock file from the old store won't be removed because nothing has a
    # reference to its new location. So clean it up manually. Alternatively, we
    # could update srcrepo.svfs and other variables to point to the new
    # location. This is simpler.
    backupvfs.unlink(b'store/lock')

    return backuppath
