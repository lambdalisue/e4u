#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:    alisue
# Date:        2011/03/25
#
from utils import get_range_from_code

def get_stored_thumbnail_urls(carrier, base_url=r"/image/emoji/%s/%s.gif"):
    if not carrier.code:
        return None
    urls = []
    for code in carrier.code.split('+'):
        urls.append(base_url%(carrier._name, code.upper()))
    return urls

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
def get_docomo_thumbnail_urls(docomo, base_url=r"http://www.nttdocomo.co.jp/service/imode/make/content/pictograph/%s/images/%d.gif"):
    if not docomo.code:
        return None
    urls = []
    for code in docomo.code.split('+'):
        code = int(code, 16)
        if code >= 0xE70C:
            category = 'extention'
        else:
            category = 'basic'
        range = get_range_from_code(code, _code_to_docomo_id_ranges)
        offset = code - range[0]
        number = range[2] + offset
        urls.append(base_url % (category, number))
    return urls

def get_kddi_thumbnail_urls(kddi, base_url = r"http://mail.google.com/mail/e/ezweb_ne_jp/%s"):
    if not kddi.code:
        return None
    return [base_url % kddi._id]

_code_to_sjis_code_ranges = (
    (0xE001, 0xE05A, 0xF941, 0xF99B),
    (0xE101, 0xE15A, 0xF741, 0xF79B),
    (0xE201, 0xE25A, 0xF7A1, 0xF7FA),
    (0xE301, 0xE34D, 0xF9A1, 0xF9ED),
    (0xE401, 0xE44C, 0xFB41, 0xFB8D),
    (0xE501, 0xE53E, 0xFBA1, 0xFBDE),
)
# SoftBank may refuse access image from external so the code below may not work.
def get_softbank_thumbnail_urls(softbank, base_url = u"http://creation.mb.softbank.jp/web/img/%04X/%04X_20.gif"):
    if not softbank.code:
        return None
    urls = []
    for code in softbank.code.split('+'):
        code = int(code, 16)
        range = get_range_from_code(code, _code_to_sjis_code_ranges)
        urls.append(base_url % (range[0], code))
    return urls
