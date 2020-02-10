import sys
import numpy as np
from math import exp
import random

###########################################################################
#File preprocessing
###########################################################################
#the aFloat function see whether a value can be converted to a float or not
def aFloat(i):
 try:
  float(i)
  return True
 except(VlaueError):
  return False

#the binarize function binarizes the input file
def binarize(file,name):
 stored={}
 dict={}
 countdict={}
 percentdict={}
 for ln in file:
  ln=ln.strip("\r\n")
  ln=ln.split(",")
  natt=len(ln)-1
  clas=ln[-1]
  arry=ln[:-1]
  vals=[clas]
  #each dataset has its specific cutoff values for the cutoff between 0 and 1
  # this is determined by the distribution of each attribute
  if "breast" in name:
   cuto=[3,3,3,3,3,3,3,3,3]
  if "iris" in name:
   cuto=[6,3,5,1]
  if "soybean" in name:
   cuto=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
  if "glass" in name:
   cuto=[1.517,12,3,1.6,73,0.5,9,0.1,0.01]
  #if the attribute values are not y/n then they get assigned to their value in this loop
  if "vote" not in name:
   for i in arry:
    u=arry.index(i)
    if aFloat(i) == True:
     i=float(i)
    if i > cuto[u]:
     vals.append(1)
    else:
     vals.append(0)
  #if the attribute values are y/n then they get assigned to their value in this loop
  if "vote" in name:
   ip=0
   for i in arry:
    ip+=1
    if i == "y":
     vals.append(1)
    elif i == "n":
     vals.append(0)
    #if an attribute value is a "?"
    elif i == "?":
     if ip%2==0:        #give it a zero if the counter is even
      vals.append(0)
     else:
      vals.append(1)    #give it a one if the counter is odd
  if clas not in stored:
   stored[clas]=[vals]      #this stores all the datpoints
   dict[clas]=[]            #this stores a dictionary with classes, which will be used in Naive Bayes
   countdict[clas]=[]       #this stores a dictionary with classes, which will be used in Naive Bayes
   percentdict[clas]=[]     #this stores a dictionary with classes, which will be used in Naive Bayes
  else:
   stored[clas].append(vals)
 return (stored,dict,countdict,percentdict)   #returns all the dictionaries generated

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
  for p in par:    #for partition in partitions
   if p != i:      #if the partition is not the partition used for the testSet
    for l in par[p]:  #for each line in that partition
     trainSet.append(l)  #add the line to the training set
  rounds[i]=[trainSet,testSet] 
 return rounds

#########################################################################
#NAIVE BAYES
#########################################################################
#The bayesTrain function calculates the percentages from the training set
def bayesTrain(trainset,dict,countdict,percentdict):
 natt=len(trainset[0])-1            #get the number of attributes
 for sample in trainset:            #generate a dictionary with class as the key
  dict[sample[0]].append(sample[1:])
 for clas in dict:          #for each class
  tot=len(dict[clas])       #get the total number of data points
  zeros=[]                 
  ones=[]
  for i in range(0,natt):   #add the data point to either zero or one
   zeros.append(0)
   ones.append(0)
  for sample in dict[clas]:
   for index in range(0,natt):  #count the number of zeros and ones for each attribute
    if sample[index]==0:
     zeros[index]+=1
    else:
     ones[index]+=1 
  countdict[clas]=[zeros,ones,tot]  #store the number of zeros and one and the total number in countdict
 for clas in countdict:
  for l in range(0,2):
   percentages=[]
   for i in countdict[clas][l]:
    percentage=i/countdict[clas][2]      #calculate the percentage of zeros and ones
    if percentage==0:
     percentage=0.00000001
    percentages.append(percentage)
   percentdict[clas].append(percentages)  #store them in percetdict   
 return (natt,percentdict)

