#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Created by Ross on 19-4-12
s0 = 1  # 初始状态为1
Z = {4}


# ----------------状态转换----------------

def state1(c):
    if c == '1':
        return 2
    return 1


def state2(c):
    if c == '1':
        return 3
    return 2


def state3(c):
    if c == '1':
        return 4
    return 3


def state4(c):
    if c == '1':
        return 5
    return 4


def state5(c):
    return 5


table = {
    1: state1,
    2: state2,
    3: state3,
    4: state4,
    5: state5,
}


# ----------------状态转换----------------

def f(s, c):
    func = table[s]
    return func(c)


def DFA(string):
    s = s0
    for c in string:
        s = f(s, c)
    if s in Z:
        return 'yes'
    else:
        return 'no'


if __name__ == '__main__':
    string = input()
    print(DFA(string))
