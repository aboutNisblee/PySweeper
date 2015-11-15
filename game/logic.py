#!/usr/bin/env python3
# coding=utf-8
"""
Created on 29.10.2015

:author: Moritz Nisblé (mNisblee) <moritz.nisble@gmx.de>
"""

import logging
from random import randint


class FieldObserver:
    def on_reveal(self, field):
        pass


class MatrixObserver:
    def on_win(self):
        pass

    def on_lost(self):
        pass

    def on_remaining_bombs_changed(self):
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
        self._revealed = False
        self._obs = []

        # Determine indices of adjacent fields.
        self._neighbour_idx = (
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
        """ Get the column index. """
        return self._column

    @property
    def row(self):
        """ Get the row index. """
        return self._row

    @property
    def bomb(self):
        """ Is it a bomb? """
        return self._bomb

    @property
    def revealed(self):
        return self._revealed

    @property
    def neighbour_idx(self):
        """ Returns all valid neighbour indices.
        :return: A tuple of column, row.
        """
        return ((c, r) for c, r in self._neighbour_idx if
                not (c < 0 or r < 0 or c >= self._matrix.columns() or r >= self._matrix.rows()))

    def neighbours(self):
        return (self._matrix[idx] for idx in self.neighbour_idx)

    def adjacent_bombs(self):
        # TODO: Do I really need a list? Have a look at itertools.ifilter
        return [self._matrix[idx].bomb for idx in self.neighbour_idx].count(True)

    def set_bomb(self, value=True):
        """
        Mark/un-mark this field as bomb.
        :param value: The new value.
        :return: True when flag was changed, else False.
        """
        if not isinstance(value, bool):
            raise TypeError('Bomb flag should be of type bool')
        if self._bomb == value:
            return False

        self._bomb = value
        return True

    def reveal(self):
        if self._revealed:
            return
        # Call handler, before locking second reveal.
        # This way the handler is be able to determine state.
        for ob in self._obs:
            ob.on_reveal(self)
        self._revealed = True
        if not self.adjacent_bombs():
            for n in self.neighbours():
                n.reveal()
        elif self.bomb:
            # self.oberservers.lost()
            print('LOST')
            # TODO: Add win/lost check

    def mark(self):
        # TODO
        pass

    def add_observer(self, observer):
        if observer not in self._obs:
            self._obs.append(observer)

    def rem_observer(self, observer):
        self._obs.remove(observer)

    def console_symbol(self):
        return 'X' if self.bomb else str(self.adjacent_bombs())

    def __str__(self):
        return 'C:{} R:{} S:{}'.format(self.column, self.row, self.console_symbol())


class Matrix(object):
    """
    :todo: Pay attention to deep copies!
    """

    def __init__(self, columns=2, rows=2, bombs=1):
        self._bombs = bombs

        self._matrix = [[Field(c, r, self) for r in range(rows)] for c in range(columns)]

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

    @staticmethod
    def col_wise(matrix, yield_col=False):
        """
        Column-wise field generator.
        :param matrix: The Matrix instance to iterate over.
        :param yield_col: If true yielding after a complete row.
         """
        for c in range(matrix.columns()):
            for r in range(matrix.rows()):
                yield (matrix[c][r])
            if yield_col:
                yield False

    @staticmethod
    def row_wise(matrix, yield_row=False):
        """
        Row-wise field generator.
        :param matrix: The Matrix instance to iterate over.
        :param yield_row: If true yielding after a complete row.
        """
        for r in range(matrix.rows()):
            for c in range(matrix.columns()):
                yield (matrix[c][r])
            if yield_row:
                yield False  # TODO Whats the best type for None?? None? :D

    def __len__(self):
        """ Get the count of fields. """
        return len(self._matrix) * len(self._matrix[0])

    def __str__(self):
        string = 'Matrix information:\n' \
                 '{} fields in {} columns and {} rows\n' \
                 'containing {} bombs\n' \
                 'Field list:\n'.format(len(self), self.columns(), self.rows(), self.bombs)
        for field in Matrix.col_wise(self):
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
        for field in Matrix.row_wise(self, True):
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
    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)
    # logger.debug('Run tests')
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Run tests')
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
