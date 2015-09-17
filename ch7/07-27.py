#!/usr/bin/env python2
# coding: utf-8

# 게으른 강
# 제약조건
# 1. 데이터는 온전한 한 덩어리(complete whole)가 아니라 스트림으로 사용할 수
#    있다.
# 2. 함수는 한 데이터 스트림을 다른 것으로 바꾸는 필터/변환기다.
# 3. 데이터는 다운스트림의 필요에 따라 업스트림에서 처리된다.

import sys
import operator
import string


def characters(filename):
    for line in open(filename):
        for c in line:
            yield c


def all_words(filename):
    start_char = True
    for c in characters(filename):
        if start_char == True:
            word = ""
            if c.isalnum():
                # 단어 시작을 찾았다.
                word = c.lower()
                start_char = False
            else:
                pass
        else:
            if c.isalnum():
                word += c.lower()
            else:
                # 단어 끝을 찾았으며, 그 단어를 반환한다.
                start_char = True
                yield word


def non_stop_words(filename):
    stopwords = set(open('../stop_words.txt').read().split(',') +
                    list(string.ascii_lowercase))
    for w in all_words(filename):
        if not w in stopwords:
            yield w


def count_and_sort(filename):
    freqs, i = {}, 1
    for w in non_stop_words(filename):
        freqs[w] = 1 if w not in freqs else freqs[w] + 1
        if i % 5000 == 0:
            yield sorted(freqs.iteritems(), key=operator.itemgetter(1),
                         reverse=True)
        i = i + 1
    yield sorted(freqs.iteritems(), key=operator.itemgetter(1),
                 reverse=True)


# main
for word_freqs in count_and_sort(sys.argv[1]):
    print "-------------------------------"
    for (w, c) in word_freqs[0:25]:
        print "{} - {}".format(w, c)
