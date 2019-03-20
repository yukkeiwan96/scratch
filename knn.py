import sys 
import math
import operator
#k value for the forestfire dataset is 13
#k value for the pubished performance of the machine dataset is 1
#k value for the estimated performance of the machine dataset is 1
#k value for the ecoli dataset is 1
#k value for the segmentation dataset is 1

####################FUNCTIONS####################################

#the openFile function reads open the input csv files
# and process each of the files accordingly
def openFile(rawdata):
 file=open(rawdata,"r")
 stored={}
 for ln in file:
  ln=ln.strip("\r\n")
  ln=ln.split(",")
  if "ecoli" in rawdata:           #if read in the ecoil dataset
   type="classification"           #the type of work knn will do
   line=list(map(float, ln[1:-1]))
   line.append(ln[-1])
   if ln[-1] not in stored:
    stored[ln[-1]]=[line]
   else:
    stored[ln[-1]].append(line)
  if "segmentation" in rawdata:   #if read in the segmentation dataset
   type="classification"          # the type of work knn will do
   line=list(map(float, ln[1:]))
   line.append(ln[0])
   if ln[0] not in stored:
    stored[ln[0]]=[line]
   else:
    stored[ln[0]].append(line) 
  if "forest" in rawdata:        #if read in the forest fire dataset
   type="regression"             # the type of work knn will do
   line=list(map(float,ln[4:-1]))
   line.append(float(ln[0]))
   line.append(float(ln[1]))
   #change the day and month of the data point to numeric values
   days=[0,"mon","tue","wed","thr","fri","sat","sun"]
   if ln[3] in days:
    d=days.index(ln[3])
    line.append(d)
   months=[0,"jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
   if ln[2] in months:
    m=months.index(ln[2])
    line.append(m)
   line.append(float(ln[-1]))
   if len(line)==13:
    if ln[2] not in stored:
     stored[ln[2]]=[line]
    else:
     stored[ln[2]].append(line)
  if "machine" in rawdata:      #if read in the machine dataset
   type="regression"            # the type of work knn will do
   line=list(map(float, ln[2:]))
   if ln[0] not in stored:
    stored[ln[0]]=[line]
   else:
    stored[ln[0]].append(line)  
 #returns a tupule the data and the type of work knn will do 
 return (stored,type)           

#the splitData function splits the data into five portions with equal number of data points
def splitData(dat):
 itemsTest={}
 partitions={}
 for i in dat:       #for each class in the dataset
  a=int(len(dat[i])/5)
  itemsTest[i]=[0,a,a*2,a*3,a*4,a*5]   #itemsTest stores the indecies of where the dataset will divide
 for b in range(0,5):   #this loop allocates the data points into each of the five partitions
  partition=[]
  for i in dat:        #for each class
   for a in range(itemsTest[i][b],itemsTest[i][b+1]): 
    partition.append(dat[i][a])  #append items from the start index to the end index of the partition 
  partitions[b]=partition  #partitions stores all five of the partitions
 return partitions

#the Sets function determines the training set and the test set for the five rounds of experiments
def Sets(par):
 rounds={} #rounds stores the training set for normal and condensed knn, and the testing set for all five rounds
 for i in range(0,5):
  testSet=par[i]   #testSet is a list of data points from one of the partitions
  trainSet=[]      #trainSet stores the remaining 80% of the data points
  ctrainSet={}     #ctrainSet is the dictionary version of the trainSet and is for condensed knn
  for p in par:    #for partition in partitions
   if p != i:      #if the partition is not the partition used for the testSet
    for l in par[p]:  #for each line in that partition
     trainSet.append(l)  #add the line to the training set
     if l[-1] not in ctrainSet:  #if the class is not the ctrainSet dictionary
      ctrainSet[l[-1]]=[l]   #initiate the class in ctrainSet and add in the line
     else:     #if the class has already been initiated
      ctrainSet[l[-1]].append(l)  #add in the line to the corresponding class
  rounds[i]=[trainSet,ctrainSet,testSet] 
 return rounds

#the Distance function calculates the Euclidian distances between one point to another
def Distance(point1,point2,parameters):
 distance=0
 #the loop adds up the distances from all the parameters
 for i in range(0,parameters): 
  distance+= pow((point1[i]-point2[i]),2)
 distance= math.sqrt(distance)
 return distance

#the knn function finds the nearest k neighbor(s) for each point in the testing set
def knn(trainSet,testSet,k,rawdata):
 results=[]
 for testpt in testSet: #each point in the testSet   
  #stores the distances between a test point to each of the points in the training set
  distances=[] 
  for trainpt in trainSet: 
   d= Distance(trainpt,testpt,len(testpt)-1) #calculate the distance between the two points
   if "machine" in rawdata:  #the machine data has 2 performance values
    distances.append((d,trainpt[-2],trainpt[-1])) #append the distance, the published, and estimated performance values
   else:  #one class is stored for the classification problem; the forestfire dataset only has one area estimate
    distances.append((d,trainpt[-1])) 
  distances.sort(key=operator.itemgetter(0)) #sort the distances based on the distance
  neighbors=[]
  #the following stores k number of neighbors of a point in the testing set
  if "machine" in rawdata:
   for x in range(k):
    neighbors.append((distances[x][1],distances[x][2]))
   results.append(((testpt[-2],testpt[-1]),neighbors))
  else:
   for x in range(k):
    neighbors.append(distances[x][1])
   results.append((testpt[-1],neighbors))
 #returns a results the the point from the testing set and all k of neighbors of the point
 return results

#the condensedknn function
def condensedknn(dat):
 Z=[] #stores the points put into z from each class
 distances=[] #stores the distances
 for c in dat: #for each class in the dataset
  z=[]   #initialize z
  for x in dat[c]:  #for each data point in the class
   if len(z)==0:  #if z is empty
    z.append(x)   #add the current data point to z
   else:  #if z is not empty
    for p in z:  #for every point in z
     d=Distance(x,p,len(x)-1)  #get the distance between the point in z and the 
     distances.append((x[-1],d)) #append the point and the distance
    distances.sort(key=operator.itemgetter(1)) #sort the distances
    if p[-1] != distances[0][0]:  #if the class of p does not equal to that of the nearest point to it
     z.append(x) #append the nearest point
   distances=[] 
  for e in z: #for all the points from class c that are added to z
   Z.append(e)  #append those to Z
 return Z 

#the regression function calculates the differences between the predicted value
# and the original value
def regression(results,rawdata):
 li=[]
 if "machine" not in rawdata:
  for e in results:
   original=e[0]
   predicted=sum(e[1])/len(e[1])
   difference=abs(original-predicted)
   re=[original,predicted,difference,e[1]]
   li.append(re)
 else:             #the machine dataset has two performance values
  for e in results:
   sump=0
   sume=0
   originalp=e[0][0]
   originale=e[0][1]
   for a in range(0,len(e[1])):
    sump+=e[1][a][0]
    sume+=e[1][a][1]
   predictedp=sump/len(e[1])
   predictede=sume/len(e[1])
   differencep=abs(originalp-predictedp)
   differencee=abs(originale-predictede)
   difference=(differencep,differencee)
   re= [originalp,predictedp,differencep,originale,predictede,differencee]
   li.append(re)
 return li

#the classificationError function calculates the percentage of wrong prediction
# in the testing set
def classificationError(results):
 li=[]
 for e in results:
  original=e[0]
  neighbors=e[1]
  percentError=1-(neighbors.count(original)/len(neighbors))
  li.append([percentError,original,neighbors])
 return li

###########################RUN##########################
rawdata=sys.argv[1]  #input the name of the file
raw=rawdata.split(".")
ra=raw[0]
file=openFile(rawdata)
if "machine" in rawdata:
 k=1
if "forest" in rawdata:
 k=13
if "ecoli" in rawdata:
 k=1
if "segmentation" in rawdata:
 k=1
dat=file[0]
type=file[1]
par=splitData(dat)
rounds= Sets(par)
#for i in range(1,26): #for finding the best k value
stora={}
storb={}
for r in rounds:
 trainSet=rounds[r][0]
 ctrainSet=rounds[r][1]
 con=condensedknn(ctrainSet)
 testSet=rounds[r][2]
 if "classification" in type:
  results=knn(trainSet,testSet,k,rawdata)
  conresults=knn(con,testSet,k,rawdata)
  clasi=classificationError(results)
  conclasi=classificationError(conresults)
  stora[r]=clasi
  storb[r]=conclasi
 if "regression" in type:
  results=knn(trainSet,testSet,k,rawdata)
  regress=regression(results,rawdata)
  stora[r]=regress

if "classification" in type:
  faname=ra+"knn.csv"
  fbname=ra+"condensedknn.csv"
  outfilea=open(faname,"w")
  outfileb=open(fbname,"w")
  meanerrs=[]
  for r in stora:
   t=r+1
   outfilea.write("k value is "+str(k)+"\r\n")
   outfilea.write("round "+str(t)+"\r\n")
   outfilea.write("percent error"+","+"original class"+","+"predicted class"+"\r\n")
   rsum=0
   for j in stora[r]:
    outfilea.write(str(j[0])+","+j[1]+","+j[2][0]+"\r\n")
    rsum+=j[0]
   rsum=rsum/len(stora[r])
   meanerrs.append(rsum)
  me=sum(meanerrs)/5
  outfilea.write("mean error: "+","+str(me)+"\r\n")
  for r in storb:
   t=r+1
   outfileb.write("k value is "+str(k)+"\r\n")
   outfileb.write("round "+str(t)+"\r\n")
   outfileb.write("percent error"+","+"original class"+","+"predicted class"+"\r\n")
   rsum=0
   for j in stora[r]:
    outfileb.write(str(j[0])+","+j[1]+","+j[2][0]+"\r\n")
    rsum+=j[0]
   rsum=rsum/len(stora[r])
   meanerrs.append(rsum)
  me=sum(meanerrs)/5
  outfileb.write("mean error: "+","+str(me)+"\r\n")
  outfilea.close()
  outfileb.close()
if "forestfire" in rawdata:
  faname=ra+"knn.csv"
  outfilea=open(faname,"w")
  meanerrs=[]
  for r in stora:
   t=r+1
   outfilea.write("k value is "+str(k)+"\r\n")
   outfilea.write("round "+str(t)+"\r\n")
   outfilea.write("difference"+","+"original"+","+"predicted"+"\r\n")
   rsum=0
   for j in stora[r]:
    outfilea.write(str(j[2])+","+str(j[0])+","+str(j[1])+"\r\n")
    rsum+=j[0]
   rsum=rsum/len(stora[r])
   meanerrs.append(rsum)
  me=sum(meanerrs)/5
  outfilea.write("mean error: "+","+str(me)+"\r\n")
  outfilea.close()
if "machine" in rawdata:
  faname=ra+"knn.csv"
  outfilea=open(faname,"w")
  meanerrs=[]
  meane=[]
  for r in stora:
   t=r+1
   outfilea.write("k value is "+str(k)+"\r\n")
   outfilea.write("round "+str(t)+"\r\n")
   outfilea.write("published"+","+""+","+""+","+"estimated"+","+""+","+""+"\r\n")
   outfilea.write("difference"+","+"original"+","+"predicted"+","+"difference"+","+"original"+","+"predicted"+"\r\n")
   rsump=0
   rsume=0
   for j in stora[r]:
    outfilea.write(str(j[2])+","+str(j[0])+","+str(j[1])+","+str(j[5])+","+str(j[3])+","+str(j[4])+"\r\n")
    rsump+=j[0]
    rsume+=j[3]
   rsump=rsump/len(stora[r])
   rsume=rsume/len(stora[r])
   meanerrs.append(rsump)
   meane.append(rsume)
  me=sum(meanerrs)/5
  mee=sum(meane)/5
  outfilea.write("mean error for published performance: "+","+str(me)+"\r\n")
  outfilea.write("mean error for estimated performance: "+","+str(mee)+"\r\n")
  outfilea.close()
  
#finding the best k-value
#  if "machine" not in rawdata:
#   meanerrs=[]
#   for r in stor:
#    meanerrs.append(stor[r][0])
#   me=sum(meanerrs)/5
#   mei.append((i,me))                 #for finding the best k value
#   mei.sort(key=operator.itemgetter(1))  
#   print(mei[0])                       
#   row=(str(meanerrs[0])+","+str(meanerrs[1])+","+str(meanerrs[2])+","+str(meanerrs[3])+","+str(meanerrs[4])+","+str(me)+"\r\n")
#  else:
#   meanerra=[]
#   meanerrb=[]
#   for r in stor:
#    meanerra.append(stor[r][0])
#    meanerrb.append(stor[r][1])
#   mea=sum(meanerra)/5
#   meb=sum(meanerrb)/5
#   mei.append((i,meb))                 #for finding the best k value
#   mei.sort(key=operator.itemgetter(1))

