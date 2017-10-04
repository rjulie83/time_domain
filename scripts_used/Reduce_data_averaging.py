from progress.bar import Bar
import library.timedomain as td
import library.fileprocessing as fp
import numpy as np
import glob, sys, os, time

if __name__ == '__main__':
	if len(sys.argv) == 2:
		oversampling_factor = int(sys.argv[1])
	else:
		print "usage: python Reduce_data.py <oversampling>"
		sys.exit()
		
	timestart = time.time()
	F = fp.loadfile_frequency('frequency.txt')
	files = glob.glob('*.txt')
	files.sort(key=os.path.getmtime)
	files.remove('frequency.txt')
	bar = Bar('Processing',max=len(files))
	iteration = 0
	with open('data.csv','a') as data_file:
		data_file.write('Timestamp,Delay1[m],Delay1_amplitude[dB],Delay2[m],Delay2_amplitude[dB]\n')
	
	for filename in files:
		#print 'File %i out of %i being processed...' % (iteration+1,len(files))
		timestamps_temp,temp_sdata = fp.loadfile_multisweep(filename)
		#heights1 = [];heights2 = []
		loop_timestart = time.time()
		delay1,delay2,height1,height2 = td.transform(F,np.mean(temp_sdata,axis=0),verbose=0,overs=oversampling_factor)
		bar.next()
		with open('data_averaged.csv','a') as data_file:
			data_file.write('%f,%3.10f,%2.2f,%3.10f,%2.2f\n' % (timestamps_temp[0],delay1,height1,delay2,height2))
		#sys.stdout.write('\nFile process time= %0.0fs, S21_dB_average= %2.0fdB and %2.0fdB\n' % (time.time()-loop_timestart,np.mean(heights1),np.mean(heights2)))
		iteration = iteration + 1
		
	#data_file = open('data.csv','w')
	#data_file.write('Timestamp,Delay1[m],Delay1_amplitude[dB],Delay2[m],Delay2_amplitude[dB]\n')
	#for i in range(len(timestamps)):
	#	data_file.write('%f,%3.10f,%2.2f,%3.10f,%2.2f\n' % (timestamps[i],delay1_data[i],height1_data[i],delay2_data[i],height2_data[i]))
	#data_file.close()
	bar.finish()
	print ((time.time()-timestart)/3600)+' hours'
