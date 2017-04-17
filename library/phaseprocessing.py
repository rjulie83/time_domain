##Calculating Phase Offset after subtracting gradient
##CALCULATING DELTA DELAY (MAX-MIN) IN PERIOD
import time
from progress.bar import Bar
import numpy as np

#Calculate peak-peak offset after removing straightline in every period
def normal_offset_calc(timestamps,delay_data,minute_window = 20):
	
	delta_delay = delay_data - delay_data[0]
	time_start = time.time()

	samplerate = timestamps[1]-timestamps[0]   								#rough samplerate
	samples_in_period = int(minute_window*60/samplerate)    				#number of samples in minutes_interval

	phase_offset = np.empty(0)
	phase_offset_timestamps = np.empty(0)
	temp_x = np.array(range(samples_in_period))

	bar = Bar('Processing', max=(len(delay_data)-samples_in_period))					#Initialise progress bar

	#phase delta in every minute interval window calculation
	for i in range(len(delay_data)-samples_in_period):
		bar.next()
		delay_subset = delay_data[i:i+samples_in_period]  						#Restrict analysis to minute interval under consideration
		temp_coeffs = np.polyfit(temp_x,delay_subset,1) 					#Fit straightline to data in minute interval
		residual = delay_subset - (temp_x*temp_coeffs[0]+temp_coeffs[1]) 	#Subtract straightline from data in minute interval
		temp_max = np.max(residual)
		temp_min = np.min(residual)
		phase_offset = np.append(phase_offset,temp_max-temp_min) 			#determine peak to peak of delay after removing straightline
		phase_offset_timestamps = np.append(phase_offset_timestamps,timestamps[i])
	bar.finish()

	print 'Duration: %i minutes' % ((time.time()-time_start)/60)
	
	return phase_offset,phase_offset_timestamps
	
#Calculate peak-peak offset after removing straightline in every period
def offset_calc(timestamps,delay_data,minute_window = 20):
	
	delta_delay = delay_data - delay_data[0]
	time_start = time.time()
	
	samplerate = timestamps[1]-timestamps[0]   								#rough samplerate
	samples_in_period = int(minute_window*60/samplerate)    				#number of samples in minutes_interval

	phase_offset = np.empty(0)
	phase_offset_timestamps = np.empty(0)
	temp_x = np.array(range(samples_in_period))
	
	bar = Bar('Processing', max=(len(delay_data)-samples_in_period))					#Initialise progress bar
	
	#phase delta in every minute interval window calculation
	for i in range(len(delay_data)-samples_in_period):
		bar.next()
		delay_subset = delay_data[i:i+samples_in_period]  						#Restrict analysis to minute interval under consideration
		temp_max = np.max(delay_subset)
		temp_min = np.min(delay_subset)
		phase_offset = np.append(phase_offset,temp_max-temp_min) 			#determine peak to peak of delay after removing straightline
		phase_offset_timestamps = np.append(phase_offset_timestamps,timestamps[i])
	bar.finish()
	
	print 'Duration: %i minutes' % ((time.time()-time_start)/60)
	
	return phase_offset,phase_offset_timestamps
	