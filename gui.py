# coding=utf-8
"""
Created on 14.11.2015

:author: Moritz Nisblé (mNisblee) <moritz.nisble@gmx.de>
"""
import os
import glob
from tkinter import *
from PIL import Image, ImageTk

from logic import *


class Resources(object):
    root_dir = os.path.dirname(os.path.realpath(__file__))
    res_dir = os.path.join(root_dir, 'resources')
    field_images = []

    @staticmethod
    def load():
        os.pathsep
        for file in glob.glob(os.path.join(Resources.res_dir, 'drawable', '*.png')):
            try:
                Resources.field_images.append(ImageTk.PhotoImage(Image.open(file)))
            except IOError as e:
                logging.warning(e)


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


class GameGrid(object):
    def __init__(self, parent, matrix):
        self._parent = parent
        self._matrix = matrix

        self._fr_main = Frame(self._parent)
        # self._fr_main.pack(padx='0m', pady='0m')  # FIXME: Use grid and delegate destroy method to it!
        self._fr_rows = [Frame(self._fr_main), ]
        self._fr_rows[0].pack(padx='0m', pady='0m')

        # TODO: Load images
        # self.image = PhotoImage(file='../resources/unpushed_grayback_round_1.png')

        for field in Matrix.row_wise(self._matrix, True):
            if field:
                bt = FieldButton(self._fr_rows[-1], field)
                bt.configure(width=1)
                bt.pack(side=LEFT)
            else:
                self._fr_rows.append(Frame(self._fr_main))
                self._fr_rows[-1].pack(padx='0m', pady='0m')

    def __getattr__(self, item):
        return getattr(self._fr_main, item)


class MainWindowObserver:
    def on_new_game_pressed(self):
        pass


class MainWindow(Observable, object):
    def __init__(self, parent):
        super().__init__()

        self._parent = parent

        self._main_container = Frame(self._parent)
        self._main_container.pack()

        self._control_container = Frame(self._main_container)
        self._control_container.pack()
        self._new_game_button = Button(self._control_container)
        self._new_game_button.configure(command=self._on_new_game_pressed)
        self._new_game_button.pack(anchor='center')

        self._grid_container = Frame(self._main_container)
        self._grid_container.pack()
        self._game_grid = None

    def new_matrix(self, matrix):
        # TODO: Check for memory leaks!
        if self._game_grid:
            self._game_grid.pack_forget()
        self._game_grid = GameGrid(self._grid_container, matrix)
        self._game_grid.pack()

    def _on_new_game_pressed(self):
        for obs in self.observers:
            obs.on_new_game_pressed()


class Controller(MainWindowObserver, object):
    def __init__(self, args=None):
        # FIXME: This is not correct! Runtime error when key not present!!
        self._columns = args.columns if args.columns else 12
        self._rows = args.rows if args.rows else 10
        self._bombs = args.bombs if args.bombs else 10

        self._tkroot = Tk()
        self._mainwindow = MainWindow(self._tkroot)
        self._mainwindow.add_observer(self)

        self._matrix = Matrix(self._columns, self._rows, self._bombs)
        # TODO: Dirrrty! Grid should wrap the frame or better a grid and delegate the destroy method.
        self._mainwindow.new_matrix(self._matrix)

    def run(self):
        """ Run the main loop. """
        Resources().load()

        self._tkroot.mainloop()

    def on_new_game_pressed(self):
        print('New Game!')
        self._matrix = Matrix(self._columns, self._rows, self._bombs)
        self._mainwindow.new_matrix(self._matrix)


def run(columns=12, rows=10, bombs=10):
    root = Tk()
    mainwindow = MainWindow(root, columns, rows, bombs)
    root.mainloop()


if __name__ == '__main__':
    run()
