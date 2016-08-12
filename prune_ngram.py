#!/usr/bin/env python3
import sys
import argparse
import ngram_tools


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('size', type=int)
    args = parser.parse_args()

    ngrams = ngram_tools.parse_ngrams(sys.stdin)
    ngrams = ngram_tools.prune_ngrams(ngrams, args.size)
    ngram_tools.print_ngrams(ngrams, sys.stdout)

if __name__ == '__main__':
    main()

