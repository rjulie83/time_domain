import socket, date, time, datetime, array, numpy

def connect(IPaddress, port=5025, sleeptime = 1):
	vna = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	vna.setblocking(0) 
	vna.settimeout(sleeptime)
	vna.connect((IPaddress,port))
	return vna
	

def initialise(vna):
	vna.send('INIT:CONT OFF\n')
	vna.send('*IDN?\n')  
	time.sleep(1)  
	reply=vna.recv(100) 
	reply=reply[:-2]  
	print('Ident     : %s' % reply)
    
def get_trace_from_vna(option,vna, sleeptime=1):
    	# get's trace data from VNA. Either stimulus or data depending on flag. Return number data
    	#flag = 0 for frequency data, flag = 1 for trace data
    	vna.send('INIT1:IMM;*WAI\n')
    	if option:
        	vna.send('CALC:DATA? SDAT\n')
       		time.sleep(sleeptime)
        	string_list = ''
        	temp_char = vna.recv(1)
        	while temp_char != '\n':
            		string_list = string_list + temp_char
            		temp_char = vna.recv(1)
        	string_data = string.split(string_list,',')
        	data = [float(i) for i in string_data]
		X, Y = data[::2], data[1::2]
        	return X,Y
    	elif option==0:
        	vna.send('CALC:DATA:STIM?\n')
        	time.sleep(sleeptime)
        	string_list = ''
        	temp_char = vna.recv(1)
        	while temp_char != '\n':
            		string_list = string_list + temp_char
            		temp_char = vna.recv(1)
        	string_data = string.split(string_list,',')
        	frequency = [float(i) for i in string_data]
        	return frequency

def get_trace_string_from_vna(option,vna,sleeptime=1):
	# get's trace data from VNA. Either stimulus or data depending on flag. Return string array
    	#flag = 0 for frequency data, flag = 1 for trace data
    	vna.send('INIT1:IMM;*WAI\n')
    	if option:
    		vna.send('CALC:DATA? SDAT\n')
        	time.sleep(sleeptime)
        	string_list = ''
        	temp_char = vna.recv(1)
        	while temp_char != '\n':
            		string_list = string_list + temp_char
            		temp_char = vna.recv(1)
        	return string_list
    	elif option==0:
        	vna.send('CALC:DATA:STIM?\n')
        	time.sleep(sleeptime)
        	string_list = ''
        	temp_char = vna.recv(1)
        	while temp_char != '\n':
            		string_list = string_list + temp_char
            		temp_char = vna.recv(1)
        	return string_list

def write_string_to_file(data_string_list):
    	filename = 'data/'+ datetime.datetime.now().time().isoformat().replace(':','-') + '.txt'
    	text_file = open(filename, "w")
    	for i in data_string_list:
        	text_file.write('%s\n' % i)
    	text_file.close()
 
    
