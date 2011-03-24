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

def code_to_unicode(code):
    u"""Convert character code(hex) to unicode"""
    if code and isinstance(code, basestring):
        clean_code = code.replace('>', '')
        if clean_code:
            return u''.join([unichr(int(code_char, 16)) for code_char in clean_code.split('+') if code_char])
    return None
def code_to_sjis(code):
    u"""Convert character code(hex) to string"""
    if code and isinstance(code, basestring):
        clean_code = code.replace('>', '')
        if clean_code:
            return "".join([chr(int("0x%c%c"%(a, b), 16)) for a, b in izip(code[0::2], code[1::2])])
    return None
def unicode_to_code(uni):
    if not uni:
        return u"0000"
    code = []
    for x in uni:
        code.append(u"%04x" % ord(x))
    return "+".join(code)

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
        if x.unicode.code: pattern_unicode.append(re.escape(x.unicode.unicode))
        if x.google.code: pattern_google.append(re.escape(x.google.unicode))
        if x.docomo.code: pattern_docomo.append(re.escape(x.docomo.usjis))
        if x.kddi.code: pattern_kddi.append(re.escape(x.kddi.usjis))
        if x.softbank.code: pattern_softbank.append(re.escape(x.softbank.usjis))
    pattern_unicode = re.compile(u"[%s]" % u''.join(pattern_unicode))
    pattern_google = re.compile(u"[%s]" % u''.join(pattern_google))
    pattern_docomo = re.compile(u"[%s]" % u''.join(pattern_docomo))
    pattern_kddi = re.compile(u"[%s]" % u''.join(pattern_kddi))
    pattern_softbank = re.compile(u"[%s]" % u''.join(pattern_softbank))
    return {
        #            incoming           outgoing
        'text':     (None,              pattern_unicode),
        'google':   (pattern_google,    pattern_unicode),
        'docomo':   (pattern_docomo,    pattern_unicode),
        'kddi':     (pattern_kddi,      pattern_unicode),
        'softbank': (pattern_softbank,  pattern_unicode),
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
            unicode_to_text[x.unicode.unicode] = x.unicode.fallback
            unicode_to_google[x.unicode.unicode] = x.google.unicode
            unicode_to_docomo[x.unicode.unicode] = x.docomo.usjis
            unicode_to_kddi[x.unicode.unicode] = x.kddi.usjis
            unicode_to_softbank[x.unicode.unicode] = x.softbank.usjis
        if x.google.keyable: google_to_unicode[x.google.unicode] = x.unicode.unicode
        if x.docomo.keyable: docomo_to_unicode[x.docomo.usjis] = x.unicode.unicode
        if x.kddi.keyable: kddi_to_unicode[x.kddi.usjis] = x.unicode.unicode
        if x.softbank.keyable: softbank_to_unicode[x.softbank.usjis] = x.unicode.unicode
    return {
        #            forward                reverse
        'text':     (None,                  unicode_to_text),
        'google':   (google_to_unicode,     unicode_to_google),
        'docomo':   (docomo_to_unicode,     unicode_to_docomo),
        'kddi':     (kddi_to_unicode,       unicode_to_kddi),
        'softbank': (softbank_to_unicode,   unicode_to_softbank),
    }