import numpy as np
import random
#this opens a raw data file
file=open("iris.data","r")

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
 sample=0
 for ln in file:
  sample+=1
  ln=ln.strip("\n")
  ln=ln.split(",")
  clas=ln[-1]
  if clas == 'Iris-setosa':
   clas=0           
  elif clas == 'Iris-versicolor' or clas == 'Iris-virginica': 
   clas=1           
  raw=ln[0:5]
  dat=[]
  for i in raw:
   if aFloat(i) == True:
    i=float(i)
    dat.append(i)
  if len(dat)== 4:
   arr=np.asarray(dat)
   dict[sample]=[clas,np.where(arr>3,1,0)]   
 return dict

data=binarize(file)

#splitting the data into training and testing sets
#2/3 of the data goes to the training set and the rest goes ot the testing set
#the function will randomly choose the samples each time the program runs
def splitdata(data):
 trainsize=2*(int(len(data)/3))
 intrain=random.sample(list(data), trainsize)
 trainset=[]
 testset=[]
 for item in data:
  if item in intrain:
   trainset.append(data[item])
  else:
   testset.append(data[item])
  sets=(trainset,testset)
 return sets

trainset=splitdata(data)[0]
testset=splitdata(data)[1]

#The bayesTrain function calculates the percentages from the training set
def bayesTrain(trainset):
 dict={}
 dict[0]=[]
 dict[1]=[]
 countdict={}
 countdict[0]=[]
 countdict[1]=[]
 for sample in trainset:
  dict[sample[0]].append(sample[1])
 for clas in dict:
  tot=len(dict[clas])
  zeros=[0,0,0,0]
  ones=[0,0,0,0]
  for sample in dict[clas]:
   for index in range(0,4):
    if sample[index]==0:
     zeros[index]+=1
    else:
     ones[index]+=1 
  countdict[clas]=[zeros,ones,tot]
 percentdict={}
 percentdict[0]=[]
 percentdict[1]=[]
 for clas in countdict:
  for l in range(0,2):
   percentages=[]
   for i in countdict[clas][l]:
    percentage=i/countdict[clas][2]
    percentages.append(percentage)
   percentdict[clas].append(percentages)
 return percentdict

percentages=bayesTrain(trainset)

#the naiveBayes function calculates the percentage of class 0 and 1 for each sample in the testing set
#then it compares the percentages and choose the class with a higher percentage 
def naiveBayes(percentages,testset,numofatt):
 output=open("iris_naiveBayes.csv","w")
 row=("expected class"+","+"predicted class"+","+"accuracy"+"\r\n")
 output.write(row)
 right=0
 wrong=0
 for sample in testset:
  expectedclas=sample[0]
  zeros=[]
  ones=[]
  for i in range(0,numofatt):
   if sample[1][i]==0:
    zeros.append(percentages[0][0][i])
    ones.append(percentages[1][0][i])
   else:  
    zeros.append(percentages[0][1][i])
    ones.append(percentages[1][1][i])
  zero=np.prod(np.array(zeros))
  one=np.prod(np.array(ones))
  if zero < one:
   predictclas=1
  else:
   predictclas=0
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

naiveBayes(percentages,testset,4)
