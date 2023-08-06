# -*- coding: utf-8 -*-
u"""Write to stdout without causing UnicodeEncodeError."""

from __future__ import absolute_import
import sys


if (getattr(sys.stdout, u'errors', u'') == u'strict' and
        not getattr(sys.stdout, u'encoding', u'').lower().startswith(u'utf')):
    try:
        import translit
        sys.stdout = translit.StreamFilter(sys.stdout)
    except ImportError:
        import codecs
        import unicodedata
        import warnings

        TRANSLIT_MAP = {
            0x2018: u"'",
            0x2019: u"'",
            0x201c: u'"',
            0x201d: u'"',
        }

        def simplify(s):
            s = s.translate(TRANSLIT_MAP)
            return u''.join([c for c in unicodedata.normalize(u'NFKD', s)
                            if not unicodedata.combining(c)])

        def simple_translit_error_handler(error):
            if not isinstance(error, UnicodeEncodeError):
                raise error
            chunk = error.object[error.start:error.end]
            repl = simplify(chunk)
            repl = (repl.encode(error.encoding, u'backslashreplace')
                    .decode(error.encoding))
            return repl, error.end

        class SimpleTranslitStreamFilter(object):

            u"""Filter a stream through simple transliteration."""
            errors = u'simple_translit'

            def __init__(self, target):
                self.target = target

            def __getattr__(self, name):
                return getattr(self.target, name)

            def write(self, s):
                self.target.write(self.downgrade(s))

            def writelines(self, lines):
                self.target.writelines(
                    [self.downgrade(line) for line in lines])

            def downgrade(self, s):
                return (s.encode(self.target.encoding, self.errors)
                        .decode(self.target.encoding))

        codecs.register_error(SimpleTranslitStreamFilter.errors,
                              simple_translit_error_handler)
        sys.stdout = SimpleTranslitStreamFilter(sys.stdout)
        warnings.warn(u'translit is unavailable', ImportWarning)
