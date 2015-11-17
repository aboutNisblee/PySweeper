# coding=utf-8
"""
Created on 17.11.2015

:author: Moritz Nisblé (mNisblee) <moritz.nisble@gmx.de>
"""


class Observable:
    def __init__(self):
        self._observers = []

    @property
    def observers(self):
        return self._observers

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def rem_observer(self, observer):
        self._observers.remove(observer)
