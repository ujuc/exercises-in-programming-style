#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 제약조건
# 1. 주기억 장치의 양은 매우 적으며  일반적으로 처리/생성할 데이터에 비해 매우 적다.
# 2. 식별자가 없다 즉  변수명이나 참조할 꼬리표가 붙은 메모리 주소가 없으며 숫자로
#    가릴킬 수 있는 메모리만 있다.

import sys
import os
import string


def touchopen(filename, *args, **kwargs):
    try:
        os.remove(filename)
    except OSError:
        pass
    open(filename, "a").close()
    return open(filename, *args, **kwargs)


data = []

f = open('../stop_words.txt')
data = [f.read(1024).split(',')]
f.close()

data.append([])     # data[1] line (max 80 characters)
data.append(None)   # data[2] index of start_char of word
data.append(0)      # data[3] index on characters, i = 0
data.append(False)  # data[4] flag indicationg if word was found
data.append('')     # data[5] word
data.append('')     # data[6] word,NNN
data.append(0)      # data[7] frequency

word_freqs = touchopen('word_freqs', 'rb+')
f = open(sys.argv[1])

while True:
    data[1] = [f.readline()]
    if data[1] == ['']:
        break
    if data[1][0][len(data[1][0])-1] != '\n':
        data[1][0] = data[1][0] + '\n'

    data[2] = None
    data[3] = 0

    for c in data[1][0]:
        if data[2] == None:
            if c.isalnum():
                data[2] = data[3]
        else:
            if not c.isalnum():
                data[4] = False
                data[5] = data[1][0][data[2]:data[3]].lower()
                if len(data[5]) >= 2 and data[5] not in data[0]:
                    while True:
                        data[6] = word_freqs.readline().strip()
                        if data[6] == '':
                            break
                        data[7] = int(data[6].split(',')[1])
                        data[6] = data[6].split(',')[0].strip()
                        if data[5] == data[6]:
                            data[7] += 1
                            data[4] = True
                            break
                    if not data[4]:
                        word_freqs.seek(0, 1)
                        word_freqs.writelines("%20s,%04d\n" % (data[5], 1))
                    else:
                        word_freqs.seek(-26, 1)
                        word_freqs.writelines("%20s,%04d\n"
                                              % (data[5], data[7]))
                    word_freqs.seek(0, 0)
                data[2] = None
        data[3] += 1
f.close()
word_freqs.flush()

del data[:]

data = data + [[]] * (25 - len(data))
data.append('')
data.append(0)

while True:
    data[25] = word_freqs.readline().strip()
    if data[25] == '':
        break
    data[26] = int(data[25].split(',')[1])
    data[25] = data[25].split(',')[0].strip()
    for i in range(25):
        if data[i] == [] or data[i][1] < data[26]:
            data.insert(i, [data[25], data[26]])
            del data[26]
            break

for tf in data[0:25]:
    if len(tf) == 2:
        print tf[0], ' - ', tf[1]

word_freqs.close()
