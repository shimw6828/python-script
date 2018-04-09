#!/usr/bin/python
# encoding: utf-8
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--size", help="dim the window size", default=100, type=int)
parser.add_argument("-i", "--inputfile", help="the input file you give,must be csv file", type=str)
parser.add_argument("-o", "--outputfile", help="the output file you want create", type=str)
args = parser.parse_args()
inputfile = args.inputfile
outputfile = args.outputfile
size = args.size
print size


