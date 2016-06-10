#!/usr/bin/python

import operator
import sys

def main():
    in_file = open(sys.argv[1])
    out_file = open(sys.argv[2],'w')
    do_normalization = ("True" == sys.argv[3])

    x = {}
    szum = 0.0
    for i in in_file:
        splitted = i.split(" ")
        x[splitted[0]] = float(splitted[1])
        szum += float(splitted[1])
    in_file.close()
    if do_normalization:
        for i in x:
            x[i] = x[i] / szum
    sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
    for i in sorted_x:
        out_file.write(i[0]+" "+str(i[1])+"\n")
    out_file.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise RuntimeError("Usage: <input_file> <output_file> <do_normalization>")
    else:
        main()