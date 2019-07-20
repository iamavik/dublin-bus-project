from django.shortcuts import render
from django.http import HttpResponse
import pymysql,json
from operator import itemgetter
from . import machine_learning_tester  
from .machine_learning_tester import ml_model
from datetime import datetime
from calendar import timegm
#from .machine_learning_tester.py import *
import joblib
#import pickle
import _pickle as cPickle
import os
CURRENT_DIR = os.path.dirname(__file__)
#model_file = os.path.join(CURRENT_DIR, 'prediction_46A_cPickle.pickle')

def home(request):
	'''
	sql = "select ﻿stop_lat,stop_lon,stop_name,stop_id from mydbservlet.stops_2ttest_bus_stops where stop_name='Belfield, University College Dublin' or stop_name='Temple Bar, Aston Quay'"
	db = pymysql.connect(host="127.0.0.1",  # your host
                         user="root",  # username
                         passwd="Ganesha-46",  # password
                         db="mydbservlet")  # name of the database


	cursor = db.cursor()
	cursor.execute(sql)
	result = cursor.fetchall()
	result = json.dumps(result)
	args={}
	args['result']=result
	'''
	#print(args)

	#return render(request,'bus/index.html',args)

	return render(request,'bus/index.html')



def find_correct_stop(bus_number,headsign,closest_15_stops):
	for data in closest_15_stops:
		print("Data is",data)
		stop_id_check = data[2]
		print("Stop id is",stop_id_check)
		sql_3 = """ select distinct mydbservlet.stops_times.bus_number  from mydbservlet.stops_times 
            where mydbservlet.stops_times.bus_number=%s
            and mydbservlet.stops_times.bus_stop_number=%s and mydbservlet.stops_times.headsign=%s """
		db = pymysql.connect(host="127.0.0.1", user="root", passwd="Ganesha-46", db="mydbservlet")
		cursor = db.cursor()
		cursor.execute(sql_3,(bus_number,stop_id_check,headsign))
		query_result = cursor.fetchall()
		print("Query_result is",query_result)
		print(len(query_result))
		if(len(query_result)==1):
			break
	return list(data)


def extract_correct_depart_arrival_stop_id(departure_stop,arrival_stop,bus_number,headsign,lat1,long1,lat2,long2,result):
	try:
		#For departure bus stop
		from geopy import distance
		import numpy as np
		departure_bus_stop_location = (lat2,long2)
		distances_dept = []
		for i in result:
			stop_location = (i[0],i[1])
			dist = distance.distance(departure_bus_stop_location, stop_location).km
			distances_dept.append(dist)

    	#For departure bus stop
		closest_15_indexes = np.argsort(distances_dept)[:15] #Change 15 to any number as much as you want for nearest bus numbers
		closest_15_stops_dept = []
		for i in closest_15_indexes:
			closest_15_stops_dept.append(result[i])
		print("closest stops to your location is: ",closest_15_stops_dept)

		#For arrival bus stop

		arrival_bus_stop_location = (lat1,long1)
		distances_arrival = []
		for i in result:
			stop_location = (i[0],i[1])
			dist = distance.distance(arrival_bus_stop_location, stop_location).km
			distances_arrival.append(dist)

    	#For arrival bus stop
		closest_15_indexes = np.argsort(distances_arrival)[:15] #Change 15 to any number as much as you want for nearest bus numbers
		closest_15_stops_arrival = []
		for i in closest_15_indexes:
			closest_15_stops_arrival.append(result[i])
		print("closest stops to your location is: ",closest_15_stops_arrival)
		



		actual_departure_stop_info = find_correct_stop(bus_number,headsign,closest_15_stops_dept)
		actual_arrival_stop_info = find_correct_stop(bus_number,headsign,closest_15_stops_arrival)

		arrival_stop_id = actual_arrival_stop_info[2]
		departure_stop_id = actual_departure_stop_info[2]

				

		print("arrival_stop_id",arrival_stop_id)
		print("departure_stop_id",departure_stop_id)
		list_arrive_depart_stop_id=[]
		list_arrive_depart_stop_id.append(arrival_stop_id)
		list_arrive_depart_stop_id.append(departure_stop_id)

		return list_arrive_depart_stop_id
	except:
		#extract_correct_depart_arrival_stop_id(departure_stop,arrival_stop,bus_number,headsign)
		return 0



