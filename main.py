#!/usr/bin/env python3
#this is a main file which will initialise and execute the run method from the core file

#importing our application file
from core import MyApp
import os, sys
from tendo import singleton

if __name__ == "__main__":
    me = singleton.SingleInstance()

    app = MyApp()
    app.run()