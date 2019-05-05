#!/usr/bin/python3
# -*- coding: utf-8 -*-


class SyntaxAnalyzer:

    def __init__(self, in_f, out_f):
        self.line_p = -1  # 在词法分析器输出文件的当前行
        self.is_end = False  # 是否已经读完
        self.stack = ['#', self.L]
        self.data = None  # 当前行的数据
        self.token = None
        with open(in_f, 'r', encoding='utf-8') as fp:
            self.lines = [line.strip() for line in fp]  # 读成字符串
        self.n_line = len(self.lines)  # 词法分析器输出文件的行数
        self.read()

    def read(self):
        if self.is_end:
            return
        self.line_p += 1
        self.is_end = (self.line_p >= self.n_line)
        if self.is_end:
            return
        tmp = self.lines[self.line_p]
        self.data = tmp.split()
        self.token = self.data[0]


    def main(self):
        while len(self.stack):
            func = self.stack.pop()
            if func == '#':
                if self.is_end:
                    print('successfully')
                    return
                else:
                    print('main failed')
                    print('at line:', self.data[-1])
            else:
                func()

    def L(self):
        while self.token in ['if', 'while', 'ID']:
            self.A()

    def A(self):
        if self.token == 'ID':
            self.read()
            if self.token == ':=':
                self.read()
                self.E()
            else:
                print('A := failed')
                print('at line:', self.data[-1])
                exit(1)
        elif self.token in ['if', 'while']:
            self.read()
            if self.token == '(':
                self.read()
                self.EF()
                if self.token == ')':
                    self.read()
                else:
                    print('A  ) failed')
                    print('at line:', self.data[-1])
                    exit(1)
                if self.token == '{':
                    self.read()
                    self.L()
                    if self.token == '}':
                        self.read()
                    else:

                        print('A  } failed')
                        print('at line:', self.data[-1])
                        exit(1)
                else:
                    print('A  { failed')
                    print('at line:', self.data[-1])
                    exit(1)
            else:
                print('A ( failed')
                print('at line:', self.data[-1])
                exit(1)
        else:
            print('A ( failed')
            print('at line:', self.data[-1])
            exit(1)

    def EF(self):
        self.E()
        if self.token in ['>', '<', '=']:
            self.read()
            self.E()
        else:
            print('EF failed')
            print('at line:', self.data[-1])

    def E(self):
        if self.token in ['ID', '(', 'CONSTANT']:
            self.T()
        while self.token in ['+', '-']:
            self.read()
            self.T()

    def T(self):
        if self.token in ['ID', '(', 'CONSTANT']:
            self.F()
        while self.token in ['*', '/']:
            self.read()
            self.F()

    def F(self):
        if self.token in ['ID', 'CONSTANT']:
            self.read()
        elif self.token == '(':
            self.read()
            self.E()
            if self.token != ')':
                print('F failed')
                print('at line:', self.data[-1])
                raise Exception()
            else:
                self.read()
        elif self.is_end:
            print('failed')
            print('at line:', self.data[-1])

    def test(self):
        self.main()


if __name__ == '__main__':
    in_f = 'out1.txt'
    out_f = 'out2.txt'
    sa = SyntaxAnalyzer(in_f, out_f)
    sa.test()
