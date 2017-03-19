import sys, os, glob, time
import numpy as np
#import matplotlib.pyplot as plt
import library.timedomain as td
import library.fileprocessing as fp



if __name__ == '__main__':
	if len(sys.argv) == 2:
		directory = sys.argv[1]
		#filename = sys.argv[1]
		#filename2 = sys.argv[2]
	#time_stamps,sdata = fp.loadfile_multisweep(filename)
	F = fp.loadfile_frequency(directory+'/frequency.txt')
	#F = f[::10]
	#td.transform(F,sdata[0],verbose=1,overs=50,)
	starttime = time.time()

	files = glob.glob(directory+'/*.txt')
	files.sort(key=os.path.getctime)
	files.remove(directory+'/frequency.txt')

	#array storing delta length changes and time_stamps for files in directory
	delta_length = np.empty(0)
	delta_length2 = np.empty(0)
	timestamps = np.empty(0)

	#Enumerate through each files and solve for the reference delay and store into delta_length
	#Only taking the first sweep in the file

	for n,fname in enumerate(files[::10]):
    		timest,S = fp.loadfile_multisweep(fname)
    		Xpeak,Xpeak2 = td.transform(F,S[0],verbose=1,overs=100);
    		if n==0:
        		Xfirstpeak=Xpeak
			Xfirstpeak2=Xpeak2
    		delta_length = np.append(delta_length,(Xpeak-Xfirstpeak)*1000)
		delta_length2 = np.append(delta_length2,(Xpeak2-Xfirstpeak2)*1000)
    		timestamps = np.append(timestamps,timest[0])
    		print 'peak at %8.3f m and %8.3f m, Delta1 =  %+6.10f mm, Delta2 = %+6.10f mm SWEEP FILE %4.0f/%4.0f' % (Xpeak,Xpeak2,(Xpeak-Xfirstpeak)*1000,(Xpeak2-Xfirstpeak2)*1000,n,len(files))

	print 'Total time = %f minutes' % ((time.time()-starttime)/60)
	
	plot(timestamps,0.5*(delta_length1/1000/c)*1e12,'b',timestamps,0.5*(delta_length2/c)*1e12,'r')
	xlabel('TIME [s]'); ylabel('DELTA DELAY [ps]'). legend(('RFN+AFN','AFN Only'),loc=3)
	grid(True)
