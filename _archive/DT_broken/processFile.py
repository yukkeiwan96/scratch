import operator
import math

#the openFile function reads open the input csv files
# and process each of the files accordingly
def openFile(rawdata):
 file=open(rawdata,"r")
 stored={}
 for ln in file:
  ln=ln.strip("\r\n")
  ln=ln.split(",")
  if "car" in rawdata:            #if read in the car dataset
   type="classification"          # the type of work the decision tree will do
   rootnode = {'index': 5, 'right': 'unacc', 'value': 'low', 'left': 'unacc'}
   if ln[-1] not in stored:
    stored[ln[-1]]=[ln]
   else:
    stored[ln[-1]].append(ln)
  if "segmentation" in rawdata:   #if read in the segmentation dataset
   type="classification"          # the type of work the decision tree will do
   rootnode = {'index': 1, 'right': 'SKY', 'value': '197', 'left': 'FOLIAGE'}
   line=list(map(float, ln[1:]))
   line=["%.i" % x for x in line] 
   line.append(ln[0])
   if ln[0] not in stored:
    stored[ln[0]]=[line]
   else:
    stored[ln[0]].append(line)
  if "abalone" in rawdata:        #if read in the abalone dataset
   type="classification"          #the tyoe if work the decision tree will do
   rootnode = {'index': 3, 'right': '7', 'value': '0.2', 'left': '3'}
   line=list(map(float,ln[1:-1]))
   line=["%.1f" % x for x in line] 
   line.append(ln[0])
   line.append(int(ln[-1]))
   if ln[-1] not in stored:
    stored[ln[-1]]=[line]
   else:
    stored[ln[-1]].append(line)
  if "wine" in rawdata:           #if read in the wine dataset
   type="regression"              #the type of work the decision tree will do
   line=list(map(float,ln[1:]))   
   line.append(ln[0])             
   if ln[0] not in stored:
    stored[ln[0]]=[line]
   else:
    stored[ln[0]].append(line)
  if "forest" in rawdata:        #if read in the forest fire dataset
   type="regression"             # the type of work the decision tree will do
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
   type="regression"            # the type of work the decision tree will do
   line=list(map(float, ln[2:]))
   if ln[0] not in stored:
    stored[ln[0]]=[line]
   else:
    stored[ln[0]].append(line)  
 #returns a tupule the data and the type of work the decision tree will do 
 return (stored,type,rootnode)           

#the splitData function splits the data into five portions with equal number of data points
def splitData(dat):
 itemsTest={}
 partitions={}
 for i in dat:       #for each class in the dataset
  v=int(len(dat[i])/10)
  a=int((len(dat[i])*0.9)/5)
  itemsTest[i]=[0,v,v+a,v+(a*2),v+(a*3),v+(a*4),v+(a*5)]   #itemsTest stores the indecies of where the dataset will divide
 for b in range(0,6):   #this loop allocates the data points into each of the five partitions
  partition=[]
  for i in dat:        #for each class
   for a in range(itemsTest[i][b],itemsTest[i][b+1]): 
    partition.append(dat[i][a])  #append items from the start index to the end index of the partition 
  partitions[b]=partition  #partitions stores all six of the partitions
 return partitions

#the Sets function determines the training set and the test set for the five rounds of experiments
def Sets(par):
 rounds={} #rounds stores the training set and the testing set for all five rounds
 for i in range(1,6):
  testSet=par[i]   #testSet is a list of data points from one of the partitions
  trainSet=[]      #trainSet stores the remaining 80% of the data points
  for p in par:    #for partition in partitions
   if p != i:      #if the partition is not the partition used for the testSet
    for l in par[p]:  #for each line in that partition
     trainSet.append(l)  #add the line to the training set
  rounds[i]=[trainSet,testSet] 
 return rounds

#the calcGain function calculates the gain of each attribute
def calcGain(trainSet):
  classdic={}
  numfeatures=len(trainSet[0])   #total number of features
  totdatpts=len(trainSet)          #total number of datapoints
  for i in trainSet:               #for each data point in trainSet
   if i[-1] not in classdic:       #if class is not in classdic yet
    classdic[i[-1]]=[i[:-1]]       #add the class as key and store the datapoint
   else:                           #else
    classdic[i[-1]].append(i[:-1]) #append the datapoint to the class
  oI =0                             #calculates the overall entropy from the dataset
  for c in classdic:               #for each class in classdic:
   f=len(classdic[c])/totdatpts    
   i=-f*math.log(f,2)
   oI+=i                           #add up all the entropies -> I
  features={}                      #initiate a feature dictionary
  for f in range(0,numfeatures-1):   #for each feature
     fcdic={}                        #initiate a dictionary for one feature only
     for c in classdic:              #for each class
      for p in classdic[c]:          #for each data point in the class
       if c not in fcdic:            #if the class is not a key in fcdic
        fcdic[c]=[p[f]]              #initiate the key and add the feature value of the datapoint
       else:                         #if class is already a key in fcdic
        fcdic[c].append(p[f])        #add the feature value to the class
     features[f]=fcdic            #this dic has feature as key and the feature values sorted in class
  xdic={}
  for f in features:               #for each feature
   tov={}
   totv={}
   for c in features[f]:           #for each class in the feature
    for v in features[f][c]:       #for each value in the feature with the class
     if v not in totv:             #if the value is not in the totv dic
      totv[v]=[c]                  #add the value to the dic with its corresponding class
     else:
      totv[v].append(c)
   for v in totv:                    #for each value in totv dic
    I=0                              #initiate I
    tov[v]=[len(totv[v])/totdatpts]  #this is the fraction that will multiply with the entropy
    for c in features[f]:            #for each class in a feature
     i=totv[v].count(c)/len(totv[v])  #count the values in the same class and divide it by the tot # of values
     if i==0:
      i=0.00000001
     b=-i*math.log(i,2)            
     I+=b                           #add up the total entropy
    tov[v].append(I)
   xdic[f]=tov
  gain=[]
  for att in xdic:                  #for each attribute
   E=0                              #initiate the expected entropy
   for v in xdic[att]:              
    E+=(xdic[att][v][0]*xdic[att][v][1])  #add up the multiplied entropies
   gain.append((att,oI-E))          #add the attribute with its gain to the gain list
  def takeSecond(elem):
    return elem[1]
  gain.sort(key=takeSecond,reverse=True)  #sort the gain list 
  return gain[0]         #returns the gain

