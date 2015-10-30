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
    def __init__(self, columns=2, rows=2, bombs=1):
        self.matrix = self._matrix_generator(columns, rows)

    def _matrix_generator(self, columns=2, rows=2):
        return [self._column_generator(c, rows) for c in range(columns)]

    def _column_generator(self, column, rows):
        return [Field(column, r) for r in range(rows)]

    def __str__(self):
        return self._str(lambda c, r: str(self.matrix[c][r]))

    def str_matrix(self):
        '''
        Get a nicely formatted representation of the matrix as string.
        This is mainly used for debugging or logging purposes.
        :return: A string.
        '''
        return self._str(lambda c, r: self.matrix[c][r].print_mark())

    def _str(self, getter):
        '''
        Get a string representation of the current matrix. Call the passed
        callable for each field to insert the needed information.
        The matrix is displayed row-wise despite the internal representation
        is column-wise.
        :param getter: A callable that takes the column and row indices
        and returns a string.
        :return: A string.
        '''
        string = ''  # Difference to usage of a list is not measurable
        for r in range(len(self.matrix[0])):
            for c in range(len(self.matrix)):
                string += getter(c, r)
                string += ' '
            string += '\n'
        return string


if __name__ == '__main__':
    logging.info("Run tests")
    matrix = Matrix(15, 10)
#     print('__str__:\n{}'.format(matrix))
    print('str_matrix:\n{}'.format(matrix.str_matrix()))
