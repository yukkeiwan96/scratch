import sys
import random
from math import exp

###########################################################################
#File preprocessing
###########################################################################
#the aFloat function see whether a value can be converted to a float or not
def aFloat(i):
 try:
  float(i)
  return True
 except(ValueError):
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
  #each dataset has its specific cutoff values for the cutoff between 0 and 1
  # this is determined by the distribution of each attribute
  if "breast" in name:
   cuto=[3,3,3,3,3,3,3,3,3]
   allclas=["2","4"]
  if "iris" in name:
   cuto=[6,3,5,1]
   allclas=["Iris-setosa","Iris-versicolor","Iris-virginica"]
  if "soybean" in name:
   cuto=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
   allclas=["D1","D2","D3","D4"]
  if "glass" in name:
   cuto=[1.517,12,3,1.6,73,0.5,9,0.1,0.01]
   allclas=["1","2","3","5","6","7"]
  if "vote" in name:
   allclas=["republican","democrat"]
  clas=ln[-1]
  arry=ln[:-1]
  vals=[allclas.index(clas)]
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
  else:
   stored[clas].append(vals)
 return stored   

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

#######################################################################
#BACKPROPAGATION-TRAINED FEEDFORWARD NEURAL NETWORK
#######################################################################
#build the framework of the neural network
def buildNet(inNeurons, hidNeurons, outNeurons):
 Net=[]      #this stores the neural network
 hidLayer=[] #this stores the hidden layer
 outLayer=[] #this stores the output layer
 for i in range (hidNeurons):  #for each neuron in the hidden layer
  wl=[]
  for i in range (inNeurons+1):  #for each neuron in the input (previous) layer 
   a=0.0001         #generate a random number as weight
   wl.append(a)       #append the number to initialize the weight list
  wd={"weights":wl}   
  hidLayer.append(wd) #store the weight list in the hidden layer
 Net.append(hidLayer) #add the hidden layer to the neural network
 for i in range (outNeurons): #for each neuron in the output layer
  wl=[]
  for i in range (hidNeurons+1): #for each neuron in the hidden (previous) layer
   a=0.0001        #generate a random number as weight
   wl.append(a)       #append the number to initialize the weight list
  wd={"weights":wl}   
  outLayer.append(wd) #store the weight list in the output layer
 Net.append(outLayer) #add the output layer the neural network
 return Net      #return the initialize neural network

#sigmod function
def sigmod(o):
 return 1.0/(1.0 + exp(-o))

# feed forward neural network outputs the predicted output
def feedForward(inputs,neuralNet,function):
 for layer in neuralNet:   #for each layer in the neural network
  outputs= []
  for neuron in layer:     #for each neuron in the layer
   weights=neuron["weights"] 
   o= weights[-1]      #the bias
   for i in range (len(weights)-1): #for every weight
    o+= weights[i]*inputs[i]  
   if function == "sigmod":
    neuron['output']= sigmod(o)  #sigmoid function determines the prediction
   outputs.append(neuron['output'])
  inputs= outputs    #update the inputs for the next layer
 return inputs

