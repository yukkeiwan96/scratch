import sys
import random
#a python script named function.py stores all the functions for thisproject
from functions import openFile, preGlass, preIris, preSpam, featureSet, kmeans, Silhouette, SFS

#spambase has 58 columns <- no missing attributes
#iris has 5 columns <- no missing attributes
#glass has 11 columns <- no missing attributes

rawdata=sys.argv[1]  #input the name of the file
numcol=int(sys.argv[2]) #input the number of column of the file

dat=openFile(rawdata,numcol)  #open the file

#the following three if-statement specify the preprocessing required for
# each of the inputs, the number of classes defined, and the name that will
# be used in the output file.
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

F=featureSet(Dlist)  #extracts the feature set

outdata=SFS(F,Dlist,numcla)   #use the SFS function to select the best clustering features

#the following outputs a file for each of  the well-clustered features identified by SFS
# the file includes the input file
# the clustering methods and the feature selecion process
# the Silhouette coefficient
# each centroid and the data points in the cluster
for t in outdata:
 table=open(name+"_f"+str(t[0])+".csv","w")
 firln=("File analyzed: "+rawdata+"\r\n")
 table.write(firln)
 secln=("The features generating the best kmeans clustering data was identified by Stepwise Forward Selection (SFS)"+"\r\n")
 table.write(secln)
 trdln=("Silhouette coefficient: "+str(t[1])+"\r\n")
 table.write(trdln)
 header=("Cluster's centroid"+","+"Data Points"+"\r\n")
 table.write(header)
 for r in range(0,numcla):
  a=t[2][r]
  for o in t[3][r]:
   row=(str(a)+","+str(o)+"\r\n")
   table.write(row)
table.close()
