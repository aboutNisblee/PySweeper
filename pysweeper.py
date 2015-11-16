#!/usr/bin/env python3
# coding=utf-8
"""
Created on 14.11.2015

:author: Moritz Nisblé (mNisblee) <moritz.nisble@gmx.de>
"""

import argparse
from gui import mainwindow


def main():
    parser = argparse.ArgumentParser(description='A Python implementation of the famous logic game mine sweeper')
    parser.add_argument('-c', '--columns', help='Column count of the game matrix', type=int, default=12)
    parser.add_argument('-r', '--rows', help='Row count of the game matrix', type=int, default=10)
    parser.add_argument('-b', '--bombs', help='Bomb count', type=int, default=10)

    args = parser.parse_args()

    # TODO: Reduce file count; Add a controller.
    mainwindow.run(args.columns, args.rows, args.bombs)


if __name__ == '__main__':
    main()
