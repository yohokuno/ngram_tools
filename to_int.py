#!/usr/bin/env python3
import sys
import argparse
import ngram_tools


def to_int(ngrams):
    for ngram, prob in ngrams:
        freq = int(prob)
        if freq == 0:
            freq = 1
        yield ngram, freq


def scale_ngrams(ngrams, scale):
    for ngram, freq in ngrams:
        yield ngram, freq * scale


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('scale', type=float)
    args = parser.parse_args()

    ngrams = ngram_tools.parse_ngrams_float(sys.stdin)
    ngrams = scale_ngrams(ngrams, args.scale)
    ngrams = to_int(ngrams)
    ngram_tools.print_ngrams(ngrams, sys.stdout)


if __name__ == '__main__':
    main()

