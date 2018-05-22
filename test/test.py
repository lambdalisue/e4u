#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:    alisue
# Date:        2011/03/24
#
import unittest
import e4u

e4u.load()

DISPLAY_INFO = False

class TestCaseAbstract(object):
    _carrier = None
    _carrier_contents = None
    _unicode_contents = None
    _encoding = None
    
    def output(self, name, contents, expected, result):
        if not DISPLAY_INFO:
            return
        print "# %s #" % name
        print u"  Contents:\t%s" % contents
        print u"  Expected:\t%s" % expected
        print u"  Result:\t%s" % result
        print ""
        
    def test_carrier_to_unicode(self):
        contents = self._carrier_contents
        expected = self._unicode_contents
        profile = {
            'carrier': self._carrier,
            'encoding': self._encoding,
        }
        result = e4u.translate(contents, **profile)
        self.assertEqual(result, expected)
        self.output("%s => unicode" % self._carrier, contents, expected, result)
        
    def test_unicode_to_carrier(self):
        contents = self._unicode_contents
        expected = self._carrier_contents
        profile = {
            'reverse': True,
            'carrier': self._carrier,
            'encoding': self._encoding,
        }
        result = e4u.translate(contents, **profile)
        self.assertEqual(result, expected)
        self.output("unicode => %s" % self._carrier, contents, expected, result)
        
class DoCoMoTestCase(unittest.TestCase, TestCaseAbstract):
    _carrier = 'docomo'
    _carrier_contents = "\xF8\x9F \xF8\xA0 \xF8\xA1".decode('cp932', 'replace')
    _unicode_contents = u"\u2600 \u2601 \u2614"
    _encoding = 'cp932'
class KDDITestCase(unittest.TestCase, TestCaseAbstract):
    _carrier = 'kddi'
    _carrier_contents = "\xF6\x60 \xF6\x65 \xF6\x64".decode('cp932', 'replace')
    _unicode_contents = u"\u2600 \u2601 \u2614"
    _encoding = 'cp932'
    
    def test_birthday(self):
        symbol = e4u.get("511")
        self.assertEqual(symbol.docomo.unicode, u"\uE686")
        self.assertEqual(symbol.kddi.unicode, u"\uE5A0")
        self.assertEqual(symbol.softbank.unicode, u"\uE34B")
        
        for s in e4u._loader.symbols:
            if s.unicode.unicode == u"\uE5A0":
                print "found"
class SoftBankTestCase(unittest.TestCase, TestCaseAbstract):
    _carrier = 'softbank'
    _carrier_contents = u"\uE04A \uE049 \uE04B"
    _unicode_contents = u"\u2600 \u2601 \u2614"
    _encoding = None
    
    def test_conversion(self):
        pass
if __name__ == '__main__':
    e4u.load()
    unittest.main()
