#!/usr/bin/env python3
import sys
import ngram_tools


def main():
    ngrams = ngram_tools.parse_ngrams(sys.stdin)
    ngrams = ngram_tools.sort_ngrams(ngrams)
    ngram_tools.print_ngrams(ngrams)

if __name__ == '__main__':
    main()

