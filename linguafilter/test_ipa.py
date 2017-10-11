import unittest

import linguafilter.ipa as ipa

Seg = ipa.Segment

class TestTokenize(unittest.TestCase):
    def test_simple_char(self):
        self.assertEqual(ipa.tokenize('a'), ['a'])
        self.assertEqual(ipa.tokenize('T'), ['T'])
        self.assertEqual(ipa.tokenize('6'), ['6'])
        self.assertEqual(ipa.tokenize('@'), ['@'])

    def test_simple_chars(self):
        actual = ipa.tokenize('abc9de0f@T6GMTqR')
        expected = ['a', 'b', 'c', '9', 'd', 'e', '0', 'f', '@', 'T', '6', 'G', 'M', 'T', 'q', 'R']
        self.assertEqual(actual, expected)

    def test_backslash_char(self):
        self.assertEqual(ipa.tokenize('r\\'), ['r\\'])
        self.assertEqual(ipa.tokenize('B\\'), ['B\\'])
        self.assertEqual(ipa.tokenize('3\\'), ['3\\'])
        self.assertEqual(ipa.tokenize('@\\'), ['@\\'])
        self.assertEqual(ipa.tokenize('<\\'), ['<\\'])
        self.assertEqual(ipa.tokenize('>\\'), ['>\\'])
        self.assertEqual(ipa.tokenize('=\\'), ['=\\'])
        self.assertEqual(ipa.tokenize('_\\'), ['_\\'])

    def test_slash_at_beginning_errors(self):
        with self.assertRaises(Exception):
            ipa.tokenize('\\')
        with self.assertRaises(Exception):
            ipa.tokenize('\\abcdef')

    def test_long_string(self):
        actual = ipa.tokenize('r\\bcde_\\_tgmr\\')
        expected = ['r\\', 'b', 'c', 'd', 'e', '_\\', '_', 't', 'g', 'm', 'r\\']
        self.assertEqual(actual, expected)

class TestProcessChars(unittest.TestCase):
    def test_simple_char(self):
        self.assertEqual(ipa.process_chars(['a']), [Seg('a')])
        self.assertEqual(ipa.process_chars(['T']), [Seg('T')])
        self.assertEqual(ipa.process_chars(['6']), [Seg('6')])
        self.assertEqual(ipa.process_chars(['@']), [Seg('@')])

    def test_single_chars_with_modifiers(self):
        self.assertEqual(ipa.process_chars(['a', '\'']), [Seg('a', ['\''])])
        self.assertEqual(ipa.process_chars(['a', '=']), [Seg('a', ['='])])
        self.assertEqual(ipa.process_chars(['a', '`']), [Seg('a', ['`'])])
        self.assertEqual(ipa.process_chars(['a', '~']), [Seg('a', ['~'])])

        self.assertEqual(ipa.process_chars(['a', '_', 'G']), [Seg('a', ['G'])])
        self.assertEqual(ipa.process_chars(['a', '_', '=']), [Seg('a', ['='])])
        self.assertEqual(ipa.process_chars(['a', '_', 'H', '_', 'T']), [Seg('a', ['H', 'T'])])

    def test_equivalent_chars(self):
        self.assertEqual(ipa.process_chars(['P']), [Seg('v\\')])
        self.assertEqual(ipa.process_chars(['v\\']), [Seg('v\\')])
        self.assertEqual(ipa.process_chars(['a', '_', 'j']), [Seg('a', ['\''])])
        self.assertEqual(ipa.process_chars(['a', '\'']), [Seg('a', ['\''])])

    def test_long_sequences(self):
        seq = ['r\\', '_', 'G', '\'', 'a', 'a', '~']
        expected = [Seg('r\\', ['G', '\'']), Seg('a'), Seg('a', ['~'])]
        self.assertEqual(ipa.process_chars(seq), expected)

    def test_mod_char_first(self):
        with self.assertRaisesRegex(Exception, 'modifier characters must appear after a base character'):
            ipa.process_chars(['\''])
        with self.assertRaisesRegex(Exception, 'modifier characters must appear after a base character'):
            ipa.process_chars(['='])
        with self.assertRaisesRegex(Exception, 'modifier characters must appear after a base character'):
            ipa.process_chars(['`'])
        with self.assertRaisesRegex(Exception, 'modifier characters must appear after a base character'):
            ipa.process_chars(['~'])

    def test_underscores_in_wrong_positions(self):
        with self.assertRaisesRegex(Exception, 'underscore characters must appear after a base character'):
            ipa.process_chars(['_'])
        with self.assertRaisesRegex(Exception, 'underscore characters must appear after a base character'):
            ipa.process_chars(['_', '_'])
        with self.assertRaisesRegex(Exception, 'two underscore characters cannot appear next to each other'):
            ipa.process_chars(['a', '_', '_'])
        with self.assertRaisesRegex(Exception, 'dangling modifier character'):
            ipa.process_chars(['a', '_'])
        with self.assertRaisesRegex(Exception, 'two underscore characters cannot appear next to each other'):
            ipa.process_chars(['a', '_', '_', 'a'])
        with self.assertRaisesRegex(Exception, 'underscore characters must appear after a base character'):
            ipa.process_chars(['_', '_', 'a'])

