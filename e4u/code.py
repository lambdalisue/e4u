#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:    alisue
# Date:        2011/03/24
#
# Ref: https://bitbucket.org/tokibito/django-bpmobile/src/7a09b1dea05c/bpmobile/utils.py
# Ref: http://code.google.com/p/emoji4unicode/source/browse/trunk/src/carrier_data.py
#
from utils import code_to_unicode, code_to_sjis, get_range_from_code
from thumbnails import get_docomo_thumbnail_urls, get_kddi_thumbnail_urls, get_softbank_thumbnail_urls

class Code(object):
    _name = None
    def __init__(self, e, fallback=None):
        self._id = e.get('id')
        code = e.get(self._name, None)
        if code:
            if code.startswith('>'):
                code = code[1:]
                self._duplicate = True
            else:
                self._duplicate = False
            self._code = code
            self._unicode = code_to_unicode(code)
        else:
            self._code = None
            self._unicode = None
        self._fallback = fallback
    def __unicode__(self):
        return self.unicode
    keyable = property(lambda self: self.code and not self.duplicate)
    duplicate = property(lambda self: self._duplicate)
    code = property(lambda self: self._code)
    unicode = property(lambda self: self._unicode or self.fallback)
    fallback = property(lambda self: self._fallback)

class Carrier(Code):
    _code_to_sjis_code_ranges = None
    def __init__(self, e, fallback):
        super(Carrier, self).__init__(e, fallback)
        if self.code:
            self._sjis_code = self._code_to_sjis_code(self.code)
            self._sjis = code_to_sjis(self._sjis_code)
        else:
            self._sjis_code = None
            self._sjis = None
    def _code_to_sjis_code(self, code):
        if not code:
            return None
        result = []
        for c in code.split("+"):
            c = int(c, 16)
            range = get_range_from_code(c, self._code_to_sjis_code_ranges)
            offset = c - range[0]
            dst = range[2] + offset
            result.append("%04X" % dst)
        return '+'.join(result)
    sjis_code = property(lambda self: self._sjis_code)
    sjis = property(lambda self: self._sjis or self.fallback.encode('cp932'))
    usjis = property(lambda self: self.sjis.decode('cp932', 'replace') or self.fallback)
    
    def _get_thumbnail_urls(self):
        raise NotImplementedError
    def _get_thumbnail_img(self):
        img = r"""<img src="%s" alt="%s" title="%s" style="width:1em;height:1em" />"""
        fallback = self.fallback
        urls = self._get_thumbnail_urls()
        if urls is None:
            return fallback
        results = []
        for url in urls:
            results.append(img % (url, fallback, fallback))
        return u''.join(results)
    thumbnail = property(_get_thumbnail_img)
    
class Unicode(Code):
    _name = 'unicode'
    _encoding = 'utf8'
class Google(Code):
    _name = 'google'
    _encoding = 'utf8'
class DoCoMo(Carrier):
    _name = 'docomo'
    _encoding = 'cp932'
    _code_to_sjis_code_ranges = (
        (0xE63E, 0xE69B, 0xF89F, 0xF8FC),
        (0xE69C, 0xE6DA, 0xF940, 0xF97E),
        (0xE6DB, 0xE757, 0xF980, 0xF9FC),
    )
    _code_to_docomo_id_ranges = (
        (0xE63E, 0xE6A5, 0x0001, 0x0068),
        (0xE6AC, 0xE6AE, 0x00A7, 0x00A9),
        (0xE6B1, 0xE6B3, 0x00AA, 0x00AC),
        (0xE6B7, 0xE6BA, 0x00AD, 0x00B0),
        (0xE6CE, 0xE6EB, 0x0069, 0x0086),
        (0xE6EC, 0xE70A, 0x0088, 0x00A6),
        (0xE70B, 0xE70B, 0x0087, 0x0087),
        (0xE70C, 0xE757, 0x0001, 0x004C),
    )

    def __unicode__(self):
        return self.usjis
    _get_thumbnail_urls = get_docomo_thumbnail_urls
    
class KDDI(Carrier):
    _name = 'kddi'
    _encoding = 'cp932'
    _code_to_sjis_code_ranges = (
        (0xE468, 0xE4A6, 0xF640, 0xF67E),
        (0xE4A7, 0xE523, 0xF680, 0xF6FC),
        (0xE524, 0xE562, 0xF740, 0xF77E),
        (0xE563, 0xE5B4, 0xF780, 0xF7D1),
        (0xE5B5, 0xE5CC, 0xF7E5, 0xF7FC),
        (0xE5CD, 0xE5DF, 0xF340, 0xF352),
        (0xEA80, 0xEAAB, 0xF353, 0xF37E),
        (0xEAAC, 0xEAFA, 0xF380, 0xF3CE),
        (0xEAFB, 0xEB0D, 0xF7D2, 0xF7E4),
        (0xEB0E, 0xEB3B, 0xF3CF, 0xF3FC),
        (0xEB3C, 0xEB7A, 0xF440, 0xF47E),
        (0xEB7B, 0xEB8E, 0xF480, 0xF493), 
    )
    def __unicode__(self):
        return self.usjis
    _get_thumbnail_urls = get_kddi_thumbnail_urls
    
class SoftBank(Carrier):
    _name = 'softbank'
    _encoding = 'utf8'
    _code_to_sjis_code_ranges = (
        (0xE001, 0xE03E, 0xF941, 0xF97E),
        (0xE03F, 0xE05A, 0xF980, 0xF99B),
        (0xE101, 0xE15A, 0xF741, 0xF79B),
        (0xE201, 0xE25A, 0xF7A1, 0xF7FA),
        (0xE301, 0xE34D, 0xF9A1, 0xF9ED),
        (0xE401, 0xE44C, 0xFB41, 0xFB8D),
        (0xE501, 0xE53E, 0xFBA1, 0xFBDE),
    )
    
    _get_thumbnail_urls = get_softbank_thumbnail_urls