import sys
import library.timedomain as td
import library.fileprocessing as fp
import matplotlib

if __name__ == '__main__':
	if len(sys.argv)==3:
		filename1 = sys.argv[1]
		filename2 = sys.argv[2]
	else:
		print "USAGE: python Filequality <Phasedata_file> <frequency file>"
		sys.exit()
	F = fp.loadfile_frequency(filename2)
	timestamp,X = fp.loadfile_multisweep(filename1)
	td.plotresponse(F,X[0])
	A,B,C,D = td.transform(F,X[0],verbose=3)
	print "Peak 1 level %0.2fdB, Peak 2 level %0.2f" % (C,D)
	matplotlib.pyplot.show()
