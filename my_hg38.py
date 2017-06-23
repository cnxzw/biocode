#-*-coding:utf-8-*-

"""
@author:xzw
@file:my_hg38.py
@time:2017/6/20 21:44
"""
import re
import sys
import time
from collections import OrderedDict


args = sys.argv

class Gene_info:
    def __init__(self):
        self.chr = ""
        self.start = 0
        self.end = 0


class Gene(Gene_info):
    def __init__(self):
        Gene_info.__init__(self)
        self.orit = ""
        self.id = ""


class Trans(Gene_info):
    def __init__(self):
        Gene_info.__init__(self)
        self.parent = ""
        self.id = ""


class Exon(Gene_info):
    def __init__(self):
        Gene_info.__init__(self)
        self.parent = ""


def main(args):
    start_time = time.clock()
    list_chr = []
    list_gene = OrderedDict()
    list_trans = OrderedDict()
    list_exon = []

    with open(args[1], 'r')as fin:
        for line in fin:
            line = line.strip()
            if line.startswith('#'):
                continue
            lst = line.split('\t')
            chr = lst[0]
            type = lst[2]
            start = int(lst[3])
            end = int(lst[4])
            orit = lst[6]
            attr = lst[8]
            if "protein_coding" not in attr:
                continue

            if chr not in list_chr:
                list_chr.append(chr)

            if type == "gene":
                gene = Gene()
                id = re.search(r'gene_id "([^;]+)";?', attr).group(1)
                gene.chr = chr
                gene.start = start
                gene.end = end
                gene.orit = orit
                gene.id = id
                list_gene[id] = gene

            elif type == "transcript":
                trans = Trans()
                parent = re.search(r'gene_id "([^;]+)";?', attr).group(1)
                if parent not in list_gene:
                    continue
                id = re.search(r'transcript_id "([^;]+)";?', attr).group(1)
                trans.parent = parent
                trans.chr = chr
                trans.start = start
                trans.end = end
                trans.id = id
                list_trans[id] = trans

            elif type == "exon":
                exon = Exon()
                parent = re.search(r'transcript_id "([^;]+)";?', attr).group(1)
                exon.parent = parent
                exon.chr = chr
                exon.start = start
                exon.end = end
                list_exon.append(exon)

    chr_gene(list_gene)
    gene_length(list_gene)
    gene_trans(list_trans)
    trans_exon(list_exon)
    exon_pos(list_exon)

    end_time = time.clock()
    print "Use %.2f s" % (end_time - start_time)


def chr_gene(list_gene):
    chr_info = OrderedDict()
    for gene_info in list_gene.values():
        chr_id = gene_info.chr
        if chr_id in chr_info:
            chr_info[chr_id] += 1
        else:
            chr_info[chr_id] = 1
    with open("chr_gene.txt", 'w') as fout:
        fout.write("染色体基因个数分布情况\n")
        for chr_id, num in chr_info.items():
            fout.write("%s\t%d\n" % (chr_id, num))


def gene_length(list_gene):
    with open("gene_length.txt", 'w') as fout:
        fout.write("基因长度分布情况\n")
        for gene_id, gene_info in list_gene.items():
            length = gene_info.end - gene_info.start + 1
            fout.write("%s\t%d\n" % (gene_id, length))


def gene_trans(list_trans):
    count_trans = OrderedDict()
    for info in list_trans.values():
        gene_id = info.parent
        if gene_id in count_trans:
            count_trans[gene_id] += 1
        else:
            count_trans[gene_id] = 1
    with open('gene_trans.txt', 'w') as fout:
        fout.write("基因转录本个数分布情况\n")
        for gene_id, num in count_trans.items():
            fout.write("%s\t%d\n" % (gene_id, num))


def trans_exon(list_exon):
    trans_info = OrderedDict()
    for exon_info in list_exon:
        trans_id = exon_info.parent
        if trans_id in trans_info:
            trans_info[trans_id] += 1
        else:
            trans_info[trans_id] = 1
    with open('trans_exon.txt', 'w') as fout:
        fout.write("转录本外显子个数分布情况\n")
        for trans_id, num in trans_info.items():
            fout.write("%s\t%d\n" % (trans_id, num))


def exon_pos(list_exon):
    trans_exon = OrderedDict()
    for exon_info in list_exon:
        trans_id = exon_info.parent
        if trans_id not in trans_exon:
            trans_exon[trans_id] = "%s-%s" % (str(exon_info.start), str(exon_info.end))
        else:
            trans_exon[trans_id] += ",%s-%s" % (str(exon_info.start), str(exon_info.end))
    with open('exon_pos.txt', 'w') as fout:
        fout.write("外显子位置信息\n")
        for trans_id, exon_pos in trans_exon.items():
            fout.write("%s\t%s\n" % (trans_id, exon_pos))

if __name__ == "__main__":
    main(args)
