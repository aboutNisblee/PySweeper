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
    To be able to determine bombs after creation of the fields,
    a Field can also be a bomb.
    """

    def __init__(self, column, row):
        """
        Initialize a new Field.
        :param column: The column index.
        :param row: The row index.
        """
        if column < 0 or row < 0:
            raise ValueError('Column/row index cannot be negative')

        self.column = column
        self.row = row
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

    def reg_neighbour(self, field):
        """
        Register another Field a a neighbour of this one.
        :param field: A neighbour.
        """
        self.neighbours.append(field)

    def link(self, matrix):
        if not isinstance(matrix, Matrix):
            raise TypeError('Should pass a Matrix object')
        for c, r in self.n_idx:
            if c < 0 or r < 0 or c >= matrix.columns() or r >= matrix.rows():
                continue
            else:
                matrix[c][r].reg_neighbour(self)

    @property
    def bomb(self):
        """ Is this field a bomb. """
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

    def print_mark(self):
        return 'X' if self.bomb else str(self.adjacent_bombs)

    def __str__(self):
        return 'C:{} R:{} B:{}'.format(self.column, self.row, self._bomb)


class Matrix(object):
    """
    :todo: Pay attention to deep copies!
    """

    def __init__(self, columns=2, rows=2, bombs=1):
        self.matrix = []
        for c in range(columns):
            self.matrix.append([])
            for r in range(rows):
                self.matrix[c].append(Field(c, r))

        # FIXME DRY
        for c in range(columns):
            for r in range(rows):
                self.matrix[c][r].link(self)

        b = 0
        while b < bombs:
            c = randint(0, columns - 1)
            r = randint(0, rows - 1)
            if self.matrix[c][r].set_bomb(True):
                b += 1

    def columns(self):
        return len(self.matrix)

    def rows(self):
        return len(self.matrix[0])

    def __len__(self):
        return len(self.matrix) * len(self.matrix[0])

    def __str__(self):
        return self._str(lambda c, r: str(self.matrix[c][r]))

    def str_matrix(self):
        """
        Get a nicely formatted representation of the matrix as string.
        This is mainly used for debugging or logging purposes.
        :return: A string.
        """
        return self._str(lambda c, r: self.matrix[c][r].print_mark())

    def _str(self, getter):
        """
        Get a string representation of the current matrix. Call the passed
        callable for each field to insert the needed information.
        The matrix is displayed row-wise despite the internal representation
        is column-wise.
        :param getter: A callable that takes the column and row indices
        and returns a string.
        :return: A string.
        """
        string = ''  # Difference to usage of a list is not measurable
        for r in range(self.rows()):
            for c in range(self.columns()):
                string += getter(c, r)
                string += ' '
            string += '\n'
        return string

    def __getitem__(self, idx):
        try:
            # Is the passes index an sequence?
            # This makes calls as matrix[1, 1] possible.
            # IndexError is possibly raised but not caught. OK?
            c_idx, r_idx = idx
            return self.matrix[c_idx][r_idx]
        except (TypeError, ValueError):
            # If we get a TypeError only the column index was passed.
            # This makes calls like matrix[1][1] possible.
            # If a str is passed also handle it here. Error message is more
            # meaningful when trying to use a str as index.
            # 'TypeError: list indices must be integers, not str'
            # instead of
            # 'ValueError: need more than 1 value to unpack'
            return self.matrix[idx]


def test():
    logging.info('Run tests')
    matrix = Matrix(12, 10, 10)
    print('Field count: {}\n'.format(len(matrix)))
    # print('Printing:')
    # print('__str__:\n{}'.format(matrix))
    print('str_matrix:\n{}'.format(matrix.str_matrix()))
    # print('Accessing:')
    # print('matrix[1, 1] : {}'.format(str(matrix[1, 1])))
    # print('matrix[1][-1]: {}'.format(str(matrix[1][-1])))


if __name__ == '__main__':
    test()
