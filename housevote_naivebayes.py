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
  zeros=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  ones=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  for sample in dict[clas]:
   for index in range(0,16):
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
 output=open("housevote_naiveBayes.csv","w")
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

naiveBayes(percentages,testset,16)