def extract_seq_numbers_bus_stops(headsign,bus_number,arrival_stop_id,departure_stop_id,number_of_stops,bus_at_departure_stop,bus_at_arrival_stop,departure_date):
	#23-06 Adding Code
			
	sql_2 = """select mydbservlet.stops_times.bus_stop_number,mydbservlet.stops_times.stop_sequence,mydbservlet.trips_info_bus_number.direction_id,mydbservlet.stops_times.headsign,mydbservlet.stops_times.bus_number,
		mydbservlet.stops_times.trip_id from mydbservlet.stops_times,
		mydbservlet.trips_info_bus_number where stops_times.trip_id = trips_info_bus_number.trip_id and stops_times.headsign=%s
		and stops_times.bus_number = %s and (bus_stop_number=%s or bus_stop_number=%s) """
	db = pymysql.connect(host="127.0.0.1", user="root", passwd="Ganesha-46", db="mydbservlet")
	cursor = db.cursor()
	cursor.execute(sql_2,(headsign,bus_number,arrival_stop_id,departure_stop_id,))
	seq_numbers = cursor.fetchall()
	print(seq_numbers)
	seq_numbers = list(seq_numbers)
	print("length of sequence numbers is",len(seq_numbers))
	if(len(seq_numbers)>2):
		i = 0
		while(i<len(seq_numbers)-1):
			if( seq_numbers[i+1][1]-seq_numbers[i][1]==number_of_stops):
				departure_bus_seq = seq_numbers[i][1]
				arrival_bus_seq = seq_numbers[i+1][1]
				headsign_seq = seq_numbers[i][3]
				direction_id = seq_numbers[i][2]
				trip_id = seq_numbers[i][5]
				print("departure_bus_seq",departure_bus_seq)
				print("arrival_bus_seq",arrival_bus_seq)
				print("headsign",headsign_seq)
				print("trip id", trip_id)
				break
			else:
				departure_bus_seq = seq_numbers[0][1]
				arrival_bus_seq = seq_numbers[1][1]
				headsign_seq = seq_numbers[0][3]
				direction_id = seq_numbers[0][2]
				trip_id = seq_numbers[0][5]
				print("inside while-else")
				print("departure_bus_seq",departure_bus_seq)
				print("arrival_bus_seq",arrival_bus_seq)
				print("headsign",headsign_seq)
				print("trip id", trip_id)
				i+=1


	else:
		departure_bus_seq = seq_numbers[0][1]
		arrival_bus_seq = seq_numbers[1][1]
		headsign_seq = seq_numbers[0][3]
		direction_id = seq_numbers[0][2]
		trip_id = seq_numbers[0][5]
		print("departure_bus_seq",departure_bus_seq)
		print("arrival_bus_seq",arrival_bus_seq)
		print("headsign",headsign_seq)
		print("trip id", trip_id)

	if(departure_bus_seq>arrival_bus_seq):
		exchange = departure_bus_seq
		departure_bus_seq = arrival_bus_seq
		arrival_bus_seq = exchange

	sql_intermed_bus_stops = """select distinct mydbservlet.stops_times.bus_stop_number,mydbservlet.stops_times.stop_sequence,
						mydbservlet.stops_2ttest_bus_stops.﻿stop_lat,
						mydbservlet.stops_2ttest_bus_stops.stop_lon,mydbservlet.stops_2ttest_bus_stops.stop_name,mydbservlet.stops_times.bus_number from mydbservlet.stops_2ttest_bus_stops,
						mydbservlet.stops_times,mydbservlet.trips_info_bus_number where mydbservlet.stops_2ttest_bus_stops.stop_id = mydbservlet.stops_times.bus_stop_number and stops_times.trip_id = trips_info_bus_number.trip_id and  stops_times.bus_number=%s 
						and stops_times.headsign = %s and stops_times.stop_sequence between %s and %s and trips_info_bus_number.direction_id=%s and mydbservlet.stops_times.trip_id=%s  order by mydbservlet.stops_times.stop_sequence"""

	cursor = db.cursor()
	#cursor.execute(sql_intermed_bus_stops,(bus_number,headsign_seq,int(departure_bus_seq)+1,int(arrival_bus_seq)-1,))
	cursor.execute(sql_intermed_bus_stops,(bus_number,headsign_seq,int(departure_bus_seq),int(arrival_bus_seq),int(direction_id),trip_id,))
	intermediate_bus_stops = cursor.fetchall()

	print("intermediate bus stops",intermediate_bus_stops)
	seen = set()
	seen_add = seen.add
	remove_duplicates = [x for x in intermediate_bus_stops if not (x[0] in seen or seen_add(x[0]))]

	print("Length of intermediate_bus_stops",len(intermediate_bus_stops))
	remove_duplicates = [x for x in remove_duplicates if not (x[1] in seen or seen_add(x[1]))]
	print("Length of intermediate_bus_stops remove duplicates",len(remove_duplicates))
	
	print("List of sequence bus stops after removing duplicates",remove_duplicates)

	ml_model(bus_number,departure_bus_seq,arrival_bus_seq,arrival_stop_id,departure_stop_id,bus_at_departure_stop,bus_at_arrival_stop,departure_date)
	'''
	if(bus_number=="46a"):
		print("Now calling machine learning model..testing only for 46A")
		test_ml_model_46A(bus_number,departure_bus_seq,arrival_bus_seq,arrival_stop_id,departure_stop_id,bus_at_departure_stop,bus_at_arrival_stop)
	'''
	return(remove_duplicates)


