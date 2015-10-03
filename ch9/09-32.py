#!/usr/bin/env python2
# coding: utf-8

# 삼위일체
# 제약조건
# 1. 응용 프로그램을 모델, 뷰 컨트롤러라는 세 부분으로 나눈다
# 1-1. 모델은 응용 프로그램의 데이터를 나타낸다
# 1-2. 뷰는 데이터의 트정 해석 방법을 나타낸다
# 1-3. 컨트롤러는 입력 제어 모델 할당/갱신 올바른 뷰 호출을 수행한다
# 2. 모든 응용 프로그램 개체는 이러한 세 부분 중 하나와 연관되며 책임이 겹치지
#    않아야 한다

import sys
import re
import operator
import collections


class WordFrequenciesModel:
    """
    Models the data. In this case, we're only interested in words and their
    frequencies as an end result
    """
    freqs = {}
    stopwords = set(open('../stop_words.txt').read().split(','))

    def __init__(self, path_to_file):
        self.update(path_to_file)

    def update(self, path_to_file):
        try:
            words = re.findall('[a-z]{2,}', open(path_to_file).read().lower())
            self.freqs = collections.Counter(w for w in words
                                             if w not in self.stopwords)
        except IOError:
            print "File not found"
            self.freqs = {}


class WordFrequenciesView:
    def __init__(self, model):
        self._model = model

    def render(self):
        sorted_freqs = sorted(self._model.freqs.iteritems(),
                              key=operator.itemgetter(1),
                              reverse=True)
        for (w, c) in sorted_freqs[0:25]:
            print w, ' - ', c


class WordFrequencyController:
    def __init__(self, model, view):
        self._model, self._view = model, view
        view.render()

    def run(self):
        while True:
            print "Next file: "
            sys.stdout.flush()
            filename = sys.stdin.readline().split()
            self._model.update(filename)
            self._view.render()


m = WordFrequenciesModel(sys.argv[1])
v = WordFrequenciesView(m)
c = WordFrequencyController(m, v)
c.run()
