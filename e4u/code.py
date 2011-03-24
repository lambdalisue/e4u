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
        return "".join(result)
    sjis_code = property(lambda self: self._sjis_code)
    sjis = property(lambda self: self._sjis or self.fallback.encode('cp932'))
    usjis = property(lambda self: self.sjis.decode('cp932', 'replace') or self.fallback)

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
        (0xE63E, 0xE757, 0xF89F, 0xF9FC),
    )
    def __unicode__(self):
        return self.usjis
    def _image(self):
        if not self.code:
            return self.fallback
        base_url = r"http://www.nttdocomo.co.jp/service/imode/make/content/pictograph/basic/images/%d.gif"
        imgs = []
        for code in self.code.split('+'):
            code = int(code, 16)
            range = get_range_from_code(code, self._code_to_sjis_code_ranges)
            offset = code - range[0]
            imgs.append(base_url % (offset + 1))
        return imgs
    image = property(_image)
    
class KDDI(Carrier):
    _name = 'kddi'
    _encoding = 'cp932'
    _code_to_sjis_code_ranges = (
        (0xE468, 0xE5B4, 0xF640, 0xF7D1),
        (0xE5B5, 0xE5CC, 0xF7E5, 0xF7FC),
        (0xE5CD, 0xE5DF, 0xF340, 0xF352),
        (0xEA80, 0xEAFA, 0xF353, 0xF3CE),
        (0xEAFB, 0xEB0D, 0xF7D2, 0xF7E4),
        (0xEB0E, 0xEB8E, 0xF3CF, 0xF493),
    )
    def __unicode__(self):
        return self.usjis
    def _image(self):
        if not self.code:
            return self.fallback
        base_url = r"http://mail.google.com/mail/e/ezweb_ne_jp/%s"
        return [base_url % self._id]
    image = property(_image)
    
class SoftBank(Carrier):
    _name = 'softbank'
    _encoding = 'utf8'
    _code_to_sjis_code_ranges = (
        # Softbank official range is not correct.
        # See http://gyazo.com/5789130a3524a39a03369861eb142dfb.png
        #
        # Official: (0xE001, 0xE05A, 0xF941, 0xF99B),
        (0xE001, 0xE03E, 0xF941, 0xF97E),
        (0xE03F, 0xE05A, 0xF980, 0xF99B),
        #----------------------------------------------------------
        (0xE101, 0xE15A, 0xF741, 0xF79B),
        (0xE201, 0xE25A, 0xF7A1, 0xF7FA),
        (0xE301, 0xE34D, 0xF9A1, 0xF9ED),
        (0xE401, 0xE44C, 0xFB41, 0xFB8D),
        (0xE501, 0xE53E, 0xFBA1, 0xFBDE),
    )
    _code_to_sjis_code_ranges_official = (
        (0xE001, 0xE05A, 0xF941, 0xF99B),
        (0xE101, 0xE15A, 0xF741, 0xF79B),
        (0xE201, 0xE25A, 0xF7A1, 0xF7FA),
        (0xE301, 0xE34D, 0xF9A1, 0xF9ED),
        (0xE401, 0xE44C, 0xFB41, 0xFB8D),
        (0xE501, 0xE53E, 0xFBA1, 0xFBDE),
    )
    # SoftBank may refuse access image from external so the code below may not work.
    def _image(self):
        if not self.code:
            return self.fallback
        base_url = u"http://creation.mb.softbank.jp/web/img/%04X/%04X_20.gif"
        imgs = []
        for code in self.code.split('+'):
            code = int(code, 16)
            range = get_range_from_code(code, self._code_to_sjis_code_ranges_official)
            imgs.append(base_url % (range[0], code))
        return imgs
    image = property(_image)