#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 코드 골프
# 제약 조건
# 1. 코드 줄 수를 가능한 한 적게 한다.

import re, sys, collections

stops = open('../stop_words.txt').read().split(',')
words = re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower())
counts = collections.Counter(w for w in words if w not in stops)
for (w, c) in counts.most_common(25):
    print w, '-', c
