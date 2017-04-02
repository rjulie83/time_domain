import sys, os, glob, time
import numpy as np
import matplotlib.pyplot as plt
import library.timedomain as td
import library.fileprocessing as fp



if __name__ == '__main__':
	if len(sys.argv) == 5:
		directory = sys.argv[1]
		oversampling = int(sys.argv[2])
		calibration = int(sys.argv[3])
		file_skipping_factor = int(sys.argv[4])
	else:
		print "usage: python TimeDomainAnalysis_multi.py <directory> <oversampling> <calibration 1 or 0> <file_skipping_factor>"
		sys.exit()
		
	F = fp.loadfile_frequency(directory+'/frequency.txt')
	c = 299792458
	
	starttime = time.time()

	files = glob.glob(directory+'/*.txt')
	files.sort(key=os.path.getmtime)
	files.remove(directory+'/frequency.txt')

	#array storing delta length changes and time_stamps for files in directory
	delta_length = np.empty(0)
	delta_length2 = np.empty(0)
	timestamps = np.empty(0)
	pulse_peak1 = np.empty(0)
	pulse_peak2 = np.empty(0)

	#Determine peakindex with one run of transform code
	temptime,S = fp.loadfile_multisweep(files[0])
	temp1,temp2,temp3,temp4,peak1,peak2 = td.transform(F,S[0],verbose = 0,overs=oversampling)

	#Enumerate through each files and solve for the reference delay and store into delta_length
	#Only taking the first sweep in the file
	for n,fname in enumerate(files[::file_skipping_factor]):
    		timest,S = fp.loadfile_multisweep(fname)
    		Xpeak,Xpeak2,pulse_height1,pulse_height2,temp1,temp2 = td.transform(F,S[0],verbose=0,overs=oversampling,peak1_index=peak1,peak2_index=peak2)
    		if n==0:
        		Xfirstpeak=Xpeak
			Xfirstpeak2=Xpeak2
    		delta_length = np.append(delta_length,(Xpeak-Xfirstpeak)*1000)
		delta_length2 = np.append(delta_length2,(Xpeak2-Xfirstpeak2)*1000)
    		timestamps = np.append(timestamps,timest[0])
		if calibration == 0:
    			print 'peak at %8.3f m and %8.3f m, Delta1 =  %+6.10f ps, Delta2 = %+6.10f ps SWEEP FILE %4.0f/%4.0f' % (Xpeak,Xpeak2,(Xpeak-Xfirstpeak)/c*1e12,(Xpeak2-Xfirstpeak2)/c*1e12,n,len(files))
		else:
			print 'Peak at %3.10f m and Delta1 = %2.10f mm and %2.10f ps' % (Xpeak,(Xpeak-Xfirstpeak)*1000,(Xpeak-Xfirstpeak)/c*1e12)
		pulse_peak1 = np.append(pulse_peak1,pulse_height1)
		pulse_peak2 = np.append(pulse_peak2,pulse_height2)
	print 'Sampling rate = %3.1f seconds\n' % (timestamps[2] - timestamps[1])
	
	

	#For calibration run
	if calibration == 1:
		plt.subplot(2,1,1)
		plt.plot((timestamps-timestamps[0]),(delta_length/1000/c)*1e12)
		plt.xlabel('TIME [s]'); plt.ylabel('DELAY [ps]'); plt.title('SETUP STABILITY RUN (%4.0f minutes)' % ((timestamps[-1]-timestamps[0])/60))
		plt.grid(True)
		plt.subplot(2,1,2)
		plt.plot((timestamps-timestamps[0]),pulse_peak2)
		plt.xlabel('TIME [s]'); plt.ylabel('PEAK S21 [dB]'); plt.title('SETUP STABILITY RUN (%4.0f minutes)' % ((timestamps[-1]-timestamps[0])/60))
		plt.grid(True)
		plt.show(True)	

		data_file = open('data_summary.csv','w')
		data_file.write('File No.,Time stamp [s], Time Offset [s], Xpeak1 [m], Delta Xpeak1 [mm],Delta Xpeak1 [ps]\n')
		for i in range(len(timestamps)):
			data_file.write('%2.0f,%10.3f,%5.0f,%3.10f,%2.10f,%2.10f\n' % (i,timestamps[i],timestamps[i]-timestamps[0],Xpeak,(Xpeak-Xfirstpeak)*1000,(Xpeak-Xfirstpeak)/c*1e12))
		data_file.close()
	
	else:
		plt.plot(timestamps,0.5*(delta_length/1000/c)*1e12,'b',timestamps,0.5*(delta_length2/c)*1e12,'r')
        	plt.xlabel('TIME [s]'); plt.ylabel('DELTA DELAY [ps]'); plt.legend(('RFN+AFN','AFN Only'),loc=3)
        	plt.grid(True)
        	plt.show(True)

		data_file = open('data_summary.csv','w')
                data_file.write('File No.,Time stamp [s], Time Offset [s], Xpeak1 [m], Delta Xpeak1 [mm],Delta Xpeak1 [ps], Xpeak2 [m], Delta Xpeak2 [mm], Delta Xpeak2 [ps]\n')
                for i in range(len(timestamps)):
                        data_file.write('%2.0f,%10.3f,%5.0f,%3.10f,%2.10f,%2.10f,%3.10f,%2.10f,%2.10f\n' % (i,timestamps[i],timestamps[i]-timestamps[0],Xpeak,(Xpeak-Xfirstpeak)*1000,(Xpeak-Xfirstpeak)/c*1e12,Xpeak2,(Xpeak2-Xfirstpeak2)*1000,(Xpeak2-Xfirstpeak2)/c*1e12))
                data_file.close()

	print 'Total time = %f minutes' % ((time.time()-starttime)/60)