#the naiveBayes function calculates the percentage of class 0 and 1 for each sample in the testing set
#then it compares the percentages and choose the class with a higher percentage 
def naiveBayes(percentages,testset,numofatt,n):
 oname=n+"_naivebayes.csv"               #generates an output file
 output=open(oname,"w")
 row=("expected class"+","+"predicted class"+","+"accuracy"+"\r\n")
 output.write(row)
 right=0      #initiate counter for right and wrong classification
 wrong=0
 #this stores the percentages to be multipled in each class
 classes={}
 for sample in testset:     
  expectedclas=sample[0]
  if expectedclas not in classes:
   classes[expectedclas]=[]
  for i in range(1,numofatt):
   if sample[i]==0:
    for clas in classes:
     classes[clas].append(percentages[clas][0][i])
   else:
    for clas in classes:
     classes[clas].append(percentages[clas][1][i])
  prodict=[]        #stores the product of the percentage
  for clas in classes:
   val=np.prod(classes[clas])
   prodict.append((clas,val))
  #sort the product list by the percentage value
  def takeSecond(elem):
    return elem[1]
  prodict.sort(key=takeSecond,reverse=True)  #sort the product list 
  predictclas=prodict[0][0]    #the one with the largest percentage
  #check whether the class is accurate or not
  if predictclas == expectedclas:
   accuracy='accurate'
   right+=1
  else:
   accuracy='inaccurate'
   wrong+=1
  row=(str(expectedclas)+","+str(predictclas)+","+accuracy+"\r\n")
  output.write(row)
 row=("total right ones: "+ ","+str(right)+"\r\n")
 output.write(row)
 row=("total wrong ones: "+ ","+str(wrong)+"\r\n")
 output.write(row)

#######################################################################
#LOGISTIC REGRESSION
#######################################################################
# The sigmoid function determines the prediction results
def sigmoid(t,weights):
  o= weights[0]
  for j in range(len(t)-1): #for each attribute
   if t[j] == 1 or t[j]==0:  #just to check the input is binary
    o= o+weights[j+1]*t[j]
  if o < 0:                   #what to return when o is negative
    return 1 - 1/(1 + exp(o))
  else:                       #what to return when o is negative
    return 1/(1 + exp(-o))
 
# The gradientDesent function determines the weights for logistic regression
def gradientDesent(train, l_rate,one):
 #initiate the weights randomly
 weights = [random.uniform(-0.01,0.01) for i in range(len(train[0]))]
 for iteration in range(500):     #assumes that it converges after 500 rounds
  for t in train:
   c=t[0]
   if c == one:    #see whether the class is one or zero
    c=1
   else:
    c=0
   t=t[1:]
   y= sigmoid(t, weights) #get the predicted output from the sigmoid function
   error=c-y             #calculate the error
   weights[0] = weights[0]+l_rate*error*y    #calculate the weight for the first attribute
   for j in range(len(t)-1):                 #calculate the weights for the following attributes
    weights[j+1] = weights[j+1]+l_rate*error*y*t[j]
 return weights   #return the list of weights

def classify(l_rate,classcut,one,name):
 oname=name+"_LogisticRegression_Adaline.csv"               #generates an output file
 output=open(oname,"w")
 row=("class one is "+str(one)+"\r\n")
 output.write(row)
 row=(" "+","+"Logistic Regression"+","+" "+","+" "+","+"Adaline"+","+" "+","+" "+","+" "+"\r\n")
 output.write(row) 
 row=("expected class"+","+"predicted value"+","+"predicted class"+","+"accuracy"+","+"expected class"+","+"predicted value"+","+"predicted class"+","+"accuracy"+"\r\n")
 output.write(row)
 weights=gradientDesent(trainSet,l_rate,one) #get the list of weights from gradientDesent
 aweights=Adaline(trainSet,l_rate,one,natt)  #get the list of weights from Adaline
 rl=0
 wl=0
 ra=0
 wa=0
 tot=0
 for row in testSet:  #for every sample in testSet
  tot+=1
  clas=row[0] 
  if clas == one:  #see whether the class is one or zero
   c=1
  else:
   c=0
  t=row[1:]        #the rest would be attribute values
  y = sigmoid(t, weights)  #predict the output using logistic regression
  ay= sigmoid(t,aweights)  #predict the output using Adaline 
  if y > classcut:       #if the output is above the class cutoff, assign it a one
   predictclasl=1
  else:
   predictclasl=0         #if the output is above the class cutoff, assign it a zero
  if ay > classcut:       #if the output is above the class cutoff, assign it a one
   predictclasa=1
  else:
   predictclasa=0         #if the output is above the class cutoff, assign it a zero
  if predictclasl == c:
   accul='accurate'
   rl+=1
  else:
   accul='inaccurate'
   wl+=1
  if predictclasa == c:
   accua='accurate'
   ra+=1
  else:
   accua='inaccurate'
   wa+=1
  row=("%d,%.10f,%d,%s,%.10f,%d,%s" % (c, y, predictclasl,accul, y, predictclasa,accua))
  row= row+"\r\n"
  output.write(row) 
 row=("total right ones for logistic regression: "+ ","+str(rl)+"\r\n")
 output.write(row)
 row=("total wrong ones for logistic regression: "+ ","+str(wl)+"\r\n")
 output.write(row)
 percenterrl=float(wl)/float(tot)
 row=("percent of the wrong ones for logistic regression: "+ ","+str(percenterrl)+"\r\n")
 output.write(row)
 row=("total right ones for Adaline: "+ ","+str(ra)+"\r\n")
 output.write(row)
 row=("total wrong ones for Adaline: "+ ","+str(wa)+"\r\n")
 output.write(row)
 percenterra=float(wa)/float(tot)
 row=("percent of the wrong ones for logistic regression: "+ ","+str(percenterra)+"\r\n")
 output.write(row)
 return (percenterrl,percenterra)
  