def get_transit_details(transit_route):
	if(len(transit_route['legs'][0]['steps'])==4):

		departure_stop = transit_route['legs'][0]['steps'][1]['transit_details']['departure_stop']['name']
		bus_at_departure_stop = transit_route['legs'][0]['steps'][1]['transit_details']['departure_time']['text']
		headsign_first = transit_route['legs'][0]['steps'][1]['transit_details']['headsign']
		bus_number_first = transit_route['legs'][0]['steps'][1]['transit_details']['line']['short_name']
		#bus_num = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['line']['short_name']
		number_of_stops_first = transit_route['legs'][0]['steps'][1]['transit_details']['num_stops']
		arrival_stop_transit = transit_route['legs'][0]['steps'][1]['transit_details']['arrival_stop']['name']
		bus_at_intermediate_transfer_stop = transit_route['legs'][0]['steps'][1]['transit_details']['arrival_time']['text'] #Added 17-07 appended end of the list_with_direction
		
		lat1 = transit_route['legs'][0]['steps'][1]['transit_details']['arrival_stop']['location']['lat']
		long1 = transit_route['legs'][0]['steps'][1]['transit_details']['arrival_stop']['location']['lng']
		lat2 = transit_route['legs'][0]['steps'][1]['transit_details']['departure_stop']['location']['lat']
		long2 = transit_route['legs'][0]['steps'][1]['transit_details']['departure_stop']['location']['lng']
		transit = "Transfer"
		if(transit_route['legs'][0]['steps'][2]["travel_mode"]=="TRANSIT"):
			departure_stop_transit = transit_route['legs'][0]['steps'][2]['transit_details']['departure_stop']['name']
			bus_at_transit_departure_stop = transit_route['legs'][0]['steps'][2]['transit_details']['departure_time']['text']
			headsign_second = transit_route['legs'][0]['steps'][2]['transit_details']['headsign']
			bus_number_second = transit_route['legs'][0]['steps'][2]['transit_details']['line']['short_name']
			#bus_num = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['line']['short_name']
			number_of_stops_second = transit_route['legs'][0]['steps'][2]['transit_details']['num_stops']
			arrival_stop_final = transit_route['legs'][0]['steps'][2]['transit_details']['arrival_stop']['name']
			bus_at_final_destination_stop = transit_route['legs'][0]['steps'][2]['transit_details']['arrival_time']['text']
			lat3 = transit_route['legs'][0]['steps'][2]['transit_details']['arrival_stop']['location']['lat']
			long3 = transit_route['legs'][0]['steps'][2]['transit_details']['arrival_stop']['location']['lng']
			lat4 = transit_route['legs'][0]['steps'][2]['transit_details']['departure_stop']['location']['lat']
			long4 = transit_route['legs'][0]['steps'][2]['transit_details']['departure_stop']['location']['lng']

			list_with_direction = [departure_stop,bus_at_departure_stop,headsign_first,bus_number_first,number_of_stops_first,arrival_stop_transit,transit,departure_stop_transit,bus_at_transit_departure_stop,headsign_second,bus_number_second,number_of_stops_second,arrival_stop_final,bus_at_final_destination_stop,bus_at_intermediate_transfer_stop,lat1,long1,lat2,long2,lat3,long3,lat4,long4]
		else:
			departure_stop_transit = transit_route['legs'][0]['steps'][3]['transit_details']['departure_stop']['name']
			bus_at_transit_departure_stop = transit_route['legs'][0]['steps'][3]['transit_details']['departure_time']['text']
			headsign_second = transit_route['legs'][0]['steps'][3]['transit_details']['headsign']
			bus_number_second = transit_route['legs'][0]['steps'][3]['transit_details']['line']['short_name']
			#bus_num = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['line']['short_name']
			number_of_stops_second = transit_route['legs'][0]['steps'][3]['transit_details']['num_stops']
			arrival_stop_final = transit_route['legs'][0]['steps'][3]['transit_details']['arrival_stop']['name']
			bus_at_final_destination_stop = transit_route['legs'][0]['steps'][3]['transit_details']['arrival_time']['text'];
			lat3 = transit_route['legs'][0]['steps'][3]['transit_details']['arrival_stop']['location']['lat']
			long3 = transit_route['legs'][0]['steps'][3]['transit_details']['arrival_stop']['location']['lng']
			lat4 = transit_route['legs'][0]['steps'][3]['transit_details']['departure_stop']['location']['lat']
			long4 = transit_route['legs'][0]['steps'][3]['transit_details']['departure_stop']['location']['lng']
			list_with_direction = [departure_stop,bus_at_departure_stop,headsign_first,bus_number_first,number_of_stops_first,arrival_stop_transit,transit,departure_stop_transit,bus_at_transit_departure_stop,headsign_second,bus_number_second,number_of_stops_second,arrival_stop_final,bus_at_final_destination_stop,bus_at_intermediate_transfer_stop,lat1,long1,lat2,long2,lat3,long3,lat4,long4]

		

	if(len(transit_route['legs'][0]['steps'])==5):

		departure_stop = transit_route['legs'][0]['steps'][1]['transit_details']['departure_stop']['name']
		bus_at_departure_stop = transit_route['legs'][0]['steps'][1]['transit_details']['departure_time']['text']
		headsign_first = transit_route['legs'][0]['steps'][1]['transit_details']['headsign']
		bus_number_first = transit_route['legs'][0]['steps'][1]['transit_details']['line']['short_name']
		#bus_num = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['line']['short_name']
		number_of_stops_first = transit_route['legs'][0]['steps'][1]['transit_details']['num_stops']
		arrival_stop_transit = transit_route['legs'][0]['steps'][1]['transit_details']['arrival_stop']['name']
		bus_at_intermediate_transfer_stop = transit_route['legs'][0]['steps'][1]['transit_details']['arrival_time']['text']

		lat1 = transit_route['legs'][0]['steps'][1]['transit_details']['arrival_stop']['location']['lat']
		long1 = transit_route['legs'][0]['steps'][1]['transit_details']['arrival_stop']['location']['lng']
		lat2 = transit_route['legs'][0]['steps'][1]['transit_details']['departure_stop']['location']['lat']
		long2 = transit_route['legs'][0]['steps'][1]['transit_details']['departure_stop']['location']['lng']

		transit = "Transfer"
		departure_stop_transit = transit_route['legs'][0]['steps'][3]['transit_details']['departure_stop']['name']
		bus_at_transit_departure_stop = transit_route['legs'][0]['steps'][3]['transit_details']['departure_time']['text']
		headsign_second = transit_route['legs'][0]['steps'][3]['transit_details']['headsign']
		bus_number_second = transit_route['legs'][0]['steps'][3]['transit_details']['line']['short_name']
		#bus_num = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['line']['short_name']
		number_of_stops_second = transit_route['legs'][0]['steps'][3]['transit_details']['num_stops']
		arrival_stop_final = transit_route['legs'][0]['steps'][3]['transit_details']['arrival_stop']['name']
		bus_at_final_destination_stop = transit_route['legs'][0]['steps'][3]['transit_details']['arrival_time']['text'];

		lat3 = transit_route['legs'][0]['steps'][3]['transit_details']['arrival_stop']['location']['lat']
		long3 = transit_route['legs'][0]['steps'][3]['transit_details']['arrival_stop']['location']['lng']
		lat4 = transit_route['legs'][0]['steps'][3]['transit_details']['departure_stop']['location']['lat']
		long4 = transit_route['legs'][0]['steps'][3]['transit_details']['departure_stop']['location']['lng']
		list_with_direction = [departure_stop,bus_at_departure_stop,headsign_first,bus_number_first,number_of_stops_first,arrival_stop_transit,transit,departure_stop_transit,bus_at_transit_departure_stop,headsign_second,bus_number_second,number_of_stops_second,arrival_stop_final,bus_at_final_destination_stop,bus_at_intermediate_transfer_stop,lat1,long1,lat2,long2,lat3,long3,lat4,long4]

	return list_with_direction





