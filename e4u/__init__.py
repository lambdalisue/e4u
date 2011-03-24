#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:    alisue
# Date:        2011/03/23
#
import utils
import loader
import code
import symbol

_loader = None

def load(filename=None, url=r"http://emoji4unicode.googlecode.com/svn/trunk/data/emoji4unicode.xml", loader_class=loader.Loader):
    u"""load google's `emoji4unicode` project's xml file. must call this method first to use `e4u` library."""
    global _loader
    _loader = loader_class()
    _loader.load(filename, url)

def translate(source, carrier, reverse=False, encoding=None):
    u"""translate unicode text contain emoji character to unicode carrier text (or reverse)
    
    Attributes:
        source        - text contain emoji character. it must be unicode instance or have to set `encoding` attribute to decode
        carrier       - the target carrier
        reverse       - if you want to translate CARRIER TEXT => UNICODE, turn it True
        encoding      - encoding name for decode (Default is None)
    
    """
    if not isinstance(source, unicode) and encoding:
        source = source.decode(encoding, 'replace')
    elif not isinstance(source, unicode):
        raise AttributeError(u"`source` must be decoded to `unicode` or set `encoding` attribute to decode `source`")
    regex_pattern = _loader.regex_patterns[carrier]
    translate_dictionary = _loader.translate_dictionaries[carrier]
    if not reverse:
        regex_pattern = regex_pattern[0]
        translate_dictionary = translate_dictionary[0]
    else:
        regex_pattern = regex_pattern[1]
        translate_dictionary = translate_dictionary[1]
    if not regex_pattern or not translate_dictionary:
        return source
    return regex_pattern.sub(lambda m: translate_dictionary[m.group()], source)

TEXT_TRANSLATE_PROFILE = {'carrier': 'text', 'encoding': 'utf8'}
GOOGLE_TRANSLATE_PROFILE = {'carrier': 'google', 'encoding': 'utf8'}
DOCOMO_TRANSLATE_PROFILE = {'carrier': 'docomo', 'encoding': 'cp932'}
KDDI_TRANSLATE_PROFILE = {'carrier': 'kddi', 'encoding': 'cp932'}
SOFTBANK_TRANSLATE_PROFILE= {'carrier': 'softbank', 'encoding': 'cp932'}