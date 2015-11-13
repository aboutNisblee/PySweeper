#!/usr/bin/env python3
# coding=utf-8
"""
Created on 29.10.2015

:author: Moritz Nisblé (mNisblee) <moritz.nisble@gmx.de>
"""

import logging
from random import randint


class Neighbours(object):
    pass


class Field(object):
    """
    A single field in the matrix.
    """

    def __init__(self, column, row, matrix):
        """
        Initialize a new Field.
        :param column: The column index.
        :param row: The row index.
        """
        if column < 0 or row < 0:
            raise ValueError('Column/row index cannot be negative')
        if not isinstance(matrix, Matrix):
            raise TypeError('Should pass a Matrix object')

        self._matrix = matrix
        self._column = column
        self._row = row
        self._bomb = False
        self.adjacent_bombs = 0

        self.neighbours = []

        # Determine indices of adjacent fields.
        self.n_idx = (
            # Upper row
            (self.column - 1, self.row - 1),
            (self.column, self.row - 1),
            (self.column + 1, self.row - 1),
            # Middle row
            (self.column - 1, self.row),
            (self.column + 1, self.row),
            # Lower row
            (self.column - 1, self.row + 1),
            (self.column, self.row + 1),
            (self.column + 1, self.row + 1),
        )

    @property
    def column(self):
        return self._column

    @property
    def row(self):
        return self._row

    def reg_neighbour(self, field):
        """
        Register another Field a a neighbour of this one.
        :param field: A neighbour.
        """
        self.neighbours.append(field)

    def link(self):
        for c, r in self.n_idx:
            if c < 0 or r < 0 or c >= self._matrix.columns() or r >= self._matrix.rows():
                continue
            else:
                self._matrix[c][r].reg_neighbour(self)

    @property
    def bomb(self):
        """ Is it a bomb? """
        return self._bomb

    def set_bomb(self, value=True):
        """
        Mark/unmark this field as bomb.
        :param value: The new value.
        :return: True when flag was changed, else False.
        """
        if not isinstance(value, bool):
            raise TypeError('Bomb flag should be of type bool')
        if self._bomb == value:
            return False
        self._bomb = value
        # TODO: Inform neighbours.
        for f in self.neighbours:
            f.adjacent_bombs += 1
        return True

    def console_symbol(self):
        return 'X' if self.bomb else str(self.adjacent_bombs)

    def __str__(self):
        return 'C:{} R:{} S:{}'.format(self.column, self.row, self.console_symbol())


class Matrix(object):
    """
    :todo: Pay attention to deep copies!
    """

    def __init__(self, columns=2, rows=2, bombs=1):
        self._bombs = bombs

        self._matrix = [[Field(c, r, self) for r in range(rows)] for c in range(columns)]

        for field in self._col_wise():
            field.link()

        b = 0
        while b < bombs:
            c = randint(0, columns - 1)
            r = randint(0, rows - 1)
            if self._matrix[c][r].set_bomb(True):
                b += 1

    def columns(self):
        return len(self._matrix)

    def rows(self):
        return len(self._matrix[0])

    @property
    def bombs(self):
        return self._bombs

    @property
    def matrix(self):
        return self._matrix

    def _col_wise(self, yield_col=False):
        """
        Column-wise field generator.
        :param yield_col: If true yielding after a complete row.
         """
        for c in range(self.columns()):
            for r in range(self.rows()):
                yield (self._matrix[c][r])
            if yield_col:
                yield False

    def _row_wise(self, yield_row=False):
        """
        Row-wise field generator.
        :param yield_row: If true yielding after a complete row.
        """
        for r in range(self.rows()):
            for c in range(self.columns()):
                yield (self._matrix[c][r])
            if yield_row:
                yield False  # TODO Whats the best type for None?? None? :D

    def __len__(self):
        """ Get the count of fields. """
        return len(self._matrix) * len(self._matrix[0])

    def __str__(self):
        string = 'Columns {} Rows: {} Bombs: {}\n'.format(self.columns(), self.rows(), self.bombs)
        for field in self._col_wise():
            string += str(field) + '\n'
        return string

    def console_matrix(self):
        """
        Get a nicely formatted representation of the matrix as string.
        This is mainly used for debugging or logging purposes.
        The matrix is displayed row-wise despite the internal representation
        is column-wise.
        :return: A string.
        """
        string = ''  # Difference to usage of a list is not measurable
        for field in self._row_wise(True):
            if not field:
                string += '\n'
            else:
                string += field.console_symbol()
                string += ' '
        return string

    def __getitem__(self, idx):
        try:
            # Is the passes index an sequence?
            # This makes calls as matrix[1, 1] possible.
            # IndexError is possibly raised but not caught. OK?
            c_idx, r_idx = idx
            return self._matrix[c_idx][r_idx]
        except (TypeError, ValueError):
            # If we get a TypeError only the column index was passed.
            # This makes calls like matrix[1][1] possible.
            # If a str is passed also handle it here. Error message is more
            # meaningful when trying to use a str as index.
            # 'TypeError: list indices must be integers, not str'
            # instead of
            # 'ValueError: need more than 1 value to unpack'
            return self._matrix[idx]


def test():
    logging.info('Run tests')
    matrix = Matrix(12, 10, 10)
    print('Field count: {}\n'.format(len(matrix)))
    print('Printing:')
    print('__str__:\n{}'.format(matrix))
    print('console_matrix:\n{}'.format(matrix.console_matrix()))
    print('Accessing:')
    print('matrix[1, 1] : {}'.format(str(matrix[1, 1])))
    print('matrix[1][-1]: {}'.format(str(matrix[1][-1])))


if __name__ == '__main__':
    test()
