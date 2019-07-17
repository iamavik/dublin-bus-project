import joblib
#import pickle
import _pickle as cPickle
import os
CURRENT_DIR = os.path.dirname(__file__)
#model_file = os.path.join(CURRENT_DIR, 'prediction_46A_cPickle.pickle')

def ml_model(bus_line,departure_bus_seq,arrival_bus_seq,arrival_stop_id,departure_stop_id,bus_at_departure_stop,bus_at_arrival_stop,departure_date):
	#Departure date needs to be passed as well from views.py
	try:
		import gc
		from datetime import date
		from datetime import datetime
		import calendar
		if(departure_date==''):
			departure_date = date.today()
			print(departure_date)
			day_of_week = calendar.day_name[departure_date.weekday()]
		else:
			departure_date = departure_date.split('-')
			print(departure_date)
			year = int(departure_date[0])
			month = int(departure_date[1])
			date = int(departure_date[2])

			departure_date = datetime(2019,7,17)
			day_of_week = calendar.day_name[departure_date.weekday()]  #'Wednesday'

		print("Day of the week is",day_of_week)
		#import time,datetime
		print("Bus Line is",bus_line)
		extract_dept_stop_id = int(departure_stop_id[-4:])
		print("Extracted departure stop id is",extract_dept_stop_id)
		extract_arr_stop_id = int(arrival_stop_id[-4:])
		print("Extracted arrival stop id is",extract_arr_stop_id)
		print("Bus at depart stop",bus_at_departure_stop)
		print("Bus at arrival stop", bus_at_arrival_stop)
		a = bus_at_departure_stop[-2:]
		if(a=='am'):
			bus_at_departure_stop = bus_at_departure_stop[:-2]
			bus_at_departure_stop = bus_at_departure_stop.split(':')
			hr_in_sec_1 = int(bus_at_departure_stop[0])*3600
			mins_sec_1 = int(bus_at_departure_stop[1])*60
			time_secs_1 = hr_in_sec_1+mins_sec_1
		else:
			bus_at_departure_stop = bus_at_departure_stop[:-2]
			bus_at_departure_stop = bus_at_departure_stop.split(':')
			hr_in_sec_1 = (int(bus_at_departure_stop[0])+12)*3600
			mins_sec_1 = int(bus_at_departure_stop[1])*60
			time_secs_1 = hr_in_sec_1+mins_sec_1

		print("Time in seconds1",time_secs_1)
		a = bus_at_arrival_stop[-2:]
		if(a=='am'):
			bus_at_arrival_stop = bus_at_arrival_stop[:-2]
			bus_at_arrival_stop = bus_at_arrival_stop.split(':')
			hr_in_sec_2 = int(bus_at_arrival_stop[0])*3600
			mins_sec_2 = int(bus_at_arrival_stop[1])*60
			time_secs_2 = hr_in_sec_2+mins_sec_2
		else:
			bus_at_arrival_stop = bus_at_arrival_stop[:-2]
			bus_at_arrival_stop = bus_at_arrival_stop.split(':')
			hr_in_sec_2 = (int(bus_at_arrival_stop[0])+12)*3600
			mins_sec_2 = int(bus_at_arrival_stop[1])*60
			time_secs_2 = hr_in_sec_2+mins_sec_2

		print("Time in seconds2",time_secs_2)

		list_bus_lines_mon_fri = ['68A','747','66B','757','27X','33X','84A','7D','66X','66E','38B','67X','116','44B','38D','31B','25D', '32X', '51D', '16D', '46E', '84X', '7B', '69X', '15D', '41X', '142', '68X', '25X', '39X', '41D', '33D', '51X', '77X', '118', '33E']

		if(bus_line in list_bus_lines_mon_fri):
			file_name = bus_line+'.pickle'
			model_file = os.path.join(CURRENT_DIR, file_name)
			if(day_of_week=="Friday"):
				request_to_model = [[int(departure_bus_seq),int(extract_arr_stop_id),time_secs_1,1,0,0,0,0]]
				gc.disable()
				model = cPickle.load(open(model_file,'rb'))
				gc.enable()
				predicted_arrival_time_1 = int(model.predict(request_to_model))
				print("Predicted arrival time to the departure bus stop is",predicted_arrival_time_1)
				request_to_model = [[int(arrival_bus_seq),int(extract_dept_stop_id),time_secs_2,1,0,0,0,0]]
				predicted_arrival_time_2 = int(model.predict(request_to_model))
				print("Predicted arrival time to the arrival bus stop is",predicted_arrival_time_2)


			if(day_of_week=="Monday"):

				request_to_model = [[int(departure_bus_seq),int(extract_arr_stop_id),time_secs_1,0,1,0,0,0]]
				gc.disable()
				model = cPickle.load(open(model_file,'rb'))
				gc.enable()
				predicted_arrival_time_1 = int(model.predict(request_to_model))
				print("Predicted arrival time to the departure bus stop is",predicted_arrival_time_1)
				request_to_model = [[int(arrival_bus_seq),int(extract_dept_stop_id),time_secs_2,0,1,0,0,0]]
				predicted_arrival_time_2 = int(model.predict(request_to_model))
				print("Predicted arrival time to the arrival bus stop is",predicted_arrival_time_2)


			if(day_of_week=="Thursday"):

				request_to_model = [[int(departure_bus_seq),int(extract_arr_stop_id),time_secs_1,0,0,1,0,0]]
				gc.disable()
				model = cPickle.load(open(model_file,'rb'))
				gc.enable()
				predicted_arrival_time_1 = int(model.predict(request_to_model))
				print("Predicted arrival time to the departure bus stop is",predicted_arrival_time_1)
				request_to_model = [[int(arrival_bus_seq),int(extract_dept_stop_id),time_secs_2,0,0,1,0,0]]
				predicted_arrival_time_2 = int(model.predict(request_to_model))
				print("Predicted arrival time to the arrival bus stop is",predicted_arrival_time_2)


			if(day_of_week=="Tuesday"):

				request_to_model = [[int(departure_bus_seq),int(extract_arr_stop_id),time_secs_1,0,0,0,1,0]]
				gc.disable()
				model = cPickle.load(open(model_file,'rb'))
				gc.enable()
				predicted_arrival_time_1 = int(model.predict(request_to_model))
				print("Predicted arrival time to the departure bus stop is",predicted_arrival_time_1)
				request_to_model = [[int(arrival_bus_seq),int(extract_dept_stop_id),time_secs_2,0,0,0,1,0]]
				predicted_arrival_time_2 = int(model.predict(request_to_model))
				print("Predicted arrival time to the arrival bus stop is",predicted_arrival_time_2)


			if(day_of_week=="Wednesday"):

				request_to_model = [[int(departure_bus_seq),int(extract_arr_stop_id),time_secs_1,0,0,0,0,1]]
				gc.disable()
				model = cPickle.load(open(model_file,'rb'))
				gc.enable()
				predicted_arrival_time_1 = int(model.predict(request_to_model))
				print("Predicted arrival time to the departure bus stop is",predicted_arrival_time_1)
				request_to_model = [[int(arrival_bus_seq),int(extract_dept_stop_id),time_secs_2,0,0,0,0,1]]
				predicted_arrival_time_2 = int(model.predict(request_to_model))
				print("Predicted arrival time to the arrival bus stop is",predicted_arrival_time_2)
		
		#This is for bus lines operating Monday-Sunday
		else: 
			file_name = bus_line+'.pickle'
			model_file = os.path.join(CURRENT_DIR, file_name)
			if(day_of_week=="Monday"):
				request_to_model = [[int(departure_bus_seq),int(extract_arr_stop_id),time_secs_1,1,0,0,0,0,0]]
				gc.disable()
				model = cPickle.load(open(model_file,'rb'))
				gc.enable()
				predicted_arrival_time_1 = int(model.predict(request_to_model))
				print("Predicted arrival time to the departure bus stop is",predicted_arrival_time_1)
				request_to_model = [[int(arrival_bus_seq),int(extract_dept_stop_id),time_secs_2,1,0,0,0,0,0]]
				predicted_arrival_time_2 = int(model.predict(request_to_model))
				print("Predicted arrival time to the arrival bus stop is",predicted_arrival_time_2)


			if(day_of_week=="Saturday"):

				request_to_model = [[int(departure_bus_seq),int(extract_arr_stop_id),time_secs_1,0,1,0,0,0,0]]
				gc.disable()
				model = cPickle.load(open(model_file,'rb'))
				gc.enable()
				predicted_arrival_time_1 = int(model.predict(request_to_model))
				print("Predicted arrival time to the departure bus stop is",predicted_arrival_time_1)
				request_to_model = [[int(arrival_bus_seq),int(extract_dept_stop_id),time_secs_2,0,1,0,0,0,0]]
				predicted_arrival_time_2 = int(model.predict(request_to_model))
				print("Predicted arrival time to the arrival bus stop is",predicted_arrival_time_2)

			if(day_of_week=="Sunday"):

				request_to_model = [[int(departure_bus_seq),int(extract_arr_stop_id),time_secs_1,0,0,1,0,0,0]]
				gc.disable()
				model = cPickle.load(open(model_file,'rb'))
				gc.enable()
				predicted_arrival_time_1 = int(model.predict(request_to_model))
				print("Predicted arrival time to the departure bus stop is",predicted_arrival_time_1)
				request_to_model = [[int(arrival_bus_seq),int(extract_dept_stop_id),time_secs_2,0,0,1,0,0,0]]
				predicted_arrival_time_2 = int(model.predict(request_to_model))
				print("Predicted arrival time to the arrival bus stop is",predicted_arrival_time_2)


			if(day_of_week=="Thursday"):

				request_to_model = [[int(departure_bus_seq),int(extract_arr_stop_id),time_secs_1,0,0,0,1,0,0]]
				gc.disable()
				model = cPickle.load(open(model_file,'rb'))
				gc.enable()
				predicted_arrival_time_1 = int(model.predict(request_to_model))
				print("Predicted arrival time to the departure bus stop is",predicted_arrival_time_1)
				request_to_model = [[int(arrival_bus_seq),int(extract_dept_stop_id),time_secs_2,0,0,0,1,0,0]]
				predicted_arrival_time_2 = int(model.predict(request_to_model))
				print("Predicted arrival time to the arrival bus stop is",predicted_arrival_time_2)


			if(day_of_week=="Tuesday"):

				request_to_model = [[int(departure_bus_seq),int(extract_arr_stop_id),time_secs_1,0,0,0,0,1,0]]
				gc.disable()
				model = cPickle.load(open(model_file,'rb'))
				gc.enable()
				predicted_arrival_time_1 = int(model.predict(request_to_model))
				print("Predicted arrival time to the departure bus stop is",predicted_arrival_time_1)
				request_to_model = [[int(arrival_bus_seq),int(extract_dept_stop_id),time_secs_2,0,0,0,0,1,0]]
				predicted_arrival_time_2 = int(model.predict(request_to_model))
				print("Predicted arrival time to the arrival bus stop is",predicted_arrival_time_2)


			if(day_of_week=="Wednesday"):

				request_to_model = [[int(departure_bus_seq),int(extract_arr_stop_id),time_secs_1,0,0,0,0,0,1]]
				gc.disable()
				model = cPickle.load(open(model_file,'rb'))
				gc.enable()
				predicted_arrival_time_1 = int(model.predict(request_to_model))
				print("Predicted arrival time to the departure bus stop is",predicted_arrival_time_1)
				request_to_model = [[int(arrival_bus_seq),int(extract_dept_stop_id),time_secs_2,0,0,0,0,0,1]]
				predicted_arrival_time_2 = int(model.predict(request_to_model))
				print("Predicted arrival time to the arrival bus stop is",predicted_arrival_time_2)

	except:
		print("Bus Line not availabe for machine learning model")










	


	
	
