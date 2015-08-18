#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 무한거울
# 제약조건
# 1. 문제에서 모든 또는 중요한 부분을 귀납법을 사용하여 모델링한다.

import re
import sys
import operator

# 총 실행 횟수는 달라질 수 있다. 프로그램이 충돌하면 낮춘다.
RECURSION_LIMIT = 9500

# 명칭과 달리 재귀를 통제하는 것이 아니라 호출 스택의 깊이를 통제하므로 조금더 추가한다.
sys.setrecursionlimit(RECURSION_LIMIT + 10)

def count(word_list, stopwords, wordfreqs):
    # 빈 리시트일 때 할 일
    if word_list == []:
        return
    # 귀납적 사례, 단어 목록으로 할 일
    else:
        # 가장 앞 단어를 처리한다
        word = word_list[0]
        if word not in stopwords:
            if word in word_freqs:
                wordfreqs[word] += 1
            else:
                wordfreqs[word] = 1
        # 가장 끝 단어를 처리한다.
        count(word_list[1:], stopwords, wordfreqs)


def wf_print(wordfreq):
    if wordfreq == []:
        return
    else:
        (w, c) = wordfreq[0]
        print w, ' - ', c
        wf_print(wordfreq[1:])


stop_words = set(open('../stop_words.txt').read().split(','))
words = re.findall('\w{2,}', open(sys.argv[1]).read().lower())
word_freqs = dict()

# 이론적으로는 count(words, word_freqs)를 호출할 뿐이다.
# 어떻게 되는지 시험 삼아 해 본다.
for i in range(0, len(words), RECURSION_LIMIT):
    count(words[i:i+RECURSION_LIMIT], stop_words, word_freqs)

wf_print(sorted(word_freqs.iteritems(), key=operator.itemgetter(1),
                reverse=True)[:25])