import pysam
import sys
import time

start = time.clock()
args = sys.argv
bases = ['A','G','T','C','N']
base_num = {}
for base in bases:
    base_num[base] = 0

hg19 = pysam.FastaFile(args[1])
for chr_id in hg19.references:
    seq = hg19.fetch(chr_id).upper()
    for base in bases:
	    base_num[base] = seq.count(base)
    SUM = sum(base_num.values())
    GC = seq.count('G') + seq.count('C')
    print chr_id
    for base,base_count in base_num.items():
	    print "%s : %d" % (base,base_count)
    print "GC : %.2f" % (GC*1.0/SUM)
    print "SUM : %d" % (SUM)
    print "\n"

end = time.clock()
print "Use %d s" % (end-start)
    
