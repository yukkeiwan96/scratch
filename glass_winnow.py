import numpy as np
import random
#this opens a raw data file
file=open("glass.data","r")

#the aFloat function distinguishes whether a value is a float or not
def aFloat(i):
 try:
  float(i)
  return True
 except ValueError:
  return False

#the binarize function binarizes the raw data
def binarize(file):
 dict={}
 for ln in file:
  ln=ln.strip("\n")
  ln=ln.split(",")
  sample=ln[0]
  clas=ln[-1]
  if clas == '1' or clas=='2' or clas=='3': 
   clas=0     #class 0 is for window glass      
  elif clas =='5'or clas =='6' or clas=='7': 
   clas=1     #class 1 is for  non-window glass
  raw=ln[1:-1]
  dat=[]
  #values above the mean will be 1s and below the mean will be 0s
  meanlist=[1.5184,13.4079,2.6845,1.4449,72.6509,0.4971,8.9570,0.1750,0.0570]
  for index in range(0,9):
   if aFloat(raw[index])==True:
    i=float(raw[index])
    if i < meanlist[index]:
     i= 0
    else:
     i= 1
   dat.append(i)
  if len(dat)== 9:
   arr=np.asarray(dat)
   dict[sample]=[clas,arr]   
 return dict

data=binarize(file)

#splitting the data into training and testing sets
def splitdata(data):
 trainsize=2*(int(len(data)/3))   #2/3 of the data will be the training set
 intrain=random.sample(list(data), trainsize) #randomly select the 2/3s of the data
 trainset=[]
 testset=[]
 for item in data:     #this sorts the sample into either the training or testing sets
  if item in intrain:
   trainset.append(data[item])
  else:
   testset.append(data[item])
  sets=(trainset,testset)
 return sets

trainset=splitdata(data)[0]
testset=splitdata(data)[1]

#the winnowTrain funtion calculates the weight corresponding to each attribute
def winnowTrain(trainset):
 alpha=2
 weights=[]
 for n in range(0,len(trainset[1][1])):  #this generates the starting weight for each attribute
  weights.append(1)                   #the starting weight is 1, which demoting will be the main function
 for sample in trainset:
  expected=sample[0]
  zeros=list(sample[1]).count(0)
  ones=list(sample[1]).count(1)
  index=0
  #compares the number of zeros to one
  if zeros > ones:
   if expected != 0:
    for value in sample[1]:
     if value != 0:
      newWeight= weights[index]/alpha  #calculates the new weight of the attribute
      del weights[index]               #deletes the original weight of the attribute
      weights.insert(index,newWeight)  #inserts the new weight of the attribute
      index+=1
  else:
   if expected != 1:
    for value in sample[1]:
     if value != 1:
      newWeight= weights[index]/alpha  #calculates the new weight of the attribute
      del weights[index]               #deletes the original weight of the attribute
      weights.insert(index,newWeight)  #inserts the new weight of the attribute
      index+=1
  return weights

weights=winnowTrain(trainset)

#the testWinnow function tests out the weights from winnowTrain and see how they perform in predicting
def testWinnow(testset,weights):
 right=0
 wrong=0
 output=open("glass_winnow.csv","w")
 row=("expected class"+","+"predicted class"+","+"accuracy"+"\r\n")
 output.write(row)
 att=len(testset[1][1])
 for sample in testset:
  expected=sample[0]
  prediction=0
  for i in range(0,att):
   prediction+=(sample[1][i]*weights[i])
   if prediction > 1:
    predicted=1
   else:
    predicted=0
  if predicted == expected:
   accuracy='accurate'
   right+=1
  else:
   accuracy='inaccurate'
   wrong+=1
  row=(str(expected)+","+str(predicted)+","+accuracy+"\r\n")
  output.write(row)
 row=("total right ones: "+ ","+str(right)+"\r\n")
 output.write(row)
 row=("total wrong ones: "+ ","+str(wrong)+"\r\n")
 output.write(row)

testWinnow(testset,weights)
