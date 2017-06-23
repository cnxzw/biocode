#-*-coding:utf-8-*-

"""
@author:xzw
@file:gene_model.py
@time:2017/6/21 11:10
"""
import sys
from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Rectangle

args = sys.argv

geneCord = OrderedDict()
GRCh38Exon = OrderedDict()
GRCh38UTR = OrderedDict()

def main():
    with open(args[1],'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue

            lst = line.split('\t')

            if lst[-1].startswith("ID=gene"):
                gene_info = lst[-1].split(';')
                geneName = gene_info[1].split('=')[1]
                geneCord[geneName] = [int(lst[3]),int(lst[4])]
                GRCh38Exon[geneName] = OrderedDict()
                GRCh38UTR[geneName] = OrderedDict()

            elif lst[-1].startswith('ID=transcript'):
                trans_info = lst[-1].split(';')
                transName = trans_info[2].split('=')[1]
                GRCh38Exon[geneName][transName] = []
                GRCh38Exon[geneName][transName].append(lst[6])
                GRCh38UTR[geneName][transName] = []

            elif lst[2] == 'exon':
                GRCh38Exon[geneName][transName].extend([int(lst[3]),int(lst[4])])

            elif lst[2] in ['three_prime_UTR','five_prime_UTR']:
                GRCh38UTR[geneName][transName].extend([int(lst[3]),int(lst[4])])

    matplotlib.style.use('ggplot')
    gene_model(args[2])

def gene_model(geneName):
    geneName = geneName.upper()
    fig = plt.figure()
    ax = fig.add_subplot(111)

    trptNum = 0
    for trpt, exon in GRCh38Exon[geneName].items():
        trptNum += 1
        if exon[0] == '+':
            col = 'limegreen'
        elif exon[0] == '-':
            col = 'magenta'

        for i in range(1,len(exon),2):
            rect = Rectangle((exon[i], trptNum-0.1), exon[i+1]-exon[i], 0.2, color = col, fill = True)
            ax.add_patch(rect)

            if i < len(exon)-2:
                introLength = exon[i+2]-exon[i+1]
                #ax.plot([exon[i+1],exon[i+2]],[trptNum,trptNum],color = 'black',linewidth=1)

                if exon[0] == '+':
                    if introLength <500:
                        ax.arrow(exon[i+1],trptNum,introLength*0.9,0,head_width=0.03,
                                 head_length=introLength*0.1,fc='k',ec='k')
                    else:
                        ax.arrow(exon[i+1],trptNum,introLength-50,0,head_width=0.03,
                                 head_length=50,fc='k',ec='k')
                elif exon[0] == '-':
                    if introLength <500:
                        ax.arrow(exon[i+2],trptNum,introLength*0.9,0,head_width=0.03,
                                 head_length=introLength*0.1,fc='k',ec='k')
                    else:
                        ax.arrow(exon[i+2],trptNum,introLength-50,0,head_width=0.03,
                                 head_length=50,fc='k',ec='k')

    trptNum = 0
    for trpt, utr in GRCh38UTR[geneName].items():
        trptNum += 1

        if utr == []:
            continue

        for j in range(0,len(utr),2):
            rect = Rectangle((utr[j],trptNum-0.1),utr[j+1]-utr[j],0.2,color='black',fill=True)
            ax.add_patch(rect)

    ax.set_xlabel(geneName,color='blue',fontsize=14,fontweight='bold')
    ax.yaxis.set_major_locator(ticker.FixedLocator(range(1,trptNum+1)))
    ax.set_yticklabels(GRCh38Exon[geneName].keys(),fontweight='bold')

    plt.xlim(geneCord[geneName])
    plt.ylim([0,trptNum+0.5])

    plt.show()

if __name__ == '__main__':
    main()