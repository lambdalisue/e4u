#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:    alisue
# Date:        2011/03/23
#
import code

__ALL__ = ['Symbol']

class Symbol(object):
    u"""Emoji symbol class"""
    def __init__(self, e):
        u"""Constructor of the Symbol. Do not call it manually. Use `Symbol.load()` insted
        
        Attribute:
            e        - the instance of BeautifulSoup represent emoji4unicode's e element.
        """ 
        # Get data from attribute
        self._id = e['id']
        self._text_fallback = e.get('text_fallback', u"")
        self._text_repr = e.get('text_repr', u"")
        # Get code from attribute
        self._unicode = code.Unicode(e, self.fallback)
        self._google = code.Google(e, self.fallback)
        self._docomo = code.DoCoMo(e, self.fallback)
        self._kddi = code.KDDI(e, self.fallback)
        self._softbank = code.SoftBank(e, self.fallback)
    # Properties
    fallback = property(lambda self: self._text_fallback or self._text_repr)
    id = property(lambda self: self._id)
    unicode = property(lambda self: self._unicode)
    google = property(lambda self: self._google)
    docomo = property(lambda self: self._docomo)
    kddi = property(lambda self: self._kddi)
    softbank = property(lambda self: self._softbank)
