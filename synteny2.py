import numpy as np
import pandas as pd
import argparse

def get_list(begin,end,gene_list):
    a=gene_list.index(begin)
    b=gene_list.index(end)
    blcok=gene_list[a:b]
    return blcok

#get the parser
parser = argparse.ArgumentParser()
parser.add_argument("-s","--size",help="dim the window size",default=100,type=int)
parser.add_argument("-i","--inputfile",help="the input file you give,must be csv file",type=str)
parser.add_argument("-o","--outputfile",help="the output file you want create" ,type=str)
args = parser.parse_args()
inputfile=args.inputfile
outpufile=args.outputfile
size=args.size


data = pd.read_csv(inputfile)

groups_gar=data.groupby(data[data.columns[1]])





for gar_ch ,group_gar in groups_gar:
    groups_gar_cave=group_gar.groupby(group_gar[group_gar.columns[6]])
    for cave_ch ,group_gar_cave in groups_gar_cave:
        cave_gene =list(group_gar_cave.sort_values(by=group_gar_cave.columns[7])[group_gar_cave.columns[4]].drop_duplicates())
        gar_gene = list(group_gar_cave.sort_values(by=group_gar_cave.columns[2])[group_gar_cave.columns[0]].drop_duplicates())
        group_gar_cave_sort = group_gar_cave.sort_values(by=[group_gar_cave.columns[2], group_gar_cave.columns[7]])
        for i, j in zip(group_gar_cave_sort[group_gar_cave.columns[4]], group_gar_cave_sort[group_gar_cave.columns[0]]):
            print cave_gene.index(i) ,"and", gar_gene.index(j)