# train and update the weights using back propagation
def BackPropagation(neuralNet, trainSet, epochs, l_rate, outNeurons, function):
 numLay=len(neuralNet)
 for epoch in range(epochs):        #use 250 epoch to train the neural network
  totErr= 0
  for datpt in trainSet:        #for each datapoint in the training set
   clas=datpt[0]                #identify the class
   preout= feedForward(datpt,neuralNet,function)  #predict the output using feedForward
   expout=[]                    #expout is a list of weights corresponding to each class
   for i in range (outNeurons): 
    expout.append(0)            #initiate the weights with zeros
   expout[clas] = 1             #assign a weight of 1 for the expected class
   for i in range (outNeurons):       #for all the output classes
    totErr+= (expout[i]-preout[i])**2  #add up the mean sq error of the prediction when compared to the expected
   #goes backwards through the layers
   for a in range(numLay):
    i=numLay-a-1               
    layer= neuralNet[i]
    errors= []
    if i != len(neuralNet)-1:    #if it is not the last layer of the neural network
     for n in range(len(layer)):  #for every neuron in the layer i
      error= 0
      for neuron in neuralNet[i+1]:   #for neuron in the next forward layer of the neural network
       error+= (neuron["weights"][n]*neuron["delta"]) #sum up the total error
      errors.append(error)            #store the error sum to errors
    else:                        #if it is the last layer of the neural network
     for n in range(len(layer)): #for every neuron in layer i
      neuron= layer[n]
      error=expout[n]-neuron["output"]  #calculate the error
      errors.append(error)             #store the error
    for n in range(len(layer)):  #for every neuron in layer i
     neuron = layer[n]
     neuron["delta"]= errors[n]*neuron["output"]*(1.0-neuron["output"]) #calculate delta sub i
   #goes forward through the layers
   for i in range (numLay): #for each layer
    values= datpt[1:]
    if i > 0:    #if it is the output layer
     values=[]
     for neuron in neuralNet[i-1]:  #for every neurons in the previous layer
      values.append(neuron["output"])  #add the neuron output to the list of feature values
    for neuron in neuralNet[i]:  #for every neuron in layer i
     for n in range(len(values)):   #for each feature value
      neuron['weights'][n]+= l_rate*neuron['delta']*values[n]  #update the weight of the feature
     neuron['weights'][-1]+= l_rate*neuron['delta']  #update the weight of the bias   

#######################################################################
#RADIAL BASIS FUNCTION NEURAL NETWORK  (NOT DONE)
####################################################################### 
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

#radial basis function
def RBF(sigma,x,xj):
 return exp((-1/(2*sigma**2))*(x-xj)**2)

###################################RUN########################################
file=open(sys.argv[1],"r")
fl=sys.argv[1].split(".")
name=fl[0]    #get the name of the input file
outname=name+"output.csv"
outfile=open(outname,"w")
###specifications for each input files############
if "vote" in name:
 l_rate=0.1
 epochs=100
 k=2
if "breast" in name:
 l_rate=0.1
 epochs=100
 k=2
if "iris" in name:
 l_rate=0.5
 epochs=100
 k=3
if "soybean" in name:
 l_rate=0.8
 epochs=500
 k=4
if "glass" in name:
 l_rate=0.5
 epochs=2000
 k=6
##################################################
dat=binarize(file,name)          #binarize the file
par= splitData(dat) 
rounds= Sets(par)      #returns a split data for five fold cross validation
#Five-fold cross validation
errl=[]
for i in range (0,5):
 row=("round"+str(i+1)+"\r\n")
 outfile.write(row)
 row=("expected"+","+"predicted"+"\r\n")
 outfile.write(row)
 trainSet=rounds[i][0]
 testSet=rounds[i][1]
 inNeurons=len(trainSet[0]) - 1
 hidNeurons=2
 outNeurons=len(set([row[0] for row in trainSet]))
 neuralNet=buildNet(inNeurons,hidNeurons,outNeurons)
 BackPropagation(neuralNet, trainSet, epochs, l_rate, outNeurons,"sigmod")
 wrong=0
 total=0
 for inputs in testSet:
  outputs=feedForward(inputs,neuralNet,"sigmod")
  prediction=outputs.index(max(outputs))
  total+=1
  if inputs[0] != prediction:
   wrong+=1
  row= (str(inputs[0])+","+str(prediction)+"\r\n")
  outfile.write(row)
 errate=float(wrong)/float(total)
 row=("error rate: "+","+str(errate)+"\r\n")
 outfile.write(row)
 errl.append(errate)
meansqerr=(sum(errl)/len(errl))**2
row=("mean sq error: "+","+str(meansqerr)+"\r\n")
outfile.write(row)
outfile.close()

##for RBF network########################################
ktrainSet=[]
for input in trainSet:
 clas=input[0]
 addup=sum(input[1:])
 ktrainSet.append(addup) 
runKmeans=kmeans(ktrainSet,k)
centrioles=runKmeans[0]
rbfNet=buildNet(inNeurons,1,1)  #builds an RBF network with one hidden node and output node