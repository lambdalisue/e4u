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

def load(filename=None,
        url=r"https://raw.githubusercontent.com/googlei18n/emoji4unicode/master/data/emoji4unicode.xml",
        loader_class=None):
    u"""load google's `emoji4unicode` project's xml file. must call this method first to use `e4u` library. this method never work twice if you want to reload, use `e4u.reload()` insted."""
    if not has_loaded():
        reload(filename, url, loader_class)
        
def reload(filename=None,
        url=r"https://raw.githubusercontent.com/googlei18n/emoji4unicode/master/data/emoji4unicode.xml",
        loader_class=None):
    u"""reload google's `emoji4unicode` project's xml file. must call this method first to use `e4u` library."""
    if loader_class is None:
        loader_class = loader.Loader
    global _loader
    _loader = loader_class()
    _loader.load(filename, url)

def has_loaded():
    u"""get has `e4u.load()` method called or not."""
    return _loader != None

def get(id):
    u"""get symbol via id"""
    symbol_dictionary = _loader.symbol_dictionary
    return symbol_dictionary[id]

def translate_char(source_char, carrier, reverse=False, encoding=False):
    u"""translate unicode emoji character to unicode carrier emoji character (or reverse)
    
    Attributes:
        source_char   - emoji character. it must be unicode instance or have to set `encoding` attribute to decode
        carrier       - the target carrier
        reverse       - if you want to translate CARRIER => UNICODE, turn it True
        encoding      - encoding name for decode (Default is None)
    
    """
    if not isinstance(source_char, unicode) and encoding:
        source_char = source_char.decode(encoding, 'replace')
    elif not isinstance(source_char, unicode):
        raise AttributeError(u"`source_char` must be decoded to `unicode` or set `encoding` attribute to decode `source_char`")
    if len(source_char) > 1:
        raise AttributeError(u"`source_char` must be a letter. use `translate` method insted.")
    translate_dictionary = _loader.translate_dictionaries[carrier]
    if not reverse:
        translate_dictionary = translate_dictionary[0]
    else:
        translate_dictionary = translate_dictionary[1]
    if not translate_dictionary:
        return source_char
    return translate_dictionary.get(source_char, source_char)

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
#    return regex_pattern.sub(lambda m: translate_dictionary.get(m.group(), m.group()), source)

def _code_to_profile(code_class):
    carrier = code_class._name
    encoding = code_class._encoding
    return {'carrier': carrier, 'encoding': encoding}
TEXT_TRANSLATE_PROFILE          = {'carrier': 'text', 'encoding': 'utf8'}
DOCOMO_IMG_TRANSLATE_PROFILE    = {'carrier': 'docomo_img', 'encoding': 'utf8'}
KDDI_IMG_TRANSLATE_PROFILE      = {'carrier': 'kddi_img', 'encoding': 'utf8'}
SOFTBANK_IMG_TRANSLATE_PROFILE  = {'carrier': 'softbank_img', 'encoding': 'utf8'}
GOOGLE_TRANSLATE_PROFILE        = _code_to_profile(code.Google)
DOCOMO_TRANSLATE_PROFILE        = _code_to_profile(code.DoCoMo)
KDDI_TRANSLATE_PROFILE          = _code_to_profile(code.KDDI)
SOFTBANK_TRANSLATE_PROFILE      = _code_to_profile(code.SoftBank)
