#!/usr/bin/env python2
# coding: utf-8

# 격리
# 제약조건
# 1. 핵심 프로그램 함수는 입출력(IO)를 포함해 어떤 부수 효과도 없다.
# 2. 모둔 입출력 행동은 반드시 순수 함수와 명확히 분리된 계산열(Computation sequence)에 포함돼
#    있어야 한다.
# 3. 입출력이 있는 모든 순차열은 반드시 주 프로그램에서 호출해야 한다.

import sys
import re
import operator
import string


# 예제를 위한 격리 클래스
class TFQuarantine:
    def __init__(self, func):
        self._funcs = [func]

    def bind(self, func):
        self._funcs.append(func)
        return self

    def execute(self):
        def guard_callable(v):
            return v() if hasattr(v, '__call__') else v

        value = lambda: None
        for func in self._funcs:
            value = func(guard_callable(value))
        print guard_callable(value)


# 함수
def get_input(agr):
    def _f():
        return sys.argv[1]

    return _f


def extract_words(path_to_file):
    def _f():
        with open(path_to_file) as f:
            data = f.read()
        pattern = re.compile('[\W_]+')
        word_list = pattern.sub(' ', data).lower().split()
        return word_list

    return _f


def remove_stop_words(word_list):
    def _f():
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
        # 한글자로 된 단어를 추가한다.
        stop_words.extend(list(string.ascii_lowercase))
        return [w for w in word_list if not w in stop_words]

    return _f


def frequencies(word_list):
    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs


def sort(word_freq):
    return sorted(word_freq.iteritems(),
                  key=operator.itemgetter(1),
                  reverse=True)


def top25_freqs(word_freqs):
    top25 = ""
    for tf in word_freqs[0:25]:
        top25 += '{} - {}\n'.format(str(tf[0]), str(tf[1]))
    return top25


# main
TFQuarantine(get_input) \
    .bind(extract_words) \
    .bind(remove_stop_words) \
    .bind(frequencies) \
    .bind(sort) \
    .bind(top25_freqs) \
    .execute()
