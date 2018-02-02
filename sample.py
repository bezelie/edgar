#!/usr/bin/python
import sys
from time import sleep

if __name__ == '__main__':
    while True:
        print "Hello world %s" % (sys.argv)
        sys.stdout.flush()
        sleep(1)
