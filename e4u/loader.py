#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:    alisue
# Date:        2011/03/24
#
from urllib import urlopen
from BeautifulSoup import BeautifulStoneSoup

from utils import create_regex_patterns, create_translate_dictionaries 
from symbol import Symbol

class Loader(object):
    # Properties
    symbols = property(lambda self: self._symbols)
    symbol_dictionary = property(lambda self: self._symbol_dictionary)
    regex_patterns = property(lambda self: self._regex_patterns)
    translate_dictionaries = property(lambda self: self._translate_dictionaries)
    
    
    def _load(self, xml):
        soup = BeautifulStoneSoup(xml)('e')
        symbols = []
        symbol_dictionary = {}
        for e in soup:
            s = Symbol(e)
            symbols.append(s)
            symbol_dictionary[s.id] = s
        self._symbols = symbols
        self._symbol_dictionary = symbol_dictionary
        self._regex_patterns = create_regex_patterns(self.symbols)
        self._translate_dictionaries = create_translate_dictionaries(self.symbols)
        
        
    def load(self, filename=None, url=r"https://raw.githubusercontent.com/googlei18n/emoji4unicode/master/data/emoji4unicode.xml"):
        if filename:
            xml = open(filename, 'r').read()
        else:
            xml = urlopen(url).read()
        self._load(xml)
