#!/usr/bin/env python
# coding:utf-8

# 사물
# 제약조건
# 1. 규모가 큰 문제를 문제 영역에 합당한 사물(thing)로 분해한다.
# 2. 각 사물은 데이터의 캡슐이며, 나머지 세상에 프로시저를 드러낸다.
# 3. 데이터에는 절대 직접 접근하지 않으며, 오직 이러한 프로시저를 통해서만 접근한다.
# 4. 캡슐은 다른 캡슐에서 정의한 프로시저를 사용할 수 있다.

import sys
import re
import operator
import string
from abc import ABCMeta

# 클래스


class TFExercise():
    __metaclass__ = ABCMeta

    def info(self):
        return self.__class__.__name__


class DataStorageManager(TFExercise):
    """
    Models the contents of the file
    """

    def __init__(self, path_to_file):
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile('[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()

    def words(self):
        """
        Returns the list words in storage
        :return:
        """
        return self._data.split()

    def info(self):
        return super(DataStorageManager, self).info() + ": My" \
                                                        "major data structure" \
                                                        "is a" + self._data\
            .__class__.__name__


class StopWordManager(TFExercise):
    """
    Models the stop word filter
    """

    def __init__(self):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        # 한 글자로 된 단어를 추가한다.
        self._stop_words.extend(list(string.ascii_lowercase))

    def is_stop_word(self, word):
        return word in self._stop_words

    def info(self):
        return super(StopWordManager, self).info() + \
            ": My major data structure is a " + \
            self._stop_words.__class__.__name__

class WordFrequencyManager(TFExercise):
    """
    Keeps the word frequency data
    """

    def __init__(self):
        self._word_freqs = {}

    def increment_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def sorted(self):
        return sorted(self._word_freqs.iteritems(), key=operator.itemgetter(1),
                      reverse=True)

    def info(self):
        return super(WordFrequencyManager, self).info() + \
            ": My major data structure is a " + \
               self._word_freqs.__class__.__name__


class WordFrequencyController(TFExercise):
    def __init__(self, path_to_file):
        self._storage_manager = DataStorageManager(path_to_file)
        self._stop_word_manager = StopWordManager()
        self._word_freq_manager = WordFrequencyManager()

    def run(self):
        for w in self._storage_manager.words():
            if not self._stop_word_manager.is_stop_word(w):
                self._word_freq_manager.increment_count(w)

        word_freqs = self._word_freq_manager.sorted()
        for (w, c) in word_freqs[0:25]:
            print w, ' - ', c


# main

WordFrequencyController(sys.argv[1]).run()
