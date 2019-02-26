import sys
import random
from functions import openFile, preGlass, preIris, preSpam, featureSet, kmeans, Silhouette, SFS

#spambase has 58 columns <- no missing attributes
#iris has 5 columns <- no missing attributes
#glass has 11 columns <- no missing attributes

rawdata=sys.argv[1]  #opens the dataset
numcol=int(sys.argv[2])

dat=openFile(rawdata,numcol)

if "spambase" in rawdata:
 Dlist= preSpam(dat)         
 numcla= 2
 name="spambase"
if "iris" in rawdata:
 Dlist= preIris(dat)          
 numcla= 3
 name="iris"
if "glass" in rawdata:
 Dlist= preGlass(dat)         
 numcla=7    
 name="glass"

F=featureSet(Dlist)

outdata=SFS(F,Dlist,numcla)

for t in outdata:
 print(t)
 table=open(name+"_f"+str(t[0])+".csv","w")
 firln=("File analyzed: "+rawdata+"\r\n")
 table.write(firln)
 secln=("The features generating the best kmeans clustering data was identified by Stepwise Forward Selection (SFS)"+"\r\n")
 table.write(secln)
 trdln=("Silhouette coefficient: "+str(t[1])+"\r\n")
 table.write(trdln)
 header=("Cluster's centriole"+","+"Data Points"+"\r\n")
 table.write(header)
 for r in range(0,numcla):
  a=t[2][r]
  for o in t[3][r]:
   row=(str(a)+","+str(o)+"\r\n")
   table.write(row)
table.close()
