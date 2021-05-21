#!/usr/bin/env python

# NAME: Sample 0: pure python module
# DESCRIPTION: Create a tag in the shared database, and increment its value each second forever, manually written in python

import time
from drbox import sdb


def main():
    # create a client connection
    c = sdb.Client('python sample')
    c.connect()

    # create a tag
    tag = c.add_tag('some_int', sdb.DT_INT)
    print('tag "{}" created'.format(tag))

    value = 0

    while True:
        # write a new tag value then read it again
        value += 1
        tag.write(value)
        print('tag "{}" written with value {}'.format(tag, value))

        time.sleep(1)


if __name__ == '__main__':
    main()
