#!/usr/bin/python3
# -*- coding: utf-8 -*-


class SyntaxDirectedTranslate:

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
        av1 = av2 = op = None
        if self.token == 'ID':
            av1 = self.data[1]
            self.read()
            if self.token == ':=':
                op = ':='
                self.read()
                av2 = self.E()
                av1 = av1 + ':=' + av2
                print(av1)
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
        ef1 = ef2 = op = None
        ef1 = self.E()
        print('EF1:=' + ef1)
        if self.token in ['>', '<', '=']:
            op = self.token
            self.read()
            ef2 = self.E()
            print('EF2:=' + ef2)

            print('EF1' + op + 'EF2')
        else:
            print('EF failed')
            print('at line:', self.data[-1])

    def E(self):
        ev1 = ev2 = op = None
        i = 0
        if self.token in ['ID', '(', 'CONSTANT']:
            ev1 = self.T()
            print('tmpE{}:='.format(i) + ev1)
            i+=1
        while self.token in ['+', '-']:
            op = self.data[0]
            self.read()
            ev2 = self.T()
            # ev1 = ev1 + op + ev2
            print('tmpE{}:=tmpE{}'.format(i, i - 1) + op + ev2)
        return 'tmpE{}'.format(i - 1)

    def T(self):
        tv1 = tv2 = op = None
        i = 0
        if self.token in ['ID', '(', 'CONSTANT']:
            tv1 = self.F()
            print('tmpT{}:='.format(i) + tv1)
            i += 1
        while self.token in ['*', '/']:
            op = self.data[0]
            self.read()
            tv2 = self.F()
            # tv1 = tv1 + op + tv2
            print('tmpT{}:=tmpT{}'.format(i, i - 1) + op + tv2)
        return 'tmpT{}'.format(i - 1)

    def F(self):
        if self.token in ['ID', 'CONSTANT']:
            f = self.data[1]
            self.read()
            return str(f)
        elif self.token == '(':
            self.read()
            e = self.E()
            if self.token != ')':
                print('F failed')
                print('at line:', self.data[-1])
                raise Exception()
            else:
                self.read()
                print('tmpF:=', e)
                # return '(' + e + ')'
                return 'tmpF'
        elif self.is_end:
            print('failed')
            print('at line:', self.data[-1])

    def test(self):
        self.main()


if __name__ == '__main__':
    in_f = 'out1.txt'
    out_f = 'out2.txt'
    sa = SyntaxDirectedTranslate(in_f, out_f)
    sa.test()
