``e4u`` library is bundle library for `emoji4unicode <https://github.com/googlei18n/emoji4unicode/>`_

it is for handling unicode emoji and carrier's emoji. the main feature is

+	Conversion unicode emoji to carrier's emoji
+	Conversion carrier's emoji to unicode emoji

The unicode emoji which this library can handle is described on http://www.unicode.org/~scherer/emoji4unicode/snapshot/full.html

This library referred to source code of emoji4unicode and `django-bpmobile <https://bitbucket.org/tokibito/django-bpmobile>`_


Install
=================================================
::

	sudo pip install e4u

or::

	sudo pip install git+git://github.com/lambdalisue/e4u.git#egg=e4u


Required (Automatically installed)
=================================================
+ BeautifulSoup (for analysis carrier's Web site and emoji4unicode.xml)


How to use
=================================================
This library use ``emoji4unicode.xml`` to create conversion table of emoji.
So you have to load it from filesystem or Internet. ``e4u.load()`` method
load it from google code's trunk url and recommended. if you cannot connect
to internet, use ``e4u.load(file=r"some/path/emoji4unicode.xml")`` insted. The
``emoji4unicode.xml`` is found on https://github.com/googlei18n/emoji4unicode/blob/master/data/emoji4unicode.xml

Once you load ``emoji4unicode.xml``, you can translate emoji with ``e4u.translate()`` method.
To translate carrier's emoji to unicode emoji, use the method like ``contents = e4u.translate(contents, **e4u.DOCOMO_TRANSLATE_PROFILE)``
To translate unicode emoji to carrier's emoji, use the method like ``contents = e4u.translate(contents, reverse=True, **e4u.DOCOMO_TRANSLATE_PROFILE)``

The code below describe how to use the library.::

	import e4u
	e4u.load()
	carrier_contents = "\xF8\x9F \xF8\xA0 \xF8\xA1"		# Sun, Cloud, Rain in DoCoMo emoji
	unicode_contents = u"\u2600 \u2601 \u2614"			# Sun, Cloud, Rain in Unicode emoji
	
	# DoCoMo => Unicode
	contents = carrier_contents
	expected = unicode_contents
	# Translate emoji with DoCoMo profile (= {'carrier':'docomo', 'encoding':'cp932'})
	result = e4u.translate(contents, **e4u.DOCOMO_TRANSLATE_PROFILE)
	
	assert isinstance(result, unicode)		# return value is Unicode
	assert result == expected 
	
	# Unicode => DoCoMo
	contents = unicode_contents
	expected = carrier_contents
	# Translate emoji with DoCoMo profile with reverse=True
	result = e4u.translate(contents, reverse=True, **e4u.DOCOMO_TRANSLATE_PROFILE)
	
	assert isinstance(result, unicode)		# return value is Unicode
	assert result.encode('cp932', 'replace') == expected

Supported carriers
==================================================
Currently only DoCoMo, KDDI, SoftBank and Google is supported. the carrier name which you can pass to 
the ``e4u.translate()`` method is

+	text			- to text
+	docomo_img		- to img tag using DoCoMo emoji
+	kddi_img		- to img tag using KDDI emoji (recommended for PC or other device which doesn't support emoji)
+	softbank_img	- to img tag using SoftBank emoji (not recommended, SoftBank may reject access from external so doesn't work)
+	google			- to GMail emoji. I have no idea how can I use it but in case.
+	docomo			- to DoCoMo emoji. SJIS format (decoded as unicode)
+	kddi			- to KDDI emoji. SJIS format (decoded as unicode)
+	softbank		- to SoftBank emoji. Unicode format

Methods
==================================================

``e4u.load(filename=None, url=r"https://raw.githubusercontent.com/googlei18n/emoji4unicode/master/data/emoji4unicode.xml", loader_class=loader.Loader)``
    to load emoji4unicode.xml and build internal conversion table. this method never affect twice. use ``e4u.reload()`` insted to reloading library.

``e4u.reload(filename=None, url=r"https://raw.githubusercontent.com/googlei18n/emoji4unicode/master/data/emoji4unicode.xml", loader_class=loader.Loader)``
    force to reload emoji4unicode.xml, use ``e4u.load()`` method insted for general use.

``e4u.has_loaded()``
    return True if the ``e4u.load()`` method has called. use ``e4u.load()`` method insted for general use. never do like below::

        # stupid way
        import e4u
        if not e4u.has_loaded():
            e4u.reload()

        # smarter
        import e4u
        e4u.load()

``e4u.get(id)``
    get emoji symbol instance for the id. the id is described on http://www.unicode.org/~scherer/emoji4unicode/snapshot/full.html
    strip 'e-' from ID like '000' for 'e-000' and pass as unicode format.

``e4u.translate(source, carrier, reverse=False, encoding=None)``
    translate unicode emoji contained in source to carrier's emoji or reverse.

``e4u.translate_char(source_char, carrier, reverse=False, encoding=None)``
    translate unicode emoji char to carrier's emoji char. faster than ``e4u.translate()``
    method but cannot handle text. use it for letter conversion. 
