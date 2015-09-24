#!/usr/bin/env python2
# coding: utf-8

# 데이터 공간
# 제약조건
# 1. 동시에 실행되는 단위가 하나 이상 존재한다.
# 2. 여러 병행 단위에서 데이터를 저장하고 가져오는 데이터 공간(data space)이
#    하나 이상 존재한다.
# 3. 여러 병행 단위는 데이터 공간을 통하지 않고 다른 ㅂ아법으로 데이터를 직접
#    교환하지 못한다.

import re
import sys
import operator
import Queue
import threading

# 두 개의 데이터 공간
word_space = Queue.Queue()
freq_space = Queue.Queue()

stopwords = set(open('../stop_words.txt').read().split(','))


# 단어 공간에 있는 단어를 소비하고
# 부분적인 결과를 빈도 공간으로 보내는 작업 함수
def process_words():
    word_freqs = {}
    while True:
        try:
            word = word_space.get(timeout=1)
        except Queue.Empty:
            break
        if not word in stopwords:
            if word in word_freqs:
                word_freqs[word] += 1
            else:
                word_freqs[word] = 1
    freq_space.put(word_freqs)


# 이 스레드에 단어 공간을 할당하자
for word in re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower()):
    word_space.put(word)

# 작업 스레드를 생성하고 작업을 할당해 실행하자
workers = []
for i in range(5):
    workers.append(threading.Thread(target=process_words))
[t.start() for t in workers]

# 작업 스레드가 마칠 때까지 기다리자
[t.join() for t in workers]

# 빈도 공간에 있는 빈도 데이터를 사용해
# 부준적인 여러 빈도 결과를 병합하자
word_freqs = {}
while not freq_space.empty():
    freqs = freq_space.get()
    for (k, v) in freqs.iteritems():
        if k in word_freqs:
            count = sum(item[k] for item in [freqs, word_freqs])
        else:
            count = freqs[k]
        word_freqs[k] = count

for (w, c) in sorted(word_freqs.iteritems(), key=operator.itemgetter(1),
                     reverse=True)[:25]:
    print w, '-', c
