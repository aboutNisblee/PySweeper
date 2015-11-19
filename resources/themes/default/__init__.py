# coding=utf-8
"""
Created on 18.11.2015

:author: Moritz Nisblé (mNisblee) <moritz.nisble@gmx.de>
"""
import logging
import glob
import os
from PIL import Image
import resources.themes as themes

logging.debug(__file__ + ' imported')


class Default(themes.FieldImages):
    """
    Default theme.
    Implements resources.themes.FieldImages
    """

    def __init__(self):
        themes.FieldImages.__init__(self)

        # FIXME: Vice versa please! Glob relative and add path for open.
        for file in glob.glob(os.path.join(os.path.dirname(os.path.realpath(__file__)), '*.png')):
            try:
                self._fields[os.path.splitext(os.path.basename(file))[0]] = Image.open(file)
            except IOError as e:
                logging.warning(e)

    def field_name_decode(self, revealed=False, adjacent_bombs=0, bomb=False):
        """
        Get the theme specific name of a field image with the given properties.
        (Interface implementation)
        :param revealed: Reveled field?
        :param adjacent_bombs: Number of adjacent bombs.
        :param bomb: Is it a bomb?
        :return: A name that can be used to address the photos in Theme.
        """
        if revealed:
            filename = 'p-{}'.format(adjacent_bombs if not bomb else 'bomb')
        else:
            # TODO: Add bomb, bang and query
            filename = 'u'
        return filename


# Instantiate an object on loading for the managing module to be independent from class name.
# FIXME: Ask Tim: This variable should come from the importing module!
# FIXME: Else each theme is required to haf such a variable.
theme = Default()
