import numpy as np
import random
#this opens a raw data file
file=open("soybean-small.data","r")

#the anInteger function distinguishes whether a value is an integer or not
def anInteger(i):
 try:
  int(i)
  return True
 except ValueError:
  return False

#the binarize function binarizes the raw data
def binarize(file):
 dict={}
 sample=0
 for ln in file:
  sample+=1
  ln=ln.strip("\n")
  ln=ln.split(",")
  clas=ln[-1]
  if clas == 'D2' or clas=='D1':   #D1 and D2 are the classes for normal ones
   clas=0           #set the normal ones to class 0
  elif clas == 'D4'or clas=='D3': #D3 and D4 are the classes for irrelavant ones
   clas=1           #set the irrelavant ones to class 1
  raw=ln[0:-1]
  dat=[]
  for i in raw:
   if anInteger(i) == True:
    i=int(i)
    dat.append(i)
  if len(dat)==35:
   arr=np.asarray(dat)
   dict[sample]=[clas,np.where(arr>0,1,0)]   
 return dict

data= binarize(file)

#splitting the data into training and testing sets
def splitdata(data):
 trainsize=2*(int(len(data)/3))    #2/3 of the data will be the training set
 intrain=random.sample(list(data), trainsize)   #randomly select the 2/3s of the data
 trainset=[]
 testset=[]
 for item in data:            #this sorts the sample into either the training or testing sets
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
  weights.append(1)                     #the starting weight is 1, which demoting will be the main function
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
 output=open("soybean_winnow.csv","w")
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
