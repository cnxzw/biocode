#-*-coding:utf-8-*-

"""
@author:xzw
@file:hg38.py
@time:2017/6/15 22:37
"""

"""
生信编程第3题
数据来源：ensembl  gtf格式
ftp://ftp.ensembl.org/pub/release-87/gtf/homo_sapiens/Homo_sapiens.GRCh38.87.chr.gtf.gz
统计信息：
1染色体上基因分布
2基因长度
3基因上转录本分布
4转录本上外显子分布
5外显子位置信息
"""


import sys
import re

args = sys.argv


class Genome_info:
    def __init__(self):
        self.chr = ""
        self.start = 0
        self.end = 0


class Gene(Genome_info):
    def __init__(self):
        Genome_info.__init__(self)
        self.orientation = ""
        self.id = ""


class Transcript(Genome_info):
    def __init__(self):
        Genome_info.__init__(self)
        self.id = ""
        self.parent = ""


class Exon(Genome_info):
    def __init__(self):
        Genome_info.__init__(self)
        self.parent = ""


def main(args):
    """
    一个输入参数：
    第一个参数为物种gtf文件

    :return:
    """

    list_chr = []
    list_gene = {}
    list_transcript = {}
    list_exon = []
    # l_n = 0
    with open(args[1]) as fp_gtf:
        for line in fp_gtf:
            if line.startswith("#"):
                continue
            # print ("in %s" % l_n)
            # l_n += 1
            lines = line.strip("\n").split("\t")
            chr = lines[0]
            type = lines[2]
            start = int(lines[3])
            end = int(lines[4])
            orientation = lines[6]
            attr = lines[8]
            if not re.search(r'protein_coding', attr):
                continue

            if not chr in list_chr:
                list_chr.append(chr)

            if type == "gene":
                gene = Gene()
                id = re.search(r'gene_id "([^;]+)";?', attr).group(1)
                gene.chr = chr
                gene.start = start
                gene.end = end
                gene.id = id
                gene.orientation = orientation
                list_gene[id] = gene
                # print(id)
            elif type == "transcript":
                transcript = Transcript()
                id = re.search(r'transcript_id "([^;]+)";?', attr).group(1)
                parent = re.search(r'gene_id "([^;]+)";?', attr).group(1)
                if not parent in list_gene:
                    continue
                transcript.chr = chr
                transcript.start = start
                transcript.end = end
                transcript.id = id
                transcript.parent = parent
                list_transcript[id] = transcript

            elif type == "exon":
                exon = Exon()
                parent = re.search(r'transcript_id "([^;]+)";?', attr).group(1)
                if not parent in list_transcript:
                    continue
                exon.chr = chr
                exon.start = start
                exon.end = end
                exon.parent = parent
                list_exon.append(exon)

    chr_gene(list_gene)
    gene_len(list_gene)
    gene_transcript(list_transcript)
    transcript_exon(list_exon)
    exon_pos(list_exon)


def chr_gene(list_gene):
    """
    染色体上基因数量分布

    :param list_gene:
    :return:
    """

    print("染色体上基因数量分布")
    count_gene = {}
    for info in list_gene.values():
        chr = info.chr
        if chr in count_gene:
            count_gene[info.chr] += 1
        else:
            count_gene[info.chr] = 1
    with open("chr_gene.txt", 'w') as fp_out:
        for chr, num in count_gene.items():
            print("\t".join([chr, str(num)]) + "\n")
            fp_out.write("\t".join([chr, str(num)]) + "\n")


def gene_len(list_gene):
    """
    基因长度分布情况

    :param list_gene:
    :return:
    """

    print ("基因长度分布情况")
    with open("gene_len.txt", 'w') as fp_out:
        for gene_id, info in list_gene.items():
            len = info.end - info.start + 1
            fp_out.write("\t".join([gene_id, str(len)]) + "\n")
            print("\t".join([gene_id, str(len)]) + "\n")


def gene_transcript(list_transcript):
    """
    基因的转录本数量分布

    :param list_transcript:
    :return:
    """

    print("基因的转录本数量分布")
    count_transcript = {}
    for info in list_transcript.values():
        gene_id = info.parent
        if gene_id in count_transcript:
            count_transcript[gene_id] += 1
        else:
            count_transcript[gene_id] = 1
    with open("gene_transcript.txt", 'w') as fp_out:
        for gene_id, num in count_transcript.items():
            print("\t".join([gene_id, str(num)]) + "\n")
            fp_out.write("\t".join([gene_id, str(num)]) + "\n")


def transcript_exon(list_exon):
    """
    转录本的外显子数量统计

    :param list_exon:
    :return:
    """

    print("转录本的外显子数量统计")
    count_exon = {}
    for exon in list_exon:
        transcript_id = exon.parent
        if transcript_id in count_exon:
            count_exon[transcript_id] += 1
        else:
            count_exon[transcript_id] = 1
    with open("transcript_exon.txt", 'w') as fp_out:
        for transcript_id, num in count_exon.items():
            print("\t".join([transcript_id, str(num)]) + "\n")
            fp_out.write("\t".join([transcript_id, str(num)]) + "\n")


def exon_pos(list_exon):
    """
    外显子坐标统计

    :param list_exon:
    :return:
    """

    print("外显子坐标统计")
    count_exon = {}
    for exon in list_exon:
        transcript_id = exon.parent
        if transcript_id in count_exon:
            count_exon[transcript_id] += ",%s-%s" % (str(exon.start), str(exon.end))
        else:
            count_exon[transcript_id] = "%s-%s" % (str(exon.start), str(exon.end))
    with open("exon_pos.txt", 'w') as fp_out:
        for transcript_id, pos in count_exon.items():
            print("\t".join([transcript_id, pos]) + "\n")
            fp_out.write("\t".join([transcript_id, pos]) + "\n")


def gene_exon_pos(list_gene, list_transcript, list_exon):
    """
    根据exon的parent将所有exon对应到transcript
    根据transcript的parent将所有transcript对应到gene
    根据gene按chr分组得到chromosome列表

    从chromosome中输出某个指定基因的所有外显子坐标信息并画图
    生信编程直播第五题

    :param list_gene:
    :param list_transcript:
    :param list_exon:
    :return:
    """
    pass


if __name__ == "__main__":
    main(args)