#!/usr/bin/env python2
# coding: utf-8

# 애스팩트
# 제약조건
# 1. 문제를 어떤 추상 형태(프로시저, 함수, 객체 등)를 사용해 분해한다.
# 2. 해당 추상에 관한 소스코드 또는 그 추상을 사용하는지점의 소스코드를 전혀 편집하지 않고 해당 문제의
#    애스펙트(aspect)를 주 프로그램에 추가한다.
# 3. 외부 결합 베커니즘은 해당 추상을 애스펙트와 결합한다.

import sys
import re
import operator
import string
import time


# 함수
def extract_words(path_to_file):
    with open(path_to_file) as f:
        str_data = f.read()
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]


def frequencies(word_list):
    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs


def sort(word_freq):
    return sorted(word_freq.iteritems(), key=operator.itemgetter(1),
                  reverse=True)


# 부가 기능
def profile(f):
    def profilewrapper(*arg, **kw):
        start_time = time.time()
        ret_value = f(*arg, **kw)
        elapsed = time.time() - start_time
        print "{}(...) took {} secs".format(f.__name__, elapsed)
        return ret_value

    return profilewrapper


# 결합점
tracked_functions = [extract_words, frequencies, sort]

# 직조기
for func in tracked_functions:
    globals()[func.func_name] = profile(func)

word_freqs = sort(frequencies(extract_words(sys.argv[1])))

for (w, c) in word_freqs[0:25]:
    print "{} - {}".format(w, c)
