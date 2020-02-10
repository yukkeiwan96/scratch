import random

#the function openFile opens a file
#it requires the input of the file name and the number of columns in the file
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

#the featureSet function extracts all the features from 
#Dlist, which has features as its key
def featureSet(Dlist):
 F=[]
 for f in Dlist:
  F.append(f)
 return F

#the kmeans function takes data points from a feature and the number of
# classes indicated from the description of the data as its number of clusters
def kmeans(D,k):
 m=random.sample(D,k)  #initializes the means randomly
 m=list(map(float,m))
 clusters=[]           #stores all datapoints within each clusters
 for n in range(0,k):
  v=[m[n]]             #create a sublist for each of the means
  clusters.append(v)
 for x in D:            #for each datapoint in the dataset
  nc=[]
  for n in range(0,k):     #compares the datapoint to all the means
   dist=abs(float(x)-m[n])  #finds its absolute distance to all the means
   nc.append(dist)          #appends all of the distance to a list
  locx=nc.index(min(nc))    #find the minimum distance in the list
  clusters[locx].append(float(x))  #append the the minimum distance to the right cluster
 kmeans=[]
 for v in clusters:      
  new=sum(v)/len(v)    #average the points of the clusters
  kmeans.append(new)   #append it to the centroids
 return (kmeans,clusters)  #return the centroid values and the datapoints in the cluster

#the Silhouette function measures the performance of the clustering
#Required input: datapoints from all of the clusters
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

#the SFS functions apply Stepwise Forward Selection to determine the features
# that generates the best clustering data
#Required inputs: feature set, a dictionary of datapoints in a feature, and the number of classes defined in the data
def SFS(F,Dlist,numcla):
 Fzero=[]
 basePerf=-100000      #initializes the base performance to a very low number
 bestPerf=-100000      #initializes the best performance to a very low number
# while len(F) > 0:    #loop through the process until no feature is left in F
 #the while loop took really long and therefore I ran the for loop below
 #Looped 100 times for the iris and glass data and 10 times for the spambase data
 for i in range(0,100): #I defined a finite number of loops instead of using the while loop
  for f in F:          #for each feature in feature set
   fIndex=F.index(f)   #indentify where the feature locates in the feature set
   h=kmeans(Dlist[fIndex],numcla) #find the clusters formed in the feature
   currentPerf=Silhouette(h[1]) #determine the clustering performance
   if currentPerf > bestPerf:  #if the current performance is better than the best performance
    bestPerf= currentPerf  #the current performance will then be the best performance
    bestF= f               #the best feature will be f
  if bestPerf>basePerf:    #if the best performance is better than the base performance
   basePerf=bestPerf       #the best performance will be the base performance
   F.remove(bestF)         #removes the best feature from the feature set
   Fzero.append((bestF,currentPerf,h[0],h[1])) #add best feature to the empty feature set
 return Fzero
