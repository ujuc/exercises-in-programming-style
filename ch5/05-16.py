#!/usr/bin/env python2
# coding: utf-8

# 자기 관찰
# 제약조건
# 1. 문제를 어떤 추상 형태(프로시저 함수, 객체 등)을 사용해 분해한다.
# 2. 해당 추상화에서는 그 자신과 다른 것에 관한 정보를 변경할 수는 없지만 그 정보에 접근할 수는 있다.

import sys
import re
import operator
import string
import inspect


def read_stop_words():
    """
    This function can only be called from a function named extract_words
    :return:
    """
    # 메타 수준 테이터: inspect.stack()
    if inspect.stack()[1][3] != 'extract_words':
        return None

    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    return stop_words


def extract_words(path_to_file):
    # 메타 수준 데이터: locals()
    with open(locals()['path_to_file']) as f:
        str_data = f.read()

    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()
    stop_words = read_stop_words()
    return [w for w in word_list if not w in stop_words]


def frequencies(word_list):
    # 메타 수준 데이터: locals()
    word_freqs = {}
    for w in locals()['word_list']:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs


def sort(word_freq):
    # 메타 수준 데이터: locals()
    return sorted(locals()['word_freq'].iteritems(), key=operator.itemgetter(1),
                  reverse=True)


def main():
    word_freqs = sort(frequencies(extract_words(sys.argv[1])))
    for (w, c) in word_freqs[0:25]:
        print '{} - {}'.format(w, c)


if __name__ == "__main__":
    main()
