import sys 
import math
import operator
from processFile import openFile, splitData, Sets, calcGain

#############################################################################
#the following function builds a decision tree based of the calcGain function
#reference:https://machinelearningmastery.com/implement-decision-tree-algorithm-scratch-python/
#############################################################################
# Split a dataset based on an attribute and an attribute value
def test_split(index, value, dataset):
 left=[]
 right=[]
 for row in dataset:
  if row[index] == value:
   left.append(row)
  else:
   right.append(row)
 return left, right

def get_split(trainSet):
 class_values = list(set(row[-1] for row in trainSet))
 b_index, b_value, b_score, b_groups = 0, 0, 0, None
 for index in range(len(trainSet[0])-1):
  for row in trainSet:
   groups = test_split(index, row[index], trainSet)
   runGain=calcGain(trainSet)
   gain = runGain[1]
   index=runGain[0]
   if gain > b_score:
    b_index, b_value, b_score, b_groups = index, row[index], gain, groups
 return {'index':b_index, 'value':b_value, 'groups':b_groups}

def split(node, max_depth, min_size, depth):
 left, right = node['groups']
 del(node['groups'])
 # check for a no split
 if not left or not right:
  node['left'] = node['right'] = to_terminal(left + right)
  return
 # check for max depth
 if depth >= max_depth:
  node['left'], node['right'] = to_terminal(left), to_terminal(right)
  return
 # process left child
 if len(left) <= min_size:
  node['left'] = to_terminal(left)
 else:
  node['left'] = get_split(left)
  split(node['left'], max_depth, min_size, depth+1)
 # process right child
 if len(right) <= min_size:
  node['right'] = to_terminal(right)
 else:
  node['right'] = get_split(right)
  split(node['right'], max_depth, min_size, depth+1)

def build_tree(train, max_depth, min_size):
 root = get_split(train)
 split(root, max_depth, min_size, 1)
 return root

def to_terminal(group):
 outcomes = [row[-1] for row in group]
 return max(set(outcomes), key=outcomes.count)

# Make a prediction with a decision tree
def predict(node, row):
 if row[node['index']] == node['value']:
  if isinstance(node['left'], dict):
    return predict(node['left'], row)
  else:
    return node['left']
 else:
  if isinstance(node['right'], dict):
    return predict(node['right'], row)
  else:
    return node['right']

def print_tree(node, depth=10):
	if isinstance(node, dict):
		print('%s[%s = %s]' % ((depth*' ', (node['index']), node['value'])))
		print_tree(node['left'], depth+1)
		print_tree(node['right'], depth+1)
	else:
		print('%s[%s]' % ((depth*' ', node)))

###########################RUN##########################
rawdata=sys.argv[1]  #input the name of the file
raw=rawdata.split(".")
ra=raw[0]
file=openFile(rawdata)
dat=file[0]
type=file[1]
par=splitData(dat)
valSet=par[0]   #outputs a list of data points
rounds= Sets(par)
testSet=rounds[1][1]
trainSet=rounds[1][0]  #trainSet is a list of data points
tree=build_tree(trainSet,50,3)
print_tree(tree)
rootnode= file[2]
for row in testSet:
 prediction = predict(rootnode, row)
 print('Expected=%s, Got=%s' % (row[-1], prediction))