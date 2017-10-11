import string
import unittest

import linguafilter.ipa_mappings as mappings

class TestOrder(unittest.TestCase):
    def test_base_map_order(self):
        for key in mappings.BASE_MAP:
            self.assertEqual(key[1:], tuple(sorted(key[1:])))

    def test_mod_map_order(self):
        for key in mappings.MOD_MAP:
            self.assertEqual(key, tuple(sorted(key)))

class TestFormat(unittest.TestCase):
    def test_base_map_format(self):
        for key in mappings.BASE_MAP:
            val = mappings.BASE_MAP[key]

            # test html
            html = val['html']
            all(c in string.printable for c in html)
            self.assertTrue(len(html)==1 or len(html)==8 or len(html)==16)
            if len(html) != 1:
                self.assertEqual(html[:3], '&#x')
                try:
                    int(html[3:7], 16)
                except:
                    self.fail('invalid hexidecimal value: ' + html[3:7])
                self.assertEqual(html[7], ';')
                if len(html) == 16:
                    self.assertEqual(html[8:11], '&#x')
                    try:
                        int(html[11:15], 16)
                    except:
                        self.fail('invalid hexidecimal value: ' + html[11:15])
                    self.assertEqual(html[15], ';')

            # test latex
            latex = val['latex']
            all(c in string.printable for c in latex)

    def test_mod_map_format(self):
        for key in mappings.MOD_MAP:
            val = mappings.MOD_MAP[key]

            # test html
            html = val['html']('a')
            all(c in string.printable for c in html)
            self.assertEqual(len(html), 9)
            self.assertEqual(html[0], 'a')
            self.assertEqual(html[1:4], '&#x')
            try:
                int(html[4:-1], 16)
            except:
                self.fail('invalid hexidecimal value: ' + val['html'][4:-1])
            self.assertEqual(html[8], ';')

            # test latex
            latex = val['latex']('a')
            all(c in string.printable for c in latex)
