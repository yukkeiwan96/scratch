import numpy as np
import random
#this opens a raw data file
file=open("house-votes-84.data","r")

#the preprocess function finds the preferences of both parties
def preprocess(file):
 pref={}
 rawlist=[]
 pref['rep']=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
 pref['dem']=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
 for ln in file:
  ln=ln.strip("\n")
  ln=ln.split(",")
  clas=ln[0]
  if clas == 'republican': 
   clas=0           #set republican as class 0
  elif clas == 'democrat': 
   clas=1           #set democrats as class 1
  raw=ln[1:]
  for index in range(0,16):
   if clas == 0:
    if raw[index] == 'y':
     pref['rep'][0][index]+=1
    elif raw[index] == 'n':
     pref['rep'][1][index]+=1
   else:
    if raw[index] =='y':
     pref['dem'][0][index]+=1
    elif raw[index] =='n':
     pref['dem'][1][index]+=1
  combine=[clas,raw]
  rawlist.append(combine)
  prefs={}
  prefs['rep']=[]
  prefs['dem']=[]
  for clas in pref:
   for index in range(0,16):
    if pref[clas][1]>=pref[clas][0]:
     prefs[clas].append(1)
    else:
     prefs[clas].append(0)  
  lists=(prefs['rep'],prefs['dem'],rawlist) 
 return lists

lists= preprocess(file)

#the binarize function binarizes the data
def binarize(lists):
 dict={}
 sample=0
 for ln in lists[2]:
  dat=[] 
  sample+=1
  index=0
  for att in ln[1]:
   if att == 'y':
    att= 0
   elif att == 'n':
    att= 1
   elif att == '?':
    att=lists[ln[0]][index]
   dat.append(att)
   index+=1
  dict[sample]=[ln[0],dat]
 return dict
data=binarize(lists)

#splitting the data into training and testing sets
def splitdata(data):
 trainsize=2*(int(len(data)/3))   #2/3 of the data will be the training set
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
 alpha=50
 weights=[]
 for n in range(0,len(trainset[1][1])):  #this generates the starting weight for each attribute
  weights.append(1)               #the starting weight is 1, which demoting will be the main function
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
  print(weights)
  return weights

weights=winnowTrain(trainset)

#the testWinnow function tests out the weights from winnowTrain and see how they perform in predicting
def testWinnow(testset,weights):
 right=0
 wrong=0
 output=open("housevotes_winnow.csv","w")
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
