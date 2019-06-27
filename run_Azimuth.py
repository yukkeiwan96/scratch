import sys
import numpy as np
import azimuth.model_comparison

def conSeq(seq):
 newseq=""
 for i in reversed(range(len(seq))):
  if seq[i] == "A":
   newseq+="T"
  if seq[i] == "T":
   newseq+="A"
  if seq[i] == "C":
   newseq+="G"
  if seq[i] == "G":
   newseq+="C"
 return newseq

name=sys.argv[1]
oname="azimuth"+name
file=open(name,"r")
outfile=open(oname,"w")
for ln in file:
 l=ln.split(",")
 if l[1][21:51][25:27] != "GG":
  GUIDE=np.array([l[1][20:50]])
 print(l[1][21:51][25:27])
 GUIDE=np.array([l[1][21:51]])
 CUT_SITE=np.array([23])
 PERCENT_PEPTIDE=np.array([-1])
 ON_TARGET=azimuth.model_comparison.predict(GUIDE,CUT_SITE,PERCENT_PEPTIDE)[0]
 row=ln.strip("\r\n")+","+str(ON_TARGET)+"\r\n"
 outfile.write(row)
outfile.close()
