import sys
OT=float(sys.argv[1])
FS=float(sys.argv[2])

file=open(sys.argv[3],"r")
header=file.readline()
dict,totgenes={},[]
for ln in file:
 l=ln.split(",")
 if l[3] not in totgenes:
  totgenes.append(l[3])
 if float(l[6]) >= OT and float(l[7]) > FS and float(l[8]):
  if l[4] != "NOT_MAPPED":
   if l[3] not in dict:
    dict[l[3]]=[(int(l[4]),l[2],ln)]
   else:
    dict[l[3]].append((int(l[4]),l[2],ln))
c=0
outfile=open("out.csv","w")
outfile.write(header)
for g in totgenes:
 if g not in dict:
 # print(g)
  c+=1
 elif g in dict and len(dict[g]) < 3:
 # print(g,dict[g]) 
  c+=1
 else:
  pos,ind=[dict[g][0][0]],[0]
  for i in range (1,len(dict[g])):
   t=0
   for j in pos:
    if abs(dict[g][i][0]-j) > 1000:
     t+=1
   if t == len(pos):
    pos.append(dict[g][i][0])
    ind.append(i)
  if len(ind) < 3:
   c+=1
  else:
   for i in ind[:3]:
    outfile.write(dict[g][i][2])
outfile.close()
