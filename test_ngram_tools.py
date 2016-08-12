#!/usr/bin/env python3
import unittest
import io
import ngram_tools


class Test(unittest.TestCase):
    def test_parse_ngrams(self):
        lines = ['^ a➾A 1\n']
        actual = list(ngram_tools.parse_ngrams(lines))
        expected = [([('^','^'),('a','A')],1)]
        self.assertEqual(actual, expected)

    def test_parse_ngrams_float(self):
        lines = ['^ a➾A 1.0\n']
        actual = list(ngram_tools.parse_ngrams_float(lines))
        expected = [([('^','^'),('a','A')],1.0)]
        self.assertEqual(actual, expected)

    def test_print_ngrams(self):
        fout = io.StringIO()
        ngrams = [([('^','^'),('a','A')],1)]
        ngram_tools.print_ngrams(ngrams, fout)
        expected = '^ a➾A 1\n'
        self.assertEqual(fout.getvalue(), expected)

    def test_reverse_ngrams(self):
        ngrams = [([('^', '^'),('a','A')],1)]
        actual = list(ngram_tools.reverse_ngrams(ngrams))
        expected = [([('^','^'),('A','a')],1)]
        self.assertEqual(actual, expected)

    def test_cutoff_ngrams(self):
        ngrams = [('a',2),('b',5),('c',3)]
        actual = list(ngram_tools.cutoff_ngrams(ngrams,3))
        expected = [('b',5),('c',3)]
        self.assertEqual(actual, expected)

    def test_prune_ngrams(self):
        ngrams = [('c',1),('a',3),('b',2)]
        actual = list(ngram_tools.prune_ngrams(ngrams,2))
        expected = [('a',3),('b',2)]
        self.assertEqual(actual, expected)

    def test_restrict_order(self):
        ngrams = [(['a'],2),(['b','c'],1)]
        actual = list(ngram_tools.restrict_order(ngrams,1))
        expected = [(['a'],2)]
        self.assertEqual(actual, expected)

    def test_drop_source(self):
        ngrams = [([('a','A')],1)]
        actual = list(ngram_tools.drop_source(ngrams))
        expected = [([('A','A')],1)]
        self.assertEqual(actual, expected)

    def test_filter_ngrams(self):
        ngrams = [([('','あ')],1), ([('','A')],1)]
        actual = list(ngram_tools.filter_ngrams(ngrams))
        expected = [([('','あ')],1)]
        self.assertEqual(actual, expected)

    def test_expand_ngram(self):
        def mock_expander(word):
            return [('a',1.0), ('b',2.0)]
        ngram = ['A']
        actual = list(ngram_tools.expand_ngram(ngram, mock_expander))
        expected = [(['a',],1.0), (['b'],2.0)]
        self.assertEqual(actual, expected)

    def test_expand_ngrams(self):
        def mock_expander(word):
            return [('a',1.0), ('b',2.0)]
        ngrams = [(['A'], 2)]
        actual = list(ngram_tools.expand_ngrams(ngrams, mock_expander))
        expected = [(['a'],2), (['b'],4)]
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()

