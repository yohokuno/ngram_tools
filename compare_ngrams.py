#!/usr/bin/env python3
import argparse
import ngram_tools


def compare_ngrams(target, baseline):
    dictionary = {}
    for ngram, freq in baseline:
        ngram = [(source.lower(), target.lower()) for source, target in ngram]
        dictionary[tuple(ngram)] = freq

    ratio_ngrams = []

    for ngram, freq in target:
        ngram = [(source.lower(), target.lower()) for source, target in ngram]
        if tuple(ngram) in dictionary:
            freq_baseline = dictionary[tuple(ngram)]
            ratio_ngrams.append([ngram, freq / freq_baseline])

    return ratio_ngrams


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('baseline')
    parser.add_argument('--size', type=int, default=1000000)
    args = parser.parse_args()

    target = ngram_tools.parse_ngrams(open(args.target))
    baseline = ngram_tools.parse_ngrams(open(args.baseline))
    ratio_ngrams = compare_ngrams(target, baseline)

    ngram_tools.print_ngrams(ngram_tools.prune_ngrams(ratio_ngrams, args.size))

if __name__ == '__main__':
    main()

