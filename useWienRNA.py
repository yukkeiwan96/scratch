import sys
sys.path.append('/usr/local/lib/python2.7/site-packages/')
sys.path
import RNA
# The RNA sequence
seq = "GAGUAGUGGAACCAGGCUAUGUUUGUGACUCGCAGACUAACA"
###MFE Prediction (flat interface)
# compute minimum free energy (MFE) and corresponding structure
(ss, mfe) = RNA.fold(seq)
# print output
print "%s\n%s [ %6.2f ]" % (seq, ss, mfe)
###MFE Prediction (obj-oriented interface)
sequence = "CGCAGGGAUACCCGCG"
# create new fold_compound object
fc = RNA.fold_compound(sequence)
# compute minimum free energy (mfe) and corresponding structure
(ss, mfe) = fc.mfe()

def compare(mint,nint):
 if nint > mint:
  mint=nint
 return mint

def SStruct(ln):
 S1=ln.split("(.")
 S=[]
 for sub in S1:
  if "(" in sub and ")" in sub:
   subl=sub.split(").")
   if len(subl) > 1:
    for s in subl:
     if ")" in s:
      s+=")."
     else:
      s+="(."
     S.append(s)
   else:
    subl=sub.split(")(")
    for s in subl:
     if ")" in s:
      s+=")"
     else:
      s="("+s+"(."
     S.append(s)
  else:
   if ")" not in sub:
    sub+="(."
    S.append(sub)
   else:
    subl=sub.split(").")
    for s in subl[:-1]:
     s+=")."
     S.append(s)
    S.append(subl[-1])
 print(ln)
 a=""
 for i in S:
  a+=i
 print(a)
 print(S)
 MCstem=0
 for j in range(len(S)):
  cstem=S[j].count("(")+S[j].count(")")
  MCstem=compare(MCstem,cstem)
 loops,Mloop,Mstem,snt0,snt1=[],0,0,0,0
 for j in range(len(S)):
  if j == 0:
   loop=[S[j]]
  else:
   if "(" in S[j] and "(" in loop[-1]:
    loop.append(S[j])
   elif "(" in loop[-1] and ")" in S[j]:
    loop.append(S[j])
   elif ")" in S[j] and ")" in loop[-1]:
    loop.append(S[j])
   elif ")" in loop[-1] and "(" in S[j]:
    loops.append(loop)
    loop=[S[j]]
 loops.append(loop)
 stems1,stems2="",""
 for loop in loops:
  stem1,stem2="",""
  for a in range (len(loop)):
   if a+1 < len(loop):
    if loop[a].endswith("(.") and loop[a+1].startswith("."):
     cloop=len(loop[a])-loop[a].find("(.")-1+loop[a+1].find(")")
     Mloop=compare(Mloop,cloop)
   if "(" in loop[a]:
    stem1+=loop[a]
   elif ")" in loop[a]:
    stem2+=loop[a]
  stems=[stem1,stem2]
  stems1+=stem1
  stems2+=stem2
  for stem in stems:
   snt=stem.count("(")+stem.count(")")
   Mstem=compare(Mstem,snt)
 allbp=compare(stems1.count("("),stems2.count(")"))
 print(Mloop,MCstem,Mstem,allbp)
SStruct(ss)
