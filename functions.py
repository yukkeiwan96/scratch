import random

def openFile(rawdata,numcol):
 file=open(rawdata,"r")
 stored={}
 for ln in file:
  ln=ln.strip("\r\n")
  ln=ln.split(",")
  for n in range(0,numcol):
   if n not in stored:
    stored[n]=[ln[n]]
   else:
    stored[n].append(ln[n])
 return stored


#the following three functions are to remove the columns that are
#the sample number and the associated class from the data.
def preGlass(dat):
 del dat[0]  #removes sample number
 del dat[10] #removes associated class
 newdat={}
 for i in range(1,10):
  newdat[i-1]=dat[i]
 return newdat

def preIris(dat):
 del dat[4] #removes associated class
 return dat

def preSpam(dat):
 del dat[57] #removes associated class
 return dat

def featureSet(Dlist):
 F=[]
 for f in Dlist:
  F.append(f)
 return F


def kmeans(D,k):
 m=random.sample(D,k)
 m=list(map(float,m))
 clusters=[]
 for n in range(0,k):
  v=[m[n]]
  clusters.append(v)
 for x in D:
  nc=[]
  for n in range(0,k):
   dist=abs(float(x)-m[n])
   nc.append(dist)
  locx=nc.index(min(nc))
  clusters[locx].append(float(x))
 kmeans=[]
 for v in clusters:
  new=sum(v)/len(v)
  kmeans.append(new)
 return (kmeans,clusters)

def Silhouette(clusters):
 svalues=[]
 numCluster=len(clusters)
 curloc=0
 otherIndex=[]              
 for cluster in clusters:      #1st loop: loop through each of the cluster in the list of all clusters
  for i in range(0,numCluster):      #find the cluster(s) that's not the current one
   if i != curloc:
    otherIndex.append(i)
  others = [clusters[i] for i in otherIndex] #create a list of the clusters' indices
#  for o in others:    
#   print(o[0:5])
#  print(cluster[0:5])
  curloc+=1             #move the location to the next cluster in the 1st loop
  otherIndex=[]         #default the index list for other cluster(s)
  inCluster=[]          #initiates a list storing all the average distance inside a cluster
  outCluster=[]         #initiates a list storing all the average distance outside a cluster
  loc=0                 #a counter that specify the location of a point with in a cluster
  for p in cluster:     #2nd loop: looping through all the points in a cluster
   ptot=[]              #initializes a list for point-to-point distances
   otot=[]
   temp=cluster         #set a temporary list of all the points in the cluster,
   del temp[loc]        # and delete the current point
   for x in temp:       #3rd loop: compares the current point to all other points
    dist=abs(p-x)       #get the absvalue of the distance between the current point with others
    ptot.append(dist)   #append to the point-to-point distance list
   if len(ptot)>1:
    pavg=sum(ptot)/len(ptot)  #get the average distance from the list
   else:
    pavg=sum(ptot)/0.000000001
   inCluster.append(pavg)    #append the average of that point to the list storing average distance
   otherL=[]            
   for other in others: #loops through all the other cluster(s)
    for y in other:     #loops through all the points in a cluster
     dist=abs(p-y)      #get the absvalue of the distance between the current point with a point from another cluster
     otot.append(dist)  #append to the point-to-point distance list 
    if len(otot) > 1:
     oavg=sum(otot)/len(otot)  #get the average distance from the list 
    else:
     oavg=sum(otot)/0.00000001
    outCluster.append(oavg)   #append the average of that point to the list storing average distance
    otherL.append(outCluster) #appending a list of point-to-point distances between the current cluster to the current other cluster
   loc+=1               #moving to the point in the next position
  outC=[]
  if len(otherL)>1:
   en=len(otherL[1])
   for pa in range(0,en-1):
    if otherL[0][pa] >= otherL[1][pa]:
     outC.append(otherL[1][pa])
    elif otherL[0][pa] < otherL[1][pa]:
     outC.append(otherL[0][pa])
  elif len(otherL) == 1:
   outC=otherL[0]
  allpts=len(inCluster)
  for i in range(0,allpts-1):
   if outC[i] >= inCluster[i]:
    maxi= outC[i]
   elif outC[i] < inCluster[i]:
    maxi= inCluster[i]
   if maxi == 0:
    maxi=0.0000001
   s=((outC[i]-inCluster[i])/maxi)
   svalues.append(s)
 scoef=sum(svalues)/len(svalues)
 return scoef


def SFS(F,Dlist,numcla):
 Fzero=[]
 basePerf=-100000
 bestPerf=-100000
# while len(F) > 0:
 for i in range(0,100):
  print(i)
  for f in F:
   fIndex=F.index(f)
  # Fzero.append(f)
   h=kmeans(Dlist[fIndex],numcla)
   currentPerf=Silhouette(h[1])
   if currentPerf > bestPerf:
    bestPerf= currentPerf
    bestF= f
  if bestPerf>basePerf:
   basePerf=bestPerf
   F.remove(bestF)
   Fzero.append((bestF,currentPerf,h[0],h[1])) 
 return Fzero


