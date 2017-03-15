import numpy as np

def loadfile_multisweep(filename):
	try:
		content = []
		with open(filename) as f:
			content = f.readlines()
		time_stamps = []
		sdata = []
		for i in content:
			time_stamps.append(float(i.split(' ')[0]))
			temp = np.array(map(float,i.split(' ')[1].split(',')))
			sdata.append(temp[::2]+1j*temp[1::2])
		return time_stamps,sdata

	except:
		print 'Error - could not load file %s', filename

def loadfile_frequency(filename):    
	try:
        	return np.genfromtxt(filename,delimiter=',')
    	except:
        	print 'Error - could not load file %s' % filename



