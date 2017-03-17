import sys



if __name__ == "__main__":
	IPaddress = "10.97.64.118"
	vna = connect(IPaddress, port=5025, sleeptime = 1)
	initialise(vna)

	frequency_string = get_trace_string_from_vna(0,vna)
	text_file = open('data/frequency.txt', "w")
	text_file.write(frequency_string)
	text_file.close()
	

	number_of_datasets_per_file = 10
	minutes = 60*6*6#3756;    #approximately 24 hours
	iteration = 0;
	start_time = time.time()
	for i in range(minutes):
    		temp_string_list = []
    		for i in range(number_of_datasets_per_file):
        		temp_string_list.append(str(time.time())+' '+get_trace_string_from_vna(1,vna))        
    			write_string_to_file(temp_string_list)
    		print iteration,len(temp_string_list[0].split(',')),(time.time() - start_time)
    		iteration += 1
	print (time.time() - start_time)
