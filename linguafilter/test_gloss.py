import panflute as pf
import unittest

import linguafilter.gloss as gloss
import linguafilter.test_common as common

class TestParse(unittest.TestCase):
    def test_valid_content_strs_html(self):
        doc = common.MockDoc('html')
        span = pf.Span(pf.Str('a'), pf.Str('b'), pf.Str('c'), classes=['gloss'])
        gloss.parse(span, doc)
        self.assertEqual(pf.stringify(span), 'a<br/>b<br/>c')

    def test_valid_content_spans_html(self):
        doc = common.MockDoc('html')
        span1 = pf.Span(pf.Str('a'))
        span2 = pf.Span(pf.Str('b'))
        span3 = pf.Span(pf.Str('c'))
        span = pf.Span(span1, span2, span3, classes=['gloss'])
        gloss.parse(span, doc)
        self.assertEqual(pf.stringify(span), 'a<br/>b<br/>c')

    def test_valid_content_strs_and_spans_html(self):
        doc = common.MockDoc('html')
        span1 = pf.Span(pf.Str('a'))
        str1 = pf.Str('b')
        span2 = pf.Span(pf.Str('c'))
        span = pf.Span(span1, str1, span2, classes=['gloss'])
        gloss.parse(span, doc)
        self.assertEqual(pf.stringify(span), 'a<br/>b<br/>c')

    def test_valid_content_strs_latex(self):
        doc = common.MockDoc('latex')
        span = pf.Span(pf.Str('a'), pf.Str('b'), pf.Str('c'), classes=['gloss'])
        gloss.parse(span, doc)
        self.assertEqual(pf.stringify(span), '\\begin{exe}\n\\ex\n\\gll a\\\\\nb\\\\\n\\trans c\n\\end{exe}')

    def test_valid_content_spans_latex(self):
        doc = common.MockDoc('latex')
        span1 = pf.Span(pf.Str('a'))
        span2 = pf.Span(pf.Str('b'))
        span3 = pf.Span(pf.Str('c'))
        span = pf.Span(span1, span2, span3, classes=['gloss'])
        gloss.parse(span, doc)
        self.assertEqual(pf.stringify(span), '\\begin{exe}\n\\ex\n\\gll a\\\\\nb\\\\\n\\trans c\n\\end{exe}')

    def test_valid_content_strs_and_spans_latex(self):
        doc = common.MockDoc('latex')
        span1 = pf.Span(pf.Str('a'))
        str1 = pf.Str('b')
        span2 = pf.Span(pf.Str('c'))
        span = pf.Span(span1, str1, span2, classes=['gloss'])
        gloss.parse(span, doc)
        self.assertEqual(pf.stringify(span), '\\begin{exe}\n\\ex\n\\gll a\\\\\nb\\\\\n\\trans c\n\\end{exe}')

    def test_invalid_content(self):
        doc = common.MockDoc('html')

        span = pf.Span(classes=['gloss'])
        with self.assertRaisesRegexp(Exception, 'invalid gloss syntax'):
            gloss.parse(span, doc)

        span = pf.Span(pf.Str('a'), pf.Str('b'), classes=['gloss'])
        with self.assertRaisesRegexp(Exception, 'invalid gloss syntax'):
            gloss.parse(span, doc)

        span = pf.Span(pf.Str('a'), pf.Str('b'), pf.Str('c'), pf.Str('d'), classes=['gloss'])
        with self.assertRaisesRegexp(Exception, 'invalid gloss syntax'):
            gloss.parse(span, doc)
