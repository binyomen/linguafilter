import panflute as pf
import unittest

import linguafilter.phonrule as phonrule
import linguafilter.test_common as common

class TestParse(unittest.TestCase):
    def test_valid_content_strs(self):
        doc = common.MockDoc('html')
        span = pf.Span(pf.Str('a'), pf.Str('b'), pf.Str('c'), pf.Str('d'), classes=['phonrule'])
        phonrule.parse(span, doc)
        self.assertEqual(pf.stringify(span), 'a -&gt; b/c_d')

    def test_valid_content_spans(self):
        doc = common.MockDoc('html')
        span1 = pf.Span(pf.Str('a'))
        span2 = pf.Span(pf.Str('b'))
        span3 = pf.Span(pf.Str('c'))
        span4 = pf.Span(pf.Str('d'))
        span = pf.Span(span1, span2, span3, span4, classes=['phonrule'])
        phonrule.parse(span, doc)
        self.assertEqual(pf.stringify(span), 'a -&gt; b/c_d')

    def test_valid_content_strs_and_spans(self):
        doc = common.MockDoc('html')
        span1 = pf.Span(pf.Str('a'))
        str1 = pf.Str('b')
        span2 = pf.Span(pf.Str('c'))
        str2 = pf.Str('d')
        span = pf.Span(span1, str1, span2, str2, classes=['phonrule'])
        phonrule.parse(span, doc)
        self.assertEqual(pf.stringify(span), 'a -&gt; b/c_d')

    def test_valid_content_strs_and_spans_latex(self):
        doc = common.MockDoc('latex')
        span1 = pf.Span(pf.Str('a'))
        str1 = pf.Str('b')
        span2 = pf.Span(pf.Str('c'))
        str2 = pf.Str('d')
        span = pf.Span(span1, str1, span2, str2, classes=['phonrule'])
        phonrule.parse(span, doc)
        self.assertEqual(pf.stringify(span), '\\phonb{a}{b}{c}{d}')

    def test_invalid_content(self):
        doc = common.MockDoc('html')

        span = pf.Span(classes=['phonrule'])
        with self.assertRaisesRegexp(Exception, 'invalid phonrule syntax'):
            phonrule.parse(span, doc)

        span = pf.Span(pf.Str('a'), pf.Str('b'), classes=['phonrule'])
        with self.assertRaisesRegexp(Exception, 'invalid phonrule syntax'):
            phonrule.parse(span, doc)

        span = pf.Span(pf.Str('a'), pf.Str('b'), pf.Str('c'), pf.Str('d'), pf.Str('e'), classes=['phonrule'])
        with self.assertRaisesRegexp(Exception, 'invalid phonrule syntax'):
            phonrule.parse(span, doc)
