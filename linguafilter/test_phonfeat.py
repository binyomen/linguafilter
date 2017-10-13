import panflute as pf
import unittest

import linguafilter.phonfeat as phonfeat
import linguafilter.test_common as common

class TestParse(unittest.TestCase):
    def test_empty_html(self):
        doc = common.MockDoc('html')
        span = pf.Span(classes=['phonfeat'])
        phonfeat.parse(span, doc)
        self.assertEqual(pf.stringify(span), '[]')

    def test_one_str_html(self):
        doc = common.MockDoc('html')
        span = pf.Span(pf.Str('a'), classes=['phonfeat'])
        phonfeat.parse(span, doc)
        self.assertEqual(pf.stringify(span), '[a]')

    def test_two_strs_html(self):
        doc = common.MockDoc('html')
        span = pf.Span(pf.Str('a'), pf.Str('b'), classes=['phonfeat'])
        phonfeat.parse(span, doc)
        self.assertEqual(pf.stringify(span), '[a, b]')

    def test_three_strs_html(self):
        doc = common.MockDoc('html')
        span = pf.Span(pf.Str('a'), pf.Str('b'), pf.Str('c'), classes=['phonfeat'])
        phonfeat.parse(span, doc)
        self.assertEqual(pf.stringify(span), '[a, b, c]')

    def test_empty_latex(self):
        doc = common.MockDoc('latex')
        span = pf.Span(classes=['phonfeat'])
        phonfeat.parse(span, doc)
        self.assertEqual(pf.stringify(span), '\\phonfeat{}')

    def test_one_str_latex(self):
        doc = common.MockDoc('latex')
        span = pf.Span(pf.Str('a'), classes=['phonfeat'])
        phonfeat.parse(span, doc)
        self.assertEqual(pf.stringify(span), '\\phonfeat{a}')

    def test_two_strs_latex(self):
        doc = common.MockDoc('latex')
        span = pf.Span(pf.Str('a'), pf.Str('b'), classes=['phonfeat'])
        phonfeat.parse(span, doc)
        self.assertEqual(pf.stringify(span), '\\phonfeat{a \\\\ b}')

    def test_three_strs_latex(self):
        doc = common.MockDoc('latex')
        span = pf.Span(pf.Str('a'), pf.Str('b'), pf.Str('c'), classes=['phonfeat'])
        phonfeat.parse(span, doc)
        self.assertEqual(pf.stringify(span), '\\phonfeat{a \\\\ b \\\\ c}')
