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
# print output
print "%s [ %6.2f ]" % (ss, mfe)
