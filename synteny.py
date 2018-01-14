import numpy as np
import pandas as pd

def get_list(begin,end,gene_list):
    a=gene_list.index(begin)
    b=gene_list.index(end)
    blcok=gene_list[a:b]
    return blcok
def put_list(gar_syn,cave_syn):
    str=""
    sep = "\t"
    for i,j in zip(gar_syn,cave_syn):
        str = str + "#block"+ bytes(gar_syn.index(i)+1) + "\n"
        str = str + "gar block:" + sep.join(i) + "\n"
        str = str + "cave block:" + sep.join(j) +"\n"
    return str



data = pd.read_csv('/home/wangdy/WGD/ortholog/gar&cavefish.csv')

groups_gar=data.groupby(data[data.columns[1]])
# 成功利用print验证，可以获取染色体单对单的列表
for gar_ch ,group_gar in groups_gar:
    groups_gar_cave=group_gar.groupby(group_gar[group_gar.columns[6]])
    for cave_ch ,group_gar_cave in groups_gar_cave:
        cave_gene =list(group_gar_cave.sort_values(by=group_gar_cave.columns[7])[group_gar_cave.columns[4]].drop_duplicates())
        gar_gene = list(group_gar_cave.sort_values(by=group_gar_cave.columns[2])[group_gar_cave.columns[0]].drop_duplicates())
        group_gar_cave_sort = group_gar_cave.sort_values(by=[group_gar_cave.columns[2], group_gar_cave.columns[7]])
        #对数据框按照第一关键词gar_startbp，第二关键词为cave_startbp的排序，先gar后cave的原因是我是按照每一个gar的基因去遍历cave的所有
        #for i,j in zip(group_gar_cave_sort[group_gar_cave.columns[4]],group_gar_cave_sort[group_gar_cave.columns[0]]):
            #print cave_gene.index(i),'and',gar_gene.index(j)
        #以上进行测试结果符合预期
        # 创建一个全是0的array，同时cave_gene作为行数，gar_gene作为列数
        matrix=np.zeros([len(cave_gene),len(gar_gene)],int)
        cave_syn = []
        gar_syn = []

        for i,j in zip(group_gar_cave_sort[group_gar_cave.columns[4]],group_gar_cave_sort[group_gar_cave.columns[0]]):
            #将对应的同源基因所对应的位置赋值为 1
            matrix[cave_gene.index(i),gar_gene.index(j)]=1
        #从所有 1 的点开始移动框
        for i,j in zip(group_gar_cave_sort[group_gar_cave.columns[4]],group_gar_cave_sort[group_gar_cave.columns[0]]):
            #判断这个 1 是否已经包含在别的框内，若是则没必要从此开始
            if matrix[cave_gene.index(i),gar_gene.index(j)]!=1:
                continue
            #创建list存放
            cave_syn_begin,cave_syn_end=i,i
            gar_syn_begin,gar_syn_end=j,j
            m,n=cave_gene.index(i)+1,gar_gene.index(j)+1
            j,k=cave_gene.index(i),gar_gene.index(j)
            #因为是检索框后 的内容，所以m和n各加 1
            if len(cave_gene) - 1 - j < 5:
                ec = len(cave_gene) - 1 - j
            else:
                ec = 5
            if len(gar_gene) - 1 - k < 5:
                eg = len(gar_gene) - 1 - k
            else:
                eg = 5

            while n <= k+eg :
                while m<= j+ec :

                    if matrix[m,n]>0:
                        cave_syn_end=cave_gene[m]
                        gar_syn_end=gar_gene[n]
                        k,j=n,m
                        # 这里计算-1是因为len返回的是长度，但是数组开始是0
                        if len(cave_gene)-1- j < 5:
                            ec = len(cave_gene)-1 - j
                        else:
                            ec = 5
                        if len(gar_gene)-1 - k < 5:
                            eg = len(gar_gene)-1- k
                        else:
                            eg = 5

                        matrix[m,n]=2
                        m=m+1
                        break
                    m=m+1
                    #判断是否到达框的边缘

                    if m>j+ec:
                        m=m-ec
                        cave_syn_in=[]
                        break
                n=n+1
            if cave_syn_end!=cave_syn_begin:
                block_cave=get_list(cave_syn_begin,cave_syn_end,cave_gene)
                block_gar=get_list(gar_syn_begin,gar_syn_end,gar_gene)
                cave_syn.append(block_cave)
                gar_syn.append(block_gar)
        with open('/opt/shimw/pycharm/test/synteny.txt','a') as f:
            str=">spotted gar Chromosome/scaffold name:"+ gar_ch + "; " +data.columns[6] + ":" + cave_ch +"\n"
            block = put_list(gar_syn,cave_syn)
            f.write(str + block)













