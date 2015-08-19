#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 앞으로 차기
# 제약조건
# 1. 각 함수에서는 추가 매개변수를 취하는데, 맨 마지막 매개변수는 일반적으로 다른 함수다.
# 2. 현재 함수 처리 마지막에 그 함수 매개변수를 적용힌다.
# 3. 현재 함수 출력을 그 함수 매개변수의 입력으로 사용한다.
# 4. 규모가 큰 문제를 함수의 파이프라인으로 해결한다. 이때 다음에 적용할 함수를 현재 함수의
#    매개변수로 활용한다.

import sys
import re
import operator
import string


# 함수
def read_file(path_to_file, func):
    with open(path_to_file) as f:
        data = f.read()
    func(data, normalize)


def filter_chars(str_data, func):
    pattern = re.compile('[\W+]+')
    func(pattern.sub(' ', str_data), scan)


def normalize(str_data, func):
    func(str_data.lower(), remove_stop_words)


def scan(str_data, func):
    func(str_data.split(), frequencies)


def remove_stop_words(word_list, func):
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    # 한 글자로 된 단어를 추가한다.
    stop_words.extend(list(string.ascii_lowercase))
    func([w for w in word_list if not w in stop_words], sort)


def frequencies(word_list, func):
    wf = dict()
    for w in word_list:
        if w in wf:
            wf[w] += 1
        else:
            wf[w] = 1
    func(wf, print_text)


def sort(wf, func):
    func(sorted(wf.iteritems(), key=operator.itemgetter(1),
                reverse=True), no_op)


def print_text(word_freqs, func):
    for (w, c) in word_freqs[0:25]:
        print w, '-', c
    func(None)


def no_op(func):
    return


# 주 함수
read_file(sys.argv[1], filter_chars)
