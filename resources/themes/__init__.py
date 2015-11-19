# coding=utf-8
"""
Created on 18.11.2015

:author: Moritz Nisblé (mNisblee) <moritz.nisble@gmx.de>
"""
import importlib
import logging

from PIL import ImageTk

logging.debug(__file__ + ' imported')


class FieldImages(object):
    """ Base class for themes that provide field images. """

    def __init__(self):
        # Child should fill this dict with 'filename' = PIL.Image(file).
        # Filename should not contain path or extension.
        self._fields = {}

    @property
    def fields(self):
        return self._fields

    def field_name_decode(self, revealed=False, adjacent_bombs=0, bomb=False):
        """

        :param revealed:
        :param adjacent_bombs
        :param bomb:
        :return:
        """
        pass


class Theme(object):
    """ Theme management. """

    def __init__(self):
        self._field_pic_cache = {}
        self._theme = None
        self.load_theme()

    def load_theme(self, theme='default'):
        self._theme = importlib.__import__('resources.themes.' + theme, globals(), locals(), ['*'], 0).theme

    def field_pic(self, name):
        """ Returns the PhotoImage for the given field name.
        Note: It is the responsibility of the concrete theme to generate a valid name.
        Use delegated method field_name_decode() to obtain a valid name.
        DO NOT TRY TO CALL THIS METHOD BEFORE INITIALIZATION OF TK
        :param name: The name of the field photo.
        :return: An ImageTk.PhotoImage.
        """
        # Lazy load field photos
        pic = self._field_pic_cache.get(name)
        if not pic:
            pic = ImageTk.PhotoImage(self._theme.fields[name])
            self._field_pic_cache[name] = pic
        return pic

    def __getattr__(self, item):
        """ Delegation to current theme. """
        return getattr(self._theme, item)