class TestRemoveMods(unittest.TestCase):
    def test_no_mods_nothing_to_remove(self):
        self.assertEqual(ipa.remove_mods([], []), [])

    def test_one_mod_nothing_to_remove(self):
        self.assertEqual(ipa.remove_mods(['='], []), ['='])

    def test_one_mod_one_mod_to_remove(self):
        self.assertEqual(ipa.remove_mods(['='], ['=']), [])

    def test_two_mods_one_mod_to_remove(self):
        self.assertEqual(ipa.remove_mods(['=', '`'], ['=']), ['`'])

class TestReduceMods(unittest.TestCase):
    def test_no_mods(self):
        self._assertModFuncsEqual(ipa.reduce_mods([]), [])

    def test_one_mod(self):
        self._assertModFuncsEqual(ipa.reduce_mods(['=']), ['a&#x0329;'])

    def test_two_mods(self):
        self._assertModFuncsEqual(ipa.reduce_mods(['=', 'd']), ['a&#x0329;', 'a&#x032A;'])

    def test_combining_mods(self):
        # TODO: once H_T is supported, uncomment
        # self._assertModFuncsEqual(ipa.reduce_mods(['H', 'T']), ['a&#x1DC4;'])
        pass

    def test_combining_mods_plus_others(self):
        # TODO: once H_T is supported, uncomment
        # self._assertModFuncsEqual(ipa.reduce_mods(['=', 'H', 'T']), ['a&#x1DC4;', 'a&#x0329;'])
        pass

    def _assertModFuncsEqual(self, funcs, results):
        self.assertEqual(len(funcs), len(results))
        for i in range(len(funcs)):
            self.assertEqual(funcs[i]('a'), results[i])

class TestReduceSeg(unittest.TestCase):
    def test_no_mods(self):
        self.assertEqual(ipa.reduce_seg(Seg('a')), ('a', []))

    def test_one_mod_no_reduction(self):
        self.assertEqual(ipa.reduce_seg(Seg('a', ['='])), ('a', ['=']))

    def test_one_mod_reduction(self):
        self.assertEqual(ipa.reduce_seg(Seg('r', ['`'])), ('&#x027D;', []))

    def test_multiple_mods_no_reduction(self):
        self.assertEqual(ipa.reduce_seg(Seg('r', ['=', 'G'])), ('r', ['=', 'G']))

    def test_multiple_mods_reduction(self):
        self.assertEqual(ipa.reduce_seg(Seg('r', ['=', '`'])), ('&#x027D;', ['=']))
        # no actual cases where two mods reduce into the base yet

class TestGetCombos(unittest.TestCase):
    def test_single_element(self):
        self.assertEqual(ipa.get_combos([1]), [[1], []])

    def test_two_elements(self):
        self.assertEqual(ipa.get_combos([1, 2]), [[1, 2], [1], [2], []])

    def test_three_elements(self):
        self.assertEqual(ipa.get_combos([1, 2, 3]), [[1,2,3],[1,2],[1,3],[2,3],[1],[2],[3],[]])