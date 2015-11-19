# coding=utf-8
"""
Created on 14.11.2015

:author: Moritz Nisblé (mNisblee) <moritz.nisble@gmx.de>
"""
import tkinter as tk
from memprof import *
from logic import *
from resources.themes import Theme

g_theme = Theme()  # Global theme variable


class FieldButton(FieldObserver, tk.Button):
    """
    Button subclass that represents a single field in the GUI,
    observes its Field in the Matrix and reacts to callbacks made by the logic.
    """

    def __init__(self, parent, field):
        tk.Button.__init__(self, parent)
        self._field = field
        self.configure(command=self._field.reveal, image=g_theme.field_pic(g_theme.field_name_decode()))
        self._field.add_observer(self)

    def refresh_theme(self):
        pass

    def on_reveal(self, field):
        """ Reveal callback handler. """
        # TODO: Register one handler for all fields and remove this class.
        # If already revealed bail out, to break the chain.
        if field.revealed:
            return
        self.configure(relief=tk.SUNKEN, image=g_theme.field_pic(
            g_theme.field_name_decode(revealed=True,
                                      adjacent_bombs=field.adjacent_bombs(),
                                      bomb=field.bomb)))


class GameGrid(object):
    """ View class that holds the game grid. """

    def __init__(self, master, matrix):
        self._master = master
        self._matrix = matrix

        self._container = tk.Frame(self._master)
        for field in Matrix.row_wise(self._matrix):
            bt = FieldButton(self._container, field)
            self._container.columnconfigure(field.column, weight=1)
            self._container.rowconfigure(field.row, weight=1)
            bt.grid(column=field.column, row=field.row, sticky=tk.N + tk.E + tk.S + tk.W)

    def __getattr__(self, item):
        """ Delegation to main frame. """
        return getattr(self._container, item)


class MainWindowObserver:
    """ MainWindow observer interface. """

    def on_new_game_pressed(self):
        """ Invoked by MainWindow when the new game button was pressed. """
        pass


class MainWindow(Observable, tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        Observable.__init__(self)

        self.grid(sticky=tk.N + tk.E + tk.S + tk.W)

        # Expand window
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._new_game_button = tk.Button(self)
        self._new_game_button.configure(command=self._on_new_game_pressed)
        self._new_game_button.grid()

        self._game_grid = None

    def reset_matrix(self, matrix):
        """
        Show a new Matrix, delete the old one.
        :param matrix: A Matrix object.
        """
        if self._game_grid:
            # Remember to not use pack_forget()!! It may cause memory leaks!!
            self._game_grid.destroy()
        self._game_grid = GameGrid(self, matrix)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self._game_grid.grid(row=1, sticky=tk.N + tk.E + tk.S + tk.W)

    def _on_new_game_pressed(self):
        """ Internal callback handler for the new game button. """
        for obs in self.observers:
            # Inform all observers
            obs.on_new_game_pressed()


class Controller(MainWindowObserver, object):
    def __init__(self, args=None):
        self._columns = args.columns if 'columns' in args else 12
        self._rows = args.rows if 'rows' in args else 10
        self._bombs = args.bombs if 'bombs' in args else 10

        self._tkroot = tk.Tk()

        self._mainwindow = MainWindow(self._tkroot)
        # Register the Controller as observer of Mainwindow
        self._mainwindow.add_observer(self)

        self.on_new_game_pressed()

    def run(self):
        """ Run the main loop. """
        self._tkroot.mainloop()

    def on_new_game_pressed(self):
        """ New game button callback handler. """
        self._mainwindow.reset_matrix(Matrix(self._columns, self._rows, self._bombs))


@memprof(threshold=1024, plot=True)
def test():
    import argparse
    controller = Controller(argparse.Namespace(columns=20, rows=15, bombs=20))
    controller.run()


if __name__ == '__main__':
    test()
