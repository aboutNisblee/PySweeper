#!/usr/bin/env python3
# coding=utf-8
"""
Created on 14.11.2015

:author: Moritz Nisblé (mNisblee) <moritz.nisble@gmx.de>
"""

from tkinter import *
from game.logic import Matrix


class MainWindow(object):
    def __init__(self, parent):
        self.parent = parent

        self.matrix = Matrix(10, 10, 5)

        # TODO: Wrap button by using delegation and add symbols and desired behaviour.

        self.fr_vert = Frame(parent)
        self.fr_vert.pack()

        self.fr_rows = [Frame(self.fr_vert), ]
        self.fr_rows[0].pack()

        for field in Matrix.row_wise(self.matrix, True):
            if field:
                bt = Button(self.fr_rows[-1])
                bt.configure(text=field.console_symbol())
                bt.pack(side=LEFT)
            else:
                self.fr_rows.append(Frame(self.fr_vert))
                self.fr_rows[-1].pack()


if __name__ == '__main__':
    root = Tk()
    mainwindow = MainWindow(root)

    root.mainloop()
