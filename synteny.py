#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import argparse,os

def get_list(begin,end,gene_list):
    a=gene_list.index(begin)
    b=gene_list.index(end)
    blcok=gene_list[a:b+1]
    return blcok

def put_list(first_syn,second_syn):
    str=""
    sep = "\t"
    for i,j in zip(first_syn,second_syn):
        str = str + "#block"+ bytes(first_syn.index(i)+1) + "\n"
        str = str + "first block:" + sep.join(i) + "\n"
        str = str + "second block:" + sep.join(j) +"\n"
    return str

def filter_gene(inputfile,outputfile,size):
    try:
        data = pd.read_csv(inputfile)
    except:
        print "make true you file is csv and the format is right"
    if "chromosome/scaffold name" not in data.columns[1].lower():
        print "the first Chromosome/scaffold name is not exit,you must let it in 2 columns"
    if "chromosome/scaffold name" not in data.columns[5].lower():
        print "the second Chromosome/scaffold name is not exit,you must let it in 6 columns"

    groups_first=data.groupby(data[data.columns[1]])
    # 成功利用print验证，可以获取染色体单对单的列表
    for first_ch ,group_first in groups_first:
        groups_first_second=group_first.groupby(group_first[group_first.columns[5]])
        for second_ch ,group_first_second in groups_first_second:
            second_gene =list(group_first_second.sort_values(by=group_first_second.columns[6])[group_first_second.columns[4]].drop_duplicates())
            first_gene = list(group_first_second.sort_values(by=group_first_second.columns[2])[group_first_second.columns[0]].drop_duplicates())
            group_first_second_sort = group_first_second.sort_values(by=[group_first_second.columns[2], group_first_second.columns[6]])
            #对数据框按照第一关键词first_startbp，第二关键词为second_startbp的排序，先first后second的原因是我是按照每一个first的基因去遍历second的所有
            #for i,j in zip(group_first_second_sort[group_first_second.columns[4]],group_first_second_sort[group_first_second.columns[0]]):
                #print second_gene.index(i),'and',first_gene.index(j)
            #以上进行测试结果符合预期
            # 创建一个全是0的array，同时second_gene作为行数，first_gene作为列数
            matrix=np.zeros([len(second_gene),len(first_gene)],int)
            second_syn = []
            first_syn = []

            for i,j in zip(group_first_second_sort[group_first_second.columns[4]],group_first_second_sort[group_first_second.columns[0]]):
                #将对应的同源基因所对应的位置赋值为 1
                matrix[second_gene.index(i),first_gene.index(j)]=1
            #从所有 1 的点开始移动框
            for i,j in zip(group_first_second_sort[group_first_second.columns[4]],group_first_second_sort[group_first_second.columns[0]]):
                #判断这个 1 是否已经包含在别的框内，若是则没必要从此开始
                if matrix[second_gene.index(i),first_gene.index(j)]!=1:
                    continue
                #创建list存放
                second_syn_begin,second_syn_end=i,i
                first_syn_begin,first_syn_end=j,j
                m,n=second_gene.index(i),first_gene.index(j)
                j,k=second_gene.index(i),first_gene.index(j)
                if len(second_gene) - 1 - j < size:
                    ec = len(second_gene) - 1 - j
                else:
                    ec = size
                if len(first_gene) - 1 - k < size:
                    eg = len(first_gene) - 1 - k
                else:
                    eg = size

                while n <= k+eg :
                    while m<= j+ec :

                        if matrix[m,n]>0:
                            second_syn_end=second_gene[m]
                            first_syn_end=first_gene[n]
                            k,j=n,m
                            # 这里计算-1是因为len返回的是长度，但是数组开始是0
                            if len(second_gene)-1- j < size:
                                ec = len(second_gene)-1 - j
                            else:
                                ec = size
                            if len(first_gene)-1 - k < size:
                                eg = len(first_gene)-1- k
                            else:
                                eg = size

                            matrix[m,n]=2
                            m=m+1
                            break
                        m=m+1
                        #判断是否到达框的边缘

                        if m>j+ec:
                            m=m-ec
                            break
                    n=n+1
                if second_syn_end!=second_syn_begin:
                    block_second=get_list(second_syn_begin,second_syn_end,second_gene)
                    block_first=get_list(first_syn_begin,first_syn_end,first_gene)
                    second_syn.append(block_second)
                    first_syn.append(block_first)
            with open(outputfile,'a') as f:
                str_title=">spotted first Chromosome/scaffold name:"+ str(first_ch)+ "; " +data.columns[5] + ":" + str(second_ch) +"\n"
                block = put_list(first_syn,second_syn)
                f.write(str_title + block)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", help="dim the window size", default=100, type=int)
    parser.add_argument("-i", "--inputfile", help="the input file you give,must be csv file", type=str)
    parser.add_argument("-o", "--outputfile", help="the output file you want create", type=str)
    args = parser.parse_args()
    inputfile = args.inputfile
    outputfile = args.outputfile
    size = args.size
    if os.path.exists(outputfile):
        print "the outputfile is already exists,we won't delete it,please delete it by yourself"
        os._exit()
    filter_gene(inputfile,outputfile,size)











