#!/usr/bin/env python3
import sys
import argparse
import ngram_tools


def diff_ngrams(ngrams, dictionary):
    targets = set(tuple(target for source, target in ngram) for ngram, freq in dictionary)

    for ngram, freq in ngrams:
        target = tuple(target for source, target in ngram)
        if not target in targets:
            yield ngram, freq


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ngrams')
    args = parser.parse_args()

    dictionary = ngram_tools.parse_ngrams(open(args.ngrams))
    ngrams = ngram_tools.parse_ngrams(sys.stdin)

    ngrams = diff_ngrams(ngrams, dictionary)
    ngram_tools.print_ngrams(ngrams)

if __name__ == '__main__':
    main()

