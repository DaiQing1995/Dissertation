import md2py as mp
import re


class MarkDownParser:

    def parse_structure(self):
        f = open("mddata","r")
        x = f.read()
        print(x)
        mdstruc = mp.md2py(x)
        print("------------------------------")
        print(mdstruc.h1[0])
        print("----------purify--------------")
        print(mdstruc.h1[0].descendants)
        # dr = re.compile(r'<[^>]+>', re.S)
        # dd = dr.sub('', mdstruc.h1[0].descendants)
        # print(dd)
        print("----------purified------------")
        print(mdstruc.h1[0].depth)
        print(mdstruc.h1[0].branches)


        print("------------------------------")
        print(mdstruc.h1[1])
        print(mdstruc.h1[1].descendants)
        print(mdstruc.h1[1].depth)
        print(mdstruc.h1[1].branches)


MarkDownParser().parse_structure()
