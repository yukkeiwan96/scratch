import sys, random
fn,pattern=sys.argv[1],sys.argv[2]
gencode = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W'}

aaDict={}
for codon in gencode:
 aa=gencode[codon]
 if aa not in aaDict:
  aaDict[aa]=[codon]
 else:
  aaDict[aa].append(codon)

file=open(fn,"r")
for CDS in file:
 CDS=CDS.strip().upper()
 print(CDS)
 codonList,i=[],0
 for j in range(1,len(CDS)):
  if j % 3 == 0:
   codonList.append(CDS[i:j])
   i=j
 codonList.append(CDS[i:])
 aminoacid,aaList="",[]
 for codon in codonList:
  aminoacid+=gencode[codon]
 for aa in aminoacid:
  aaList.append(aaDict[aa])
 mutList=[]
 for i in range(50000):
  newaaseq=""
  for codons in aaList:
   newaaseq+=random.choice(codons)
  if newaaseq not in mutList:
   pattern_occurance=newaaseq.count(pattern)
   mutList.append((newaaseq,pattern_occurance))
 mutList.sort(key=lambda tup: tup[1], reverse=True)
 outfile=open(aminoacid+"_"+pattern+".csv","w")
 for tup in mutList:
  outfile.write(tup[0]+","+str(tup[1])+"\r\n")
 outfile.close()
