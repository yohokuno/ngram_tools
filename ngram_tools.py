#!/usr/bin/env python3
import sys
import re
import heapq
import functools


# Basic parsers
def parse_word(word):
    pair = word.split('➾', 1)
    if len(pair) == 2:
        source, target = pair
        return source, target
    else:
        return word, word


def parse_ngrams(lines):
    for line in lines:
        try:
            line = line.rstrip('\n')
            *ngram, freq = line.split(' ')
            ngram = list(map(parse_word, ngram))
            freq = int(freq)
            yield ngram, freq
        except ValueError:
            print('Invalid ngram format: {}'.format(line), file=sys.stderr)


def parse_ngrams_float(lines):
    for line in lines:
        line = line.rstrip(' \n')
        *ngram, freq = line.split(' ')
        ngram = list(map(parse_word, ngram))
        freq = float(freq)
        yield ngram, freq


def unparse_word(word):
    source, target = word
    if source == target:
        return source
    return source + '➾' + target


def unparse_ngram(ngram):
    return ' '.join(map(unparse_word, ngram))


def print_ngrams(ngrams, fout=sys.stdout):
    for ngram, freq in ngrams:
        line = unparse_ngram(ngram) + ' ' + str(freq)
        print(line, file=fout)


# Basic operations
def reverse_ngrams(ngrams):
    for ngram, freq in ngrams:
        ngram = list((target, source) for source, target in ngram)
        yield ngram, freq


def cutoff_ngrams(ngrams, threshold):
    for ngram, freq in ngrams:
        if freq >= threshold:
            yield ngram, freq


def compare_ngrams(pair1, pair2):
    ngram1, freq1 = pair1
    ngram2, freq2 = pair2
    if freq1 != freq2:
        return freq1 - freq2
    if ngram1 > ngram2:
        return -1
    return 1


key_ngrams = functools.cmp_to_key(compare_ngrams)


def prune_ngrams(ngrams, size):
    return heapq.nlargest(size, ngrams, key=key_ngrams)


def sort_ngrams(ngrams):
    return sorted(ngrams, key=key_ngrams, reverse=True)


def restrict_order(ngrams, order):
    for ngram, freq in ngrams:
        if len(ngram) <= order:
            yield ngram, freq


def drop_source(ngrams):
    for ngram, freq in ngrams:
        ngram = list((target, target) for source, target in ngram)
        yield ngram, freq


def filter_ngrams(ngrams):
    target_expression = '^[ぁ-ゔァ-ヶーｧ-ﾝ々。、．，！？（）「」【】『』…□■ .,!?()\u2600-\u26FF\u4E00-\u9FCC^]+$'
    target_pattern = re.compile(target_expression)

    def is_valid(ngram):
        for source, target in ngram:
            if not target_pattern.match(target):
                return False
        return True

    for ngram, freq in ngrams:
        if is_valid(ngram):
            yield ngram, freq


def expand_ngram(ngram, expander):
    if not ngram:
        yield [], 1.
    else:
        first, *rest = ngram
        first_expand = list(expander(first))
        rest_expand = expand_ngram(rest, expander)

        for rest_ngram, rest_prob in rest_expand:
            for first_word, first_prob in first_expand:
                current_ngram = [first_word] + rest_ngram
                current_prob = first_prob * rest_prob
                yield current_ngram, current_prob


def expand_ngrams(ngrams, expander):
    for ngram, freq in ngrams:
        expanded = expand_ngram(ngram, expander)
        for joint, weight in expanded:
            new_freq = int(freq * weight)
            if new_freq == 0:
                new_freq = 1
            yield joint, new_freq