def unix_time(dttm=None):
	from datetime import datetime
	from calendar import timegm
	if dttm is None:
		dttm = datetime.utcnow()
	return timegm(dttm.utctimetuple())

	

def findroutedetails(request):
	source = request.POST['origin']
	destination = request.POST['destination']
	departure_date = request.POST.get('departure_date', False)
	departure_time = request.POST.get('departure_time', False)
	
	print(source)
	print(destination)
	print("Departure date is",departure_date)
	print("Departure time  is",departure_time)
	

	if(departure_date=='' and departure_time==''):
		#now = datetime.now()
		departure_date_time = unix_time()
	elif(departure_date=='' and departure_time!=''):
		x = str(datetime.now())
		date_today = x[0:10].split('-')
		time_hr_min = str(departure_time).split(':')
		departure_date_time = unix_time(datetime(int(date_today[0]),int(date_today[1]),int(date_today[2]),int(time_hr_min[0])-1,int(time_hr_min[1])))

	else:
		date_requested = str(departure_date).split('-')
		time_hr_min = str(departure_time).split(':')

		departure_date_time = unix_time(datetime(int(date_requested[0]),int(date_requested[1]),int(date_requested[2]),int(time_hr_min[0])-1,int(time_hr_min[1])))




# Note: if you pass in a naive dttm object it's assumed to already be in UTC




	# importing required libraries 
	import requests, json, pymysql

	'''

	# enter your api key here 
	api_key ='AIzaSyBi-bH5_sngxNibrgygRZDhmAv2fK5hzus'
	#UniversityCollegeDublin,Dublin
	# Take source as input 
	origin = source 

	# Take destination as input 
	dest = destination 

	# url variable store url 
	url ='https://maps.googleapis.com/maps/api/directions/json?alternatives=true&'

	#https://maps.googleapis.com/maps/api/directions/json?alternatives=true&origin=bieberstrasse,+dusseldorf&destination=norf,+neuss&sensor=false&mode=transit&departure_time=1399399424&key=AIzaSyBi-bH5_sngxNibrgygRZDhmAv2fK5hzus
	#API to get alternate routes
	#https://maps.googleapis.com/maps/api/directions/json?alternatives=true&origin=universitycollegedublin&destination=templebar,dublin&sensor=false&mode=transit&key=AIzaSyBi-bH5_sngxNibrgygRZDhmAv2fK5hzus
	# Get method of requests module 
	# return response object 

	r = requests.get(url + 'origin=' + source +'&destination=' + dest+'&sensor='+"false"+'&mode='+"transit"+'&key=' + api_key) 

	# json method of response object 
	# return json format result 
	x = r.json() 
	'''

	
	import googlemaps
	

	gmaps = googlemaps.Client(key='AIzaSyBi-bH5_sngxNibrgygRZDhmAv2fK5hzus')


	#now = datetime.now()
	x = gmaps.directions(origin=source,
                                     destination=destination,
                                     alternatives="true",
                                     mode="transit",
                                     transit_mode="bus",
                                     departure_time=departure_date_time
                                     
                                     
                                    )
	#departure_time=now has to be added after transit_mode

	#https://maps.googleapis.com/maps/api/directions/json?origin=Brooklyn&destination=Queens&departure_time=1563043538093&mode=transit&key=AIzaSyBi-bH5_sngxNibrgygRZDhmAv2fK5hzus







	

	# bydefault driving mode considered 

	# print the vale of x 
	#print(x['geocoded_waypoints']) 
	#print(x['routes'])
	#print(x['geocoded_waypoints']) 
	#print("-----------------------------------")
	if(len(x)!=0):
	#if(len(x['routes'])!=0): Change made on 11/07 after adding python Google Maps interface
		sql_2 = """select distinct mydbservlet.stops_times.bus_number from mydbservlet.stops_times"""
		db = pymysql.connect(host="127.0.0.1", user="root", passwd="Ganesha-46", db="mydbservlet")
		cursor = db.cursor()
		cursor.execute(sql_2,)
		list_all_bus_numbers = cursor.fetchall()
		list_all_bus_numbers = list(list_all_bus_numbers)
		print("List of all Bus Numbers in Dublin",list_all_bus_numbers)
		list_with_alternate_routes = []
		list_intermediate_bus_stops_alternate_stops = []
		sql = """select ﻿stop_lat,stop_lon,stop_id,stop_name,STOP_ID_LAST_4 from mydbservlet.stops_2ttest_bus_stops""" 
		db = pymysql.connect(host="127.0.0.1", user="root", passwd="Ganesha-46", db="mydbservlet")
		cursor = db.cursor()
		cursor.execute(sql,)
		result = list(cursor.fetchall())
		for i in x:
		#for i in x['routes']: Change made on 11/07 after adding python Google Maps interface
			if(len(i['legs'][0]['steps'])==3 ):

				total_duration = i['legs'][0]['duration']['text']
			#print("-----------------------------------")
				total_time = i['legs'][0]['distance']['text']
				html_inst1 = i['legs'][0]['steps'][0]['html_instructions']
				dist_bus_stop_walk = i['legs'][0]['steps'][0]['distance']['text']
				time_to_bus_stop_walk = i['legs'][0]['steps'][0]['duration']['text']
				html_inst2 = i['legs'][0]['steps'][1]['html_instructions']
				bus_distance = i['legs'][0]['steps'][1]['distance']['text']
				bus_time = i['legs'][0]['steps'][1]['duration']['text']
				departure_stop = i['legs'][0]['steps'][1]['transit_details']['departure_stop']['name']
				#dept_stop = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['departure_stop']['name']
				bus_at_departure_stop = i['legs'][0]['steps'][1]['transit_details']['departure_time']['text']
				headsign = i['legs'][0]['steps'][1]['transit_details']['headsign']
				bus_number = i['legs'][0]['steps'][1]['transit_details']['line']['short_name']
				#bus_num = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['line']['short_name']
				number_of_stops = i['legs'][0]['steps'][1]['transit_details']['num_stops']
				arrival_stop = i['legs'][0]['steps'][1]['transit_details']['arrival_stop']['name']
				#arr_stop = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['arrival_stop']['name']
				html_inst3 = i['legs'][0]['steps'][2]['html_instructions']
				distance_to_dest = i['legs'][0]['steps'][2]['distance']['text']
				time_by_walk_dest = i['legs'][0]['steps'][2]['duration']['text']
				#bus_at_arrival_stop newly added
				bus_at_arrival_stop = i['legs'][0]['steps'][1]['transit_details']['arrival_time']['text']
				print("Departure Stop no bus transfer",departure_stop)
				print("Arrival stop no bus transfer",arrival_stop)
				print("Headsign no bus transfer",headsign)
				list_with_direction = [total_duration, total_time,html_inst1,dist_bus_stop_walk,time_to_bus_stop_walk,html_inst2,bus_distance,bus_time,departure_stop,bus_at_departure_stop,headsign,bus_number,number_of_stops,arrival_stop,html_inst3,distance_to_dest,bus_at_arrival_stop,time_by_walk_dest]
				list_with_alternate_routes.append(list_with_direction)

				print("Bus number is",bus_number)
				lat1 = i['legs'][0]['steps'][1]['transit_details']['arrival_stop']['location']['lat']
				long1 = i['legs'][0]['steps'][1]['transit_details']['arrival_stop']['location']['lng']
				lat2 = i['legs'][0]['steps'][1]['transit_details']['departure_stop']['location']['lat']
				long2 = i['legs'][0]['steps'][1]['transit_details']['departure_stop']['location']['lng']
				if(i['legs'][0]['steps'][1]['transit_details']['line']['short_name'].upper() in list(map(itemgetter(0),list_all_bus_numbers))):

					departure_stop ='%'+departure_stop+'%'
					arrival_stop ='%'+arrival_stop+'%'

					list_arrive_depart_stop_id=extract_correct_depart_arrival_stop_id(departure_stop,arrival_stop,bus_number,headsign,lat1,long1,lat2,long2,result)
					print("Return of extract_correct_depart_arrival_stop_id",list_arrive_depart_stop_id)
					if(list_arrive_depart_stop_id!=0):
						arrival_stop_id = list_arrive_depart_stop_id[0]
						departure_stop_id = list_arrive_depart_stop_id[1]
						
						number_of_stops = int(number_of_stops)
						print("Bus Number is",bus_number)
						remove_duplicates = extract_seq_numbers_bus_stops(headsign,bus_number,arrival_stop_id,departure_stop_id,number_of_stops,bus_at_departure_stop,bus_at_arrival_stop,departure_date)
						
						list_intermediate_bus_stops_alternate_stops.append(remove_duplicates)
						print("-----------------------------------------------------------------------------------------")
					else: #This else is doing error handling if list_arrive_depart_stop_id returns 0 in case of a database failure
						pass
				else:
					#pass
					list_intermediate_bus_stops_alternate_stops.append([])


			elif(len(i['legs'][0]['steps'])==4 or len(i['legs'][0]['steps'])==5 ):
				
				print("Routes from google apis",i)
				list_with_direction = get_transit_details(i)
				list_with_alternate_routes.append(list_with_direction)

				departure_stop = list_with_direction[0]
				bus_at_departure_stop = list_with_direction[1]
				headsign_first = list_with_direction[2]
				bus_number_first = list_with_direction[3]
				number_of_stops_first = list_with_direction[4]
				arrival_stop_transit = list_with_direction[5]
				bus_at_intermediate_transfer_stop = list_with_direction[14]
				lat1 = list_with_direction[15]
				long1 = list_with_direction[16]
				lat2 = list_with_direction[17]
				long2 = list_with_direction[18]
				lat3 = list_with_direction[19]
				long3 = list_with_direction[20]
				lat4 = list_with_direction[21]
				long4 = list_with_direction[22]

				departure_stop_transit = list_with_direction[7]
				bus_at_transit_departure_stop = list_with_direction[8]
				headsign_second = list_with_direction[9]
				bus_number_second = list_with_direction[10]
				number_of_stops_second = list_with_direction[11]
				arrival_stop_final = list_with_direction[12]
				bus_at_final_destination_stop = list_with_direction[13]
				print("Bus Number first is",bus_number_first)
				print("Bus Number second is",bus_number_second)
				print("Departure Stop",departure_stop)
				print("Arrival stop transit",arrival_stop_transit)
				print("Departure Stop Transit",departure_stop_transit)
				print("Arrival Stop Final",arrival_stop_final)

				if(bus_number_first.upper() in list(map(itemgetter(0),list_all_bus_numbers)) and bus_number_second.upper() in list(map(itemgetter(0),list_all_bus_numbers))):
					print("Inside bus_number_first and bus_number_second")
					list_remove_duplicates = []
					departure_stop ='%'+departure_stop+'%'
					arrival_stop_transit ='%'+arrival_stop_transit+'%'

					list_arrive_depart_stop_id=extract_correct_depart_arrival_stop_id(departure_stop,arrival_stop_transit,bus_number_first,headsign_first,lat1,long1,lat2,long2,result)
					if(list_arrive_depart_stop_id!=0):
						arrival_stop_id_first = list_arrive_depart_stop_id[0]
						departure_stop_id_first = list_arrive_depart_stop_id[1]
						
						number_of_stops_first = int(number_of_stops_first)
						print("Bus Number first is",bus_number_first)
						remove_duplicates = extract_seq_numbers_bus_stops(headsign_first,bus_number_first,arrival_stop_id_first,departure_stop_id_first,number_of_stops_first,bus_at_departure_stop,bus_at_intermediate_transfer_stop,departure_date)
						list_remove_duplicates.append(remove_duplicates)

						#---------------------TRANSIT PART SECOND LEG INFO-------------------------------------------#	
						departure_stop_transit ='%'+departure_stop_transit+'%'
						arrival_stop_final ='%'+arrival_stop_final+'%'
						list_arrive_depart_stop_id=extract_correct_depart_arrival_stop_id(departure_stop_transit,arrival_stop_final,bus_number_second,headsign_second,lat3,long3,lat4,long4,result)
						if(list_arrive_depart_stop_id!=0 and len(remove_duplicates)>=0):

							arrival_stop_id_second = list_arrive_depart_stop_id[0]
							departure_stop_id_second = list_arrive_depart_stop_id[1]
							
							number_of_stops_second = int(number_of_stops_second)
							print("Bus Number second is",bus_number_second)
							remove_duplicates = extract_seq_numbers_bus_stops(headsign_second,bus_number_second,arrival_stop_id_second,departure_stop_id_second,number_of_stops_second,bus_at_transit_departure_stop,bus_at_final_destination_stop,departure_date)
							
							#Add a check if remove_duplicates is [],pop the intermediate bus stops inserted for first leg
							list_remove_duplicates.append(remove_duplicates)
							list_intermediate_bus_stops_alternate_stops.append(list_remove_duplicates)
						else:
							#list_with_alternate_routes.pop() #No need to remove the direction data just pass
							pass
					else:
						#list_with_alternate_routes.pop()
						pass



					



				else:
					#pass
					list_intermediate_bus_stops_alternate_stops.append([])

		'''

		seq_numbers = list(seq_numbers)
		if(len(seq_numbers)>2):
			selected_seq_numbers = [0]*2
			i = 0
			if(i<len(seq_numbers) and seq_numbers[i]!=seq_numbers[i+1]):


		'''
		print("-----------------------------------------------------------------------------------------")
		print("List of intermediate_bus_stops_with individual sequence numbers",list_intermediate_bus_stops_alternate_stops)
		list_bus_lines = []
		for i in list_intermediate_bus_stops_alternate_stops:
			#if(len(i))
			if(len(i)!=0  and isinstance(i[0][0],str) == True):

				print(len(i))
				print(i[0])
				list_bus_lines.append(i[0][5])
			else:
				if(len(i)==2):
					appended_bus_line = i[0][0][5]+'/'+i[1][0][5]
					list_bus_lines.append(appended_bus_line)
				elif(len(i)==3):
					appended_bus_line = i[0][0][5]+'/'+i[1][0][5] +'/'+i[2][0][5]
					list_bus_lines.append(appended_bus_line)
				else:
					list_bus_lines.append([])

		print("List of bus lines from back end for user",list_bus_lines)
		#args={}
		#result = json.dumps(result)
		#args['result']=result
		#return HttpResponse(json.dumps({'result': result, 'list_with_alternate_routes': list_with_alternate_routes,'list_intermediate_bus_stops_alternate_stops':list_intermediate_bus_stops_alternate_stops,'list_bus_lines':list_bus_lines,'departure_date_time':departure_date_time}))
		
		return HttpResponse(json.dumps({'list_with_alternate_routes': list_with_alternate_routes,'list_intermediate_bus_stops_alternate_stops':list_intermediate_bus_stops_alternate_stops,'list_bus_lines':list_bus_lines,'departure_date_time':departure_date_time}))
	else:
		return HttpResponse("Error")


	

	#return HttpResponse(result)
	#return render(request,'bus/real_time_route.html',args)



