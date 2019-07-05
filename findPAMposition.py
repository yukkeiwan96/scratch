file=open("70seq.csv","r")
f=0
n=0
outfile=open("forecast.txt","w")
outfile.write("ID"+"\t"+"Target"+"\t"+"PAM Index"+"\r\n")
#sadones=open("sadones.csv","w") ##PAM not found
def conSeq(seq):
 newseq=""
 for i in reversed(range(len(seq))):
  if seq[i] == "A":
   newseq+="T"
  if seq[i] == "T":
   newseq+="A"
  if seq[i] == "C":
   newseq+="G"
  if seq[i] == "G":
   newseq+="C"
 return newseq
for ln in file:
 ln=ln.strip("\r\n").split(",")
 gene, sgRNA, context=ln[0], ln[1], ln[2]
 a= context.find(sgRNA)
 if a == -1:
 # b= conSeq(context).find(sgRNA)
  b=context.find(conSeq(sgRNA))
  if b == -1:
   n+=1
  else:
   f+=1
   e=b-3
   if context[e:b-1] == "CC" and conSeq(context)[46:48]=="GG":
    row=gene+","+sgRNA+"\t"+conSeq(context)+"\t"+"45"+"\r\n"
    outfile.write(row)
 #   print(conSeq(context),context,context[e:b],conSeq(context)[45:48])
 #  if context[e:b-1] != "CC": #just a handful of them
 #   sadones.write(sgRNA+","+conSeq(sgRNA)+","+context+","+context[e:b]+"\r\n")
 else:
  f+=1
  s=a+len(sgRNA)
  e=s+3
  if context[s+1:e] == "GG":
   row=gene+","+sgRNA+"\t"+context+"\t"+str(s)+"\r\n"
   outfile.write(row)
#  if context[s+1:e] != "GG":   #just a handful of them
#   sadones.write(sgRNA+","+context+","+context[s:e]+"\r\n")
print(n,f)
