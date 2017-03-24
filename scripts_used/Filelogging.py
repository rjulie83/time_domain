import sys,socket,time
import library.vna_filelogging as flog


if __name__ == "__main__":
	IPaddress = "10.97.64.118"
	vna = flog.connect(IPaddress, port=5025, sleeptime = 1)
	flog.initialise(vna)

	frequency_string = flog.get_trace_string_from_vna(0,vna)
	text_file = open('data/frequency.txt', "w")
	text_file.write(frequency_string)
	text_file.close()
	

	number_of_datasets_per_file = 100
	files = 1
	iteration = 0
	start_time = time.time()
	for i in range(files):
    		temp_string_list = []
    		for i in range(number_of_datasets_per_file):
			sys.stdout.write('.')
        		temp_string_list.append(str(time.time())+' '+flog.get_trace_string_from_vna(1,vna))        
    		flog.write_string_to_file(temp_string_list)
    		print "File $i/%i %2.0f%%  Points check:%i Hours since start: %i" % (iteration,files-1,100.0*iteration/(files-1),len(temp_string_list[0].split(',')),int(time.time() - start_time)/3600)
    		iteration += 1
	print (time.time() - start_time)
	vna.close()
