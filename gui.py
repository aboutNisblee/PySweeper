# coding=utf-8
"""
Created on 14.11.2015

:author: Moritz Nisblé (mNisblee) <moritz.nisble@gmx.de>
"""
import importlib
import tkinter as tk
from PIL import ImageTk
from memprof import *
from logic import *

g_theme = None


class Theme(object):
    def __init__(self):
        self.field_pics = None
        self.load()

    def load(self, theme='default'):
        theme_mod = importlib.__import__('resources.themes.' + theme, globals(), locals(), ['*'], 0)
        self.field_pics = [ImageTk.PhotoImage(image) for image in theme_mod.field_images]


class Tk(object):
    """
    Tk wrapper.
    Everything that must be loaded a startup and depends on a initialized Tk instance
    can be loaded in the initializer of this class.
    """

    def __init__(self):
        self._tk = tk.Tk()
        global g_theme
        g_theme = Theme()

    @property
    def tk(self):
        return self._tk

    def __getattr__(self, item):
        return getattr(self._tk, item)


class FieldButton(FieldObserver, tk.Button):
    """
    Button subclass that represents a single field in the GUI,
    observes its Field in the Matrix and reacts to callbacks made by it.
    """

    def __init__(self, parent, field):
        tk.Button.__init__(self, parent)
        self._field = field
        self.configure(command=self._field.reveal, image=g_theme.field_pics[0])
        self._field.add_observer(self)

    def on_reveal(self, field):
        # TODO: Register one handler for all fields and remove this class.
        if field.revealed:
            return
        self.configure(relief=tk.SUNKEN)
        if field.adjacent_bombs() or field.bomb:
            self.configure(text=str(field.console_symbol()))


class GameGrid(object):
    """ View class that holds the game grid. """

    def __init__(self, parent, matrix):
        self._parent = parent
        self._matrix = matrix

        self._fr_main = tk.Frame(self._parent)
        # self._fr_main.pack(padx='0m', pady='0m')  # FIXME: Use grid and delegate destroy method to it!
        self._fr_rows = [tk.Frame(self._fr_main), ]
        self._fr_rows[0].pack(padx='0m', pady='0m')

        for field in Matrix.row_wise(self._matrix, True):
            if field:
                bt = FieldButton(self._fr_rows[-1], field)
                bt.configure(width=1)
                bt.pack(side=tk.LEFT)
            else:
                self._fr_rows.append(tk.Frame(self._fr_main))
                self._fr_rows[-1].pack(padx='0m', pady='0m')

    def __getattr__(self, item):
        return getattr(self._fr_main, item)


class MainWindowObserver:
    """ MainWindow observer interface. """

    def on_new_game_pressed(self):
        """ Invoked by MainWindow when the new game button was pressed. """
        pass


class MainWindow(Observable, object):
    def __init__(self, parent):
        super().__init__()

        self._parent = parent

        self._main_container = tk.Frame(self._parent)
        self._main_container.pack()

        self._control_container = tk.Frame(self._main_container)
        self._control_container.pack()
        self._new_game_button = tk.Button(self._control_container)
        self._new_game_button.configure(command=self._on_new_game_pressed)
        self._new_game_button.pack(anchor='center')

        self._grid_container = tk.Frame(self._main_container)
        self._grid_container.pack(expand=True)
        self._game_grid = None

    def new_matrix(self, matrix):
        if self._game_grid:
            # Remember to not use pack_forget()!! It may cause memory leaks!!
            self._game_grid.destroy()
        self._game_grid = GameGrid(self._grid_container, matrix)
        self._game_grid.pack()

    def _on_new_game_pressed(self):
        for obs in self.observers:
            obs.on_new_game_pressed()


class Controller(MainWindowObserver, object):
    def __init__(self, args=None):
        self._columns = args.columns if 'columns' in args else 12
        self._rows = args.rows if 'rows' in args else 10
        self._bombs = args.bombs if 'bombs' in args else 10

        self._tkroot = Tk()

        self._mainwindow = MainWindow(self._tkroot)
        self._mainwindow.add_observer(self)

        self._matrix = Matrix(self._columns, self._rows, self._bombs)
        # TODO: Dirrrty! GameGrid should wrap the frame or better a grid and delegate the destroy method.
        self._mainwindow.new_matrix(self._matrix)

    def run(self):
        """ Run the main loop. """
        self._tkroot.mainloop()

    def on_new_game_pressed(self):
        print('New Game!')
        self._matrix = Matrix(self._columns, self._rows, self._bombs)
        self._mainwindow.new_matrix(self._matrix)


@memprof(threshold=1024, plot=True)
def test():
    import argparse
    controller = Controller(argparse.Namespace(columns=20, rows=15, bombs=20))
    controller.run()


if __name__ == '__main__':
    test()
