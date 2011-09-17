#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:    alisue
# Date:        2011/03/23
#
# Ref: https://bitbucket.org/tokibito/django-bpmobile/src/7a09b1dea05c/bpmobile/utils.py
# Ref: http://code.google.com/p/emoji4unicode/source/browse/trunk/src/carrier_data.py
#
from itertools import izip
import re
import warnings

def code_to_unicode(code):
    u"""Convert character code(hex) to unicode"""
    def utf32chr(n):
        """utf32char for narrow build python"""
        return eval("u\'\\U%08X\'" % n)
    def lazy_unichr(n):
        try:
            return unichr(n)
        except ValueError:
            warnings.warn("Your python it built as narrow python. Make with "
                "'--enable-unicode=ucs4' configure option to build wide python")
            return utf32chr(n)
    if code and isinstance(code, basestring):
        clean_code = code.replace('>', '')
        if clean_code:
            return u''.join([lazy_unichr(int(code_char, 16)) for code_char in clean_code.split('+') if code_char])
    return None
def code_to_sjis(code):
    u"""Convert character code(hex) to string"""
    if code and isinstance(code, basestring):
        clean_code = code.replace('>', '')
        if clean_code:
            _code_to_sjis_char = lambda c: ''.join([chr(int("%c%c"%(a, b), 16)) for a, b in izip(c[0::2], c[1::2])])
            return ''.join([_code_to_sjis_char(code_char) for code_char in clean_code.split('+') if code_char])
    return None
def unicode_to_code(uni):
    if not uni:
        return u"0000"
    code = []
    for x in uni:
        code.append(u"%04x" % ord(x))
    return "+".join(code)

def get_range_from_code(code, ranges):
    for range in ranges:
        if range[0] <= code <= range[1]: return range
    return None

def create_regex_patterns(symbols):
    u"""create regex patterns for text, google, docomo, kddi and softbank via `symbols`
    
    create regex patterns for finding emoji character from text. the pattern character use
    `unicode` formatted character so you have to decode text which is not decoded.
    """
    pattern_unicode = []
    pattern_google = []
    pattern_docomo = []
    pattern_kddi = []
    pattern_softbank = []
    for x in symbols:
        if x.unicode.code: pattern_unicode.append(re.escape(unicode(x.unicode)))
        if x.google.code: pattern_google.append(re.escape(unicode(x.google)))
        if x.docomo.code: pattern_docomo.append(re.escape(unicode(x.docomo)))
        if x.kddi.code: pattern_kddi.append(re.escape(unicode(x.kddi)))
        if x.softbank.code: pattern_softbank.append(re.escape(unicode(x.softbank)))
#    pattern_unicode = re.compile(u"[%s]" % u''.join(pattern_unicode))
#    pattern_google = re.compile(u"[%s]" % u''.join(pattern_google))
#    pattern_docomo = re.compile(u"[%s]" % u''.join(pattern_docomo))
#    pattern_kddi = re.compile(u"[%s]" % u''.join(pattern_kddi))
#    pattern_softbank = re.compile(u"[%s]" % u''.join(pattern_softbank))
    pattern_unicode = re.compile(u"%s" % u'|'.join(pattern_unicode))
    pattern_google = re.compile(u"%s" % u'|'.join(pattern_google))
    pattern_docomo = re.compile(u"%s" % u'|'.join(pattern_docomo))
    pattern_kddi = re.compile(u"%s" % u'|'.join(pattern_kddi))
    pattern_softbank = re.compile(u"%s" % u'|'.join(pattern_softbank))
    return {
        #                forward            reverse
        'text':         (None,              pattern_unicode),
        'docomo_img':   (None,              pattern_unicode),
        'kddi_img':     (None,              pattern_unicode),
        'softbank_img': (None,              pattern_unicode),
        'google':       (pattern_google,    pattern_unicode),
        'docomo':       (pattern_docomo,    pattern_unicode),
        'kddi':         (pattern_kddi,      pattern_unicode),
        'softbank':     (pattern_softbank,  pattern_unicode),
    }
    
def create_translate_dictionaries(symbols):
    u"""create translate dictionaries for text, google, docomo, kddi and softbank via `symbols`
    
    create dictionaries for translate emoji character to carrier from unicode (forward) or to unicode from carrier (reverse).
    method return dictionary instance which key is carrier name and value format is `(forward_dictionary, reverse_dictionary)`
    each dictionary expect `unicode` format. any text not decoded have to be decode before using this dictionary (like matching key)
    
    DO NOT CONFUSE with carrier's UNICODE emoji. UNICODE emoji like `u"\uE63E"` for DoCoMo's sun emoji is not expected. expected character
    for DoCoMo's sun is decoded character from `"\xF8\x9F"` (actually decoded unicode of `"\xF8\xF9"` is `u"\uE63E"` however not all emoji
    can convert with general encode/decode method. conversion of UNICODE <-> ShiftJIS is operated in Symbol constructor and stored in Symbol's `sjis`
    attribute and unicode formatted is `usjis` attribute.)
        
    """
    unicode_to_text = {}
    unicode_to_docomo_img = {}
    unicode_to_kddi_img = {}
    unicode_to_softbank_img = {}
    unicode_to_google = {}
    unicode_to_docomo = {}
    unicode_to_kddi = {}
    unicode_to_softbank = {}
    google_to_unicode = {}
    docomo_to_unicode = {}
    kddi_to_unicode = {}
    softbank_to_unicode = {}
    for x in symbols:
        if x.unicode.keyable:
            unicode_to_text[unicode(x.unicode)] = x.unicode.fallback
            unicode_to_docomo_img[unicode(x.unicode)] = x.docomo.thumbnail
            unicode_to_kddi_img[unicode(x.unicode)] = x.kddi.thumbnail
            unicode_to_softbank_img[unicode(x.unicode)] = x.softbank.thumbnail
            unicode_to_google[unicode(x.unicode)] = unicode(x.google)
            unicode_to_docomo[unicode(x.unicode)] = unicode(x.docomo)
            unicode_to_kddi[unicode(x.unicode)] = unicode(x.kddi)
            unicode_to_softbank[unicode(x.unicode)] = unicode(x.softbank)
        if x.google.keyable: google_to_unicode[unicode(x.google)] = unicode(x.unicode)
        if x.docomo.keyable: docomo_to_unicode[unicode(x.docomo)] = unicode(x.unicode)
        if x.kddi.keyable: kddi_to_unicode[unicode(x.kddi)] = unicode(x.unicode)
        if x.softbank.keyable: softbank_to_unicode[unicode(x.softbank)] = unicode(x.unicode)
    return {
        #                forward                reverse
        'text':         (None,                  unicode_to_text),
        'docomo_img':   (None,                  unicode_to_docomo_img),
        'kddi_img':     (None,                  unicode_to_kddi_img),
        'softbank_img': (None,                  unicode_to_softbank_img),
        'google':       (google_to_unicode,     unicode_to_google),
        'docomo':       (docomo_to_unicode,     unicode_to_docomo),
        'kddi':         (kddi_to_unicode,       unicode_to_kddi),
        'softbank':     (softbank_to_unicode,   unicode_to_softbank),
    }
