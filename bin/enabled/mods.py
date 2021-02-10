#!/usr/bin/env python3

import os

path = ""

plugin_path = "/home/jaydavids/Downloads/mqtta/bin/enabled"
plugin_file = os.listdir(plugin_path)
plugin_list = []

for f in plugin_file:
    if f.endswith(".plugin"):
        plugin_list.append(f)
        #fopen = open(f, mode = 'r+')

#print(plugin_list)

for name in plugin_list:
    if __name__ == '__main__':
        file_to_process = name
        string_to_find = input("#!/usr/bin/env python3")
        word_find(file_to_process, string_to_find)

    def word_find(file, word):
        with open(file, 'r') as target_file:
            for num, line in enumerate(target_file.readlines(), 1):
                if str(word) in line:
                    print("{}".format(num) + " " + "{}".format(line))
                else:
                    print("{} not found.".format(word) + " in" + "{}".format(num))
                    print(name)
quit()
exit()