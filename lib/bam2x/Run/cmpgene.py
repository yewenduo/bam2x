#!/usr/bin/env python
# Programmer : zhuxp
# Date: 
# Last-modified: 02-12-2014, 22:36:39 EST
VERSION="0.0.4"
import os,sys,argparse
from bam2x.Annotation import BED6 as Bed
from bam2x.Annotation import BED12 as Bed12
from bam2x import TableIO,Tools,IO
from bam2x import DBI
import signal
signal.signal(signal.SIGPIPE,signal.SIG_DFL)
import gzip
import time
def help():
    return "cmp region with gene set(bed12 format) "
def set_parser(p):
    ''' This Function Parse the Argument '''
    p.add_argument('-I','--input_format',dest="format",choices=TableIO.hclass.keys(),default="guess",type=str,help="input file format")
    p.add_argument('-g','--gene',dest="genetab",type=str,help="Gene File, BED12 Format ")
    p.add_argument('-u','--upstream',dest="upstream",type=int,default=3000,help="upstream bp number , default: 3000")
    p.add_argument('-d','--downstream',dest="downstream",type=int,default=3000,help="downstream bp number , default: 3000")
    
def run(local_args):
    '''
    IO TEMPLATE
    '''
    global args,out
    args=local_args
    out=IO.fopen(args.output,"w")
    fin=IO.fopen(args.input,"r")
    print >>out,"# This data was generated by program ",sys.argv[0]," (version: %s)"%VERSION,
    print >>out,"in bam2x ( https://github.com/nimezhu/bam2x )"
    print >>out,"# Date: ",time.asctime()
    print >>out,"# The command line is :"
    print >>out,"#\t"," ".join(sys.argv)
    gene=DBI.init(args.genetab,"binindex",cls="bed12");
    upstream_list=[]
    downstream_list=[]
    exons_list=[]
    introns_list=[]
    utr3_list=[]
    utr5_list=[]
    for g in gene:
        upstream_list.append(g.upstream(args.upstream));
        downstream_list.append(g.downstream(args.downstream));
        for e in g.Exons():
            exons_list.append(e)
        for i in g.Introns():
            introns_list.append(i)
        if not (g.utr3() is None):
            utr3_list.append(g.utr3())
        if not (g.utr5() is None):
            utr5_list.append(g.utr5())
    upstream=DBI.init(upstream_list,"binindex",cls="bed6")
    downstream=DBI.init(downstream_list,"binindex",cls="bed6")
    exons=DBI.init(exons_list,"binindex",cls="bed6")
    introns=DBI.init(introns_list,"binindex",cls="bed6")
    utr3=DBI.init(utr3_list,"binindex",cls="bed6")
    utr5=DBI.init(utr5_list,"binindex",cls="bed6")



    if args.format=="guess":
        args.format=IO.guess_format(args.input)
    for (i0,i) in enumerate(TableIO.parse(fin,args.format)):
        if i0==0:
            if isinstance(i,Bed12):
                print >>out,"#chr\tstart\tend\tname\tscore\tstrand\tthick_start\tthick_end\titem_rgb\tblock_count\tblock_sizes\tblock_starts\tgene\tupstream\tdownstream\texon\tintron\tutr3\tutr5"
            else:
                print >>out,"#chr\tstart\tend\tname\tscore\tstrand\tgene\tupstream\tdownstream\texon\tintron\tutr3\tutr5"

        print >>out,i,
        print >>out,"\t",toIDs(gene.query(i)),

        print >>out,"\t",toIDs(upstream.query(i)),
        print >>out,"\t",toIDs(downstream.query(i)),
        print >>out,"\t",toIDs(exons.query(i)),
        print >>out,"\t",toIDs(introns.query(i)),
        print >>out,"\t",toIDs(utr3.query(i)),
        print >>out,"\t",toIDs(utr5.query(i))

def toIDs(x):
    s=""
    for i in x:
            s+=i.id+","
    if s=="":
        s="0"
    return s





    
if __name__=="__main__":
    run()




