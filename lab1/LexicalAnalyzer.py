#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Created by Ross on 19-4-12


class LexicalAnalyzer:
    KEYWORDS = {'begin', 'if', 'then', 'while', 'do', 'end'}

    ONE_SIGNS = {'+', '-', '*', '/', ';', '(', ')', '{', '}', '[', ']', ',', '!', '"', '\''}
    TWO_SIGNS = {
        '<': ['=', '>'],
        '>': ['='],
    }
    STRICT_TWO_SIGNS = {
        ':': ['='],
        '!': ['=']
    }

    keyword_to_category = {word: word.upper() for word in sorted(KEYWORDS)}

    def get_char(self):
        if self.is_end:
            return False
        self.ch = self.src_code[self.p]
        self.token += self.ch
        self.p += 1
        if self.p == len(self.src_code):
            self.is_end = True
        return self.ch

    def retract(self):
        self.is_end = False
        self.p = max(0, self.p - 1)
        if self.p + 1 >= len(self.src_code):
            self.is_end = True
        else:
            self.ch = self.src_code[self.p + 1]
            self.token = self.token[:-1]

    def alpha(self):
        while self.ch.isalpha() or self.ch.isdigit():
            self.get_char()
        self.retract()
        if self.token in self.KEYWORDS:
            self.out.write(self.token + ' ' + str(self.line_p) + '\n')
        else:
            self.out.write('ID ' + self.token + ' ' + str(self.line_p) + '\n')

    def digit(self):
        while self.ch.isdigit() and self.get_char():
            pass
        self.retract()
        self.out.write('CONSTANT ' + self.token + ' ' + str(self.line_p) + '\n')

    def one(self):
        self.out.write(self.token + ' ' + str(self.line_p) + '\n')

    def two(self):
        first_char = self.ch
        if self.get_char() in self.TWO_SIGNS[first_char]:
            self.out.write(self.token + ' ' + str(self.line_p) + '\n')
        else:
            self.retract()
            self.out.write(self.token + ' ' + str(self.line_p) + '\n')

    def strict_two(self):
        first_char = self.ch
        if self.get_char() in self.STRICT_TWO_SIGNS[first_char]:
            self.out.write(self.token + ' ' + str(self.line_p) + '\n')
        else:
            print('ERROR')
            raise Exception('Lexical Error.')

    def annotation(self):
        try:
            end_index = self.src_code.index('\n', self.p)
            self.p = end_index
        except ValueError:
            self.p = len(self.src_code)
            self.is_end = True

    switch = {
        'alpha': alpha,
        'digit': digit,
        'one': one,
        'two': two,
        'strict_two': strict_two,
        'annotation': annotation

    }

    def __init__(self, src_file: str, out_file: str):
        self.is_end = False  # 是否全部读取完
        self.token = ''  # 当前token
        self.p = 0  # 字符指针
        self.ch = ''  # 当前字
        self.line_p = 1
        with open(src_file, 'r', encoding='utf-8') as fin:
            self.src_code = fin.read().replace('\t', '')
        self.out = open(out_file, 'w', encoding='utf-8')
        # print('Your input is:')
        # print(self.src_code)
        # print('code length is', len(self.src_code))
        # print('=' * 20)

    def parse(self):
        try:
            while self.get_char():
                self.token = self.ch
                if self.ch.isalpha():
                    case = 'alpha'
                elif self.ch.isdigit():
                    case = 'digit'
                elif self.ch in self.ONE_SIGNS:
                    case = 'one'
                elif self.ch in self.TWO_SIGNS.keys():
                    case = 'two'
                elif self.ch in self.STRICT_TWO_SIGNS.keys():
                    case = 'strict_two'
                elif self.ch == '#':
                    case = 'annotation'
                elif self.ch == ' ':
                    continue
                elif self.ch == '\n':
                    self.line_p += 1
                    continue
                else:
                    print("ERROR")
                    break
                self.switch[case](self)
        except Exception as e:
            self.out.close()
            e.with_traceback()


if __name__ == '__main__':
    src = 'src_code.txt'
    out = 'out1.txt'
    analyzer = LexicalAnalyzer(src, out)
    analyzer.parse()
