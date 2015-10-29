#!/usr/bin/env python3
'''
Created on 29.10.2015

@author: moritz
'''

import logging


class Field(object):
    def __init__(self, column, row, bomb=False):
        self.column = column
        self.row = row
        self.bomb = bomb

    def __str__(self):
        return 'C:{} R:{} B:{}'.format(self.column, self.row, self.bomb)


def column_generator(rows):
    pass


def matrix_generator(columns=2, rows=2, bombs=1):
    matrix = []
    for c in range(columns):
        matrix.append([])
        for r in range(rows):
            matrix[c].append(Field(c, r))
    return matrix


if __name__ == '__main__':
    logging.info("Run tests")
    matrix = matrix_generator()
    for c in range(len(matrix)):
        for r in range(len(matrix[c])):
            print(matrix[c][r])