def getweatherdetails(request):

	import requests, json, pymysql
	url = "http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=a4822db1b5634c2e9e25209d1837cc69&units=metric"
	r = requests.get(url)
	weather_data = r.json() 
	#print(weather_data.weather[0].main)
	#print(weather_data.main.temp)
	#print(weather_data)
	return HttpResponse(json.dumps({'weather_data': weather_data}))

def getnearestbusstops(request):
	try:

		from geopy.distance import great_circle
		from geopy import distance
		import numpy as np

		user_lat = request.POST['current_latitude']
		user_lng = request.POST['current_longitude']
		print("user's lat: ",user_lat)
		print("user's longitude: ",user_lng)
		user_location = (user_lat, user_lng)
		sql_4 = "SELECT * FROM mydbservlet.stops_2ttest_bus_stops"
		db = pymysql.connect(host="127.0.0.1", user="root", passwd="Ganesha-46", db="mydbservlet")
		cursor = db.cursor()
		cursor.execute(sql_4,)
		list_stop_details = cursor.fetchall()
		list_stop_details = list(list_stop_details)
		distances = []
		for i in list_stop_details:
			stop_location = (i[1],i[3])
			dist = distance.distance(user_location, stop_location).km
			distances.append(dist)
		closest_3_indexes = np.argsort(distances)[:7] #Change 7 to any number as much as you want for nearest bus numbers
		closest_3_stops = []
		for i in closest_3_indexes:
			closest_3_stops.append(list_stop_details[i])
		print("closest stops to your location is: ",closest_3_stops)
		closest_3_stops_bus_info = []

		for i in closest_3_stops:
			sql4 = "SELECT distinct bus_number,headsign FROM mydbservlet.stops_times where bus_stop_number=%s "
			cursor.execute(sql4,(i[4]),)
			list_buses_passing_a_stop = cursor.fetchall()
			print(list_buses_passing_a_stop)
			list_buses_passing_a_stop = list(list_buses_passing_a_stop)
			closest_3_stops_bus_info.append(list_buses_passing_a_stop)
		print("bus lines in 3 closest bus stops",closest_3_stops_bus_info)




		return HttpResponse(json.dumps({'closest_3_stops': closest_3_stops, 'closest_3_stops_bus_info': closest_3_stops_bus_info}))

	except:
		return("Error")




def about(request):
	return HttpResponse('<h1>BUS ABOUT</h1>')
'''
def search(request):
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

    path('search/',views.search,name='bus-test-stop')
'''
#args = {}   args['result'] = result
    


