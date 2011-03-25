#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Alisue
# Last Change:  25-Mar-2011.
#
from urllib import urlopen
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup
import os

DOWNLOAD_THUMBNAILS = True

def fetch_docomo_codes():
    url = r"http://www.nttdocomo.co.jp/service/imode/make/content/pictograph/%s/index.html"
    codes = []
    def _fetch(url, codes):
        soup = BeautifulSoup(urlopen(url).read())
        for i, tr in enumerate(soup.find("table")("tr")[2:]):
            td = tr("td")
            sjis = int(td[2].find("span").string, 16)
            unic = int(td[4].find("span").string, 16)
            img = urljoin(url, td[1].find("img")['src'])
            codes.append((i+1, unic, sjis, img))
    _fetch(url%'basic', codes)
    _fetch(url%'extention', codes)
    return codes
def fetch_kddi_codes():
    # KDDI doesn't have official emoji table in HTML
    # And the site below doesn't have emoji data in 0xEB89 - 0xEB8E
    url = r"http://trialgoods.com/emoji/?career=au&page=all"
    
    codes = []
    soup = BeautifulSoup(urlopen(url).read())
    for i, tr in enumerate(soup.find("table")("tr")[3:-6]):
        td = tr("td")
        sjis = int(td[3].string, 16)
        unic = int(td[4].string, 16)
        img = urljoin(url, td[1].find("img")['src'])
        codes.append((i+1, unic, sjis, img))
    last = i + 1
    # Manually append lucked datas
    for offset in xrange(0xEB8E-0xEB88):
        sjis = 0xF48E + offset
        unic = 0xEB89 + offset
        codes.append((last+offset, unic, sjis, None))
    return codes

def fetch_softbank_codes():
    # SoftBank doesn't have id and sjis
    url = r"http://creation.mb.softbank.jp/web/web_pic_0%d.html"

    codes = []
    def _fetch(url, codes):
        soup = BeautifulSoup(urlopen(url).read())
        tables = soup("table", cellspacing="1", cellpadding="2", border="0", width="100%")
        for table in tables:
            for tr in table("tr")[1:]:
                td = tr("td")
                unic = int(td[1].string, 16)
                img = urljoin(url, td[0].find("img")['src'])
                codes.append((None, unic, None, img))
    for i in xrange(1, 6):
        _fetch(url%i, codes)
    return codes

def make_ranges(codes, a, b):
    ranges = []
    # Sort codes with unic cols
    codes.sort(key=lambda x: x[a])
    # Create ranges
    start_a = codes[0][a]
    start_b = codes[0][b]
    prev_a = start_a
    prev_b = start_b
    for code in codes[1:]:
        offset_a = code[a] - start_a
        offset_b = code[b] - start_b
        
        if offset_a != offset_b:
            ranges.append((start_a, prev_a, start_b, prev_b))
            start_a = code[a]
            start_b = code[b]
        prev_a = code[a]
        prev_b = code[b]
    ranges.append((start_a, prev_a, start_b, prev_b))
    return ranges

def download_thumbnails(prefix, codes, U=1, I=3):
    if not os.path.exists(prefix):
        os.makedirs(prefix)
    for code in codes:
        unic = code[U]
        img = code[I]
        if img is None:
            continue
        filename = os.path.join(prefix, "%04X.gif"%unic)
        if os.path.exists(filename):
            print "... skip %s" % img
            continue
        print "... %s" % img
        local_file = open(filename, "wb")
        local_file.write(urlopen(img).read())
        local_file.close()

def print_ranges(ranges):
    for r in ranges:
        print "(0x%04X, 0x%04X, 0x%04X, 0x%04X)," % r

if __name__ == '__main__':
    N, U, S, I = 0, 1, 2, 3

    # DoCoMo
    docomo_codes = fetch_docomo_codes()
    docomo_unicode_to_sjis_ranges = make_ranges(docomo_codes, U, S)
    print "unicode => sjis (DoCoMo)"
    print_ranges(docomo_unicode_to_sjis_ranges)
    print

    docomo_sjis_to_id_ranges = make_ranges(docomo_codes, S, N)
    print "sjis => id (DoCoMo)"
    print_ranges(docomo_sjis_to_id_ranges)
    print

    docomo_unicode_to_id_ranges = make_ranges(docomo_codes, U, N)
    print "unicode => id (DoCoMo)"
    print_ranges(docomo_unicode_to_id_ranges)
    print

    # KDDI
    kddi_codes = fetch_kddi_codes()
    kddi_unicode_to_sjis_ranges = make_ranges(kddi_codes, U, S)
    print "unicode => sjis (KDDI)"
    print_ranges(kddi_unicode_to_sjis_ranges)
    print
    
    # SoftBank
    softbank_codes = fetch_softbank_codes()

    if DOWNLOAD_THUMBNAILS:
        import sys
        sys.stdout.flush()

        print "download thumbnails..."
        download_thumbnails('docomo', docomo_codes, U, I)
        print

        print "download thumbnails..."
        download_thumbnails('kddi', kddi_codes, U, I)
        print

        print "download thumbnails..."
        download_thumbnails('softbank', softbank_codes, U, I)
        print
