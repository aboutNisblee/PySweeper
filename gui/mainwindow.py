#!/usr/bin/env python3
# coding=utf-8
"""
Created on 14.11.2015

:author: Moritz Nisblé (mNisblee) <moritz.nisble@gmx.de>
"""

from tkinter import *
from game.logic import *


class FieldButton(FieldObserver, Button):
    def __init__(self, parent, field):
        Button.__init__(self, parent)
        self._field = field
        self.configure(command=self._field.reveal)
        self._field.add_observer(self)

    def on_reveal(self, field):
        # TODO: Register one handler for all fields and remove this class.
        if field.revealed:
            return
        self.configure(relief=SUNKEN)
        if field.adjacent_bombs() or field.bomb:
            self.configure(text=str(field.console_symbol()))


class MainWindow(object):
    def __init__(self, parent):
        self.parent = parent
        self.matrix = Matrix(10, 10, 20)

        # TODO: Wrap button by using delegation and add symbols and desired behaviour.

        self.fr_vert = Frame(parent)
        self.fr_vert.pack(padx='0m', pady='0m')  # FIXME: Use grid!

        self.fr_rows = [Frame(self.fr_vert), ]
        self.fr_rows[0].pack(padx='0m', pady='0m')

        for field in Matrix.row_wise(self.matrix, True):
            if field:
                bt = FieldButton(self.fr_rows[-1], field)
                bt.configure(width=1)
                bt.pack(side=LEFT)
            else:
                self.fr_rows.append(Frame(self.fr_vert))
                self.fr_rows[-1].pack(padx='0m', pady='0m')


if __name__ == '__main__':
    root = Tk()
    mainwindow = MainWindow(root)

    root.mainloop()
