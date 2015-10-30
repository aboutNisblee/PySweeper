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

    def print_mark(self):
        return 'X' if self.bomb else '0'

    def __str__(self):
        return 'C:{} R:{} B:{}'.format(self.column, self.row, self.bomb)


class Matrix(object):
    def _column_generator(self, column, rows):
        return [Field(column, r) for r in range(rows)]

    def _matrix_generator(self, columns=2, rows=2):
        return [self._column_generator(c, rows) for c in range(columns)]

    def __init__(self, columns=2, rows=2, bombs=1):
        self.matrix = self._matrix_generator(columns, rows)

    def _str(self, getter):
        string = ''
        for r in range(len(self.matrix[0])):
            for c in range(len(self.matrix)):
                string += getter(c, r)
                string += ' '
            string += '\n'
        return string

    def str_matrix(self):
        return self._str(lambda c, r: self.matrix[c][r].print_mark())

    def __str__(self):
        return self._str(lambda c, r: str(self.matrix[c][r]))


if __name__ == '__main__':
    logging.info("Run tests")
    matrix = Matrix(10, 10)
    print('__str__:\n{}'.format(matrix))
    print('str_matrix:\n{}'.format(matrix.str_matrix()))
