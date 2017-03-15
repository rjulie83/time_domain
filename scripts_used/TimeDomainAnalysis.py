import sys, os, glob, time
#import numpy as np
#import matplotlib.pyplot as plt
import timedomain as td
import fileprocessing as fp



if __name__ == '__main__':
	if len(sys.argv) == 3:
		#directory = sys.argv[1]
		filename = sys.argv[1]
		filename2 = sys.argv[2]
	time_stamps,sdata = fp.loadfile_multisweep(filename)
	F = fp.loadfile_frequency(filename2)
	#F = f[::10]
	td.transform(F,sdata[0],verbose=1,overs=50,)
	starttime = time.time()

	#files = glob.glob(directory+'/*.txt')
	#files.sort(key=os.path.getctime)
	#files.remove(filename2)

	#array storing delta length changes and time_stamps for files in directory
	#delta_length = np.empty(0)
	#timestamps = np.empty(0)

	#Enumerate through each files and solve for the reference delay and store into delta_length
	#Only taking the first sweep in the file

#	for n,fname in enumerate(files[::2]):
#    		timest,S = loadfile_multisweep(fname)
#    		Xpeak = transform(F,S[0],verbose=3,overs=1678);
#    		if n==0:
#        		Xfirstpeak=Xpeak
#    		delta_length = np.append(delta_length,(Xpeak-Xfirstpeak)*1000)
#    		timestamps = np.append(timestamps,timest[0])
#    		print 'peak at %8.10f m, delta of %+6.10f mm for sweep file %4.0f/%4.0f' % (Xpeak,(Xpeak-Xfirstpeak)*1000,n,len(files))

#	print 'Total time = %f minutes' % ((time.time()-starttime)/60)
