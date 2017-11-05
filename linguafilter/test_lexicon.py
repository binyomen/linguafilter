import os.path
import panflute as pf
import unittest

import linguafilter.lexicon as lexicon
import linguafilter.test_common as common

class TestGetConfig(unittest.TestCase):
    def test_defaults(self):
        config = lexicon.get_config({'file': 'file.csv'})
        self.assertEqual(config, {'file': 'file.csv', 'delimiter': ',', 'quote': '"', 'merge_root': False})

    def test_no_file(self):
        with self.assertRaisesRegexp(Exception, 'filename required'):
            lexicon.get_config({})

    def test_tab_delim(self):
        config = lexicon.get_config({'file': 'file.csv', 'delim': '\\t'})
        self.assertEqual(config, {'file': 'file.csv', 'delimiter': '\t', 'quote': '"', 'merge_root': False})

    def test_all_specified(self):
        config = lexicon.get_config({'file': 'file.csv', 'delim': '\t', 'quote': '|', 'merge_root': 'foo'})
        self.assertEqual(config, {'file': 'file.csv', 'delimiter': '\t', 'quote': '|', 'merge_root': True})

class TestReplaceFields(unittest.TestCase):
    def test_no_replacements(self):
        s = pf.Str('abcd')
        lexicon.replace_fields({}, s)
        self.assertEqual(s.text, 'abcd')

    def test_not_str(self):
        span = pf.Span(pf.Str('{field}'))
        lexicon.replace_fields({'field': 'value'}, span)
        self.assertEqual(span.content[0].text, '{field}')

    def test_one_replacement(self):
        s = pf.Str('{field}')
        lexicon.replace_fields({'field': 'value'}, s)
        self.assertEqual(s.text, 'value')

    def test_repeated_replacements(self):
        s = pf.Str('{field1}{field2}{field3}{field2}')
        lexicon.replace_fields({'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}, s)
        self.assertEqual(s.text, 'value1value2value3value2')

    def test_unused_replacements(self):
        s = pf.Str('{field1}{field2}')
        lexicon.replace_fields({'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}, s)
        self.assertEqual(s.text, 'value1value2')

    def test_nonexistant_replacements(self):
        s = pf.Str('{field1}{field2}{field3}')
        lexicon.replace_fields({'field1': 'value1', 'field3': 'value3'}, s)
        self.assertEqual(s.text, 'value1{field2}value3')

class TestParse(unittest.TestCase):
    def test_empty(self):
        doc = common.MockDoc('html')
        filename = os.path.join('linguafilter', 'test_lexicon.csv')
        div = pf.Div(attributes={'file': filename}, classes=['lexicon'])
        lexicon.parse(div, doc)
        self.assertEqual(pf.stringify(div), '')

    def test_single_line(self):
        doc = common.MockDoc('html')
        filename = os.path.join('linguafilter', 'test_lexicon.csv')
        attributes = {'file': filename}
        div = pf.Div(pf.Para(pf.Str('{field1}, {field2}, and {field3}')), attributes=attributes, classes=['lexicon'])
        lexicon.parse(div, doc)
        self.assertEqual(pf.stringify(div), 'r1f1, r1f2, and r1f3\n\nr2f1, r2f2, a field, and r2f3\n\nr3f1, r3f2, and r3f3\n\n')

    def test_merge_root_single_line(self):
        doc = common.MockDoc('html')
        filename = os.path.join('linguafilter', 'test_lexicon.csv')
        attributes = {'file': filename, 'merge_root': 'foo'}
        div = pf.Div(pf.Para(pf.Str('{field1}, {field2}, and {field3}')), attributes=attributes, classes=['lexicon'])
        lexicon.parse(div, doc)
        self.assertEqual(pf.stringify(div), 'r1f1, r1f2, and r1f3r2f1, r2f2, a field, and r2f3r3f1, r3f2, and r3f3\n\n')

    def test_merge_root_multiple_nodes(self):
        doc = common.MockDoc('html')
        filename = os.path.join('linguafilter', 'test_lexicon.csv')
        attributes = {'file': filename, 'merge_root': 'foo'}
        div = pf.Div(pf.Para(pf.Str('{field1}')), pf.Para(pf.Str('{field2}')), attributes=attributes, classes=['lexicon'])
        with self.assertRaisesRegexp(Exception, 'if merge_root is specified, there can be only one node under the lexicon div'):
            lexicon.parse(div, doc)