###################################################################
#ADALINE
###################################################################
def Adaline(train,l_rate,one,natt):
 D=len(train)  #get the sample size
 #initiate the weights randomly
 weights = [random.uniform(-0.01,0.01) for i in range(len(train[0])+1)]
 errors=[]   #for storing the errors
 xnplusone=-1   #the xn+1 for calculating theta
 for i in range(15):   #number of iteration for it to converge
  for x in train:
   c=x[0]
   if c == one:    
    d=0
   else:
    d=1
   y=0
   if len(x) <= natt:      #add in the -1 as the xn+1 item
    x.append(xnplusone)
   x=x[1:]
   theta=weights[-1]       #get the last weight as theta
   for id in range(len(x)-1):
    y+= x[id]*weights[id]-theta   #sum of the output
   if y < 11:          #just in case y get too big for the square
    err=(d-y)**2       #mean square error
    weights[0] = weights[0]+(l_rate*err)/D  #I followed the lecture and did this
    for j in range(len(x)-1):
     #I try to follow the lecture and did this Widrow-Hoff
     weights[j+1] = weights[j]+(l_rate*sum(errors)*x[j])/D
    errors.append(err) #add the err to the error list
 return weights
###################################RUN########################################
file=open(sys.argv[1],"r")
fl=sys.argv[1].split(".")
name=fl[0]    #get the name of the input file
#define the learning rate and the class cutoff values for each dataset
if "breast" in name:              
 l_rate=0.0002
 classcut=0.65
 one="2"
if "vote" in name:
 l_rate=0.0002
 classcut=0.7
 one="republican"
if "iris" in name:
 l_rate=0.05
 classcut=0.5
if "glass" in name:
 l_rate=0.01
 cutlist=[0,0.56,0.5,0.2756,0,0.1,0.1,0.1]  #each attribute has different cutoff values
if "soybean" in name:
 l_rate=0.01
 classcut=0.5
dat=binarize(file,name)          #binarize the file
dict=dat[1]            #an empty dictionary with classes used in Naive Bayes
countdict=dat[2]       #an empty dictionary with classes used in Naive Bayes
percentdict=dat[3]     #an empty dictionary with classes used in Naive Bayes
par= splitData(dat[0]) 
rounds= Sets(par)      #returns a split data for five fold cross validation

#Five-fold cross validation
for i in range (0,5):
 r=i+1
 n=name+str(r)
 trainSet=rounds[i][0]
 testSet=rounds[i][1]
 trainbayes=bayesTrain(trainSet,dict,countdict,percentdict)
 natt=trainbayes[0]
 percentages=trainbayes[1]
 naiveBayes(percentages,testSet,natt,n)
 if len(dat[0]) == 2:
  classify(l_rate,classcut,one,n)
 elif len(dat[0]) > 2:    #if there are more than two classes
  for clas in dat[0]:
   nc=n+clas
   if clas == "Iris-versicolor":
    classcut=0.13
   if "glass" in name:  
    classcut=cutlist[int(clas)]
   for i in trainSet:
    if i[0] == clas:
     one= clas
     c=1
    else:
     c=0
   classify(l_rate,classcut,one,nc)
