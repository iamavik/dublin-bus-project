from django.shortcuts import render
from django.http import HttpResponse
import pymysql,json
from operator import itemgetter

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

def extract_correct_depart_arrival_stop_id(departure_stop,arrival_stop,bus_number,headsign):
	try:
		sql = """select ﻿stop_lat,stop_lon,stop_id,STOP_ID_LAST_4,stop_name from mydbservlet.stops_2ttest_bus_stops where stop_name LIKE %s or stop_name LIKE %s""" 
		db = pymysql.connect(host="127.0.0.1", user="root", passwd="Ganesha-46", db="mydbservlet")
		cursor = db.cursor()
		cursor.execute(sql,(departure_stop,arrival_stop,))
		result = cursor.fetchall()
				
		#result = json.dumps(result)
				
		result = list(result)
		print(result)
		print("Length of result is",len(result))
		#The following if is to handle a case where for length 2, the bus stop name are exactly same. "townsend st. garda station" issue. Bus stop id is 340
		if(len(result)==2 and result[0][4]==result[1][4]):
			#departure_stop = departure_stop.replace('%','')
			arrival_stop = arrival_stop.replace('%','')
			arrival_stop = arrival_stop.split()
			arrival_stop = "%"+arrival_stop[len(arrival_stop)-1]
			extract_correct_depart_arrival_stop_id(departure_stop,arrival_stop,bus_number,headsign)
			#departure_stop = departure_stop.split()
			#arrival_stop = arrival_stop.split()
			#if(result[0][4]!= arrival_stop):


		#Code added on 23-06
		if(len(result)>2):
			new_result = [0]*2
			for data in result:
				print("Data is",data)
				stop_id_check = data[2]
				sql_3 = """ select distinct mydbservlet.stops_times.bus_number  from mydbservlet.stops_times 
					where mydbservlet.stops_times.bus_number=%s
					and mydbservlet.stops_times.bus_stop_number=%s and mydbservlet.stops_times.headsign=%s """
				db = pymysql.connect(host="127.0.0.1", user="root", passwd="Ganesha-46", db="mydbservlet")
				cursor = db.cursor()
				cursor.execute(sql_3,(bus_number,stop_id_check,headsign))
				query_result = cursor.fetchall()
				print("Query_result is",query_result)
				if(len(query_result)!=0):
					new_result.append(data)
					new_result = list(filter(lambda a: a != 0, new_result))
			print("New result is ",new_result)
			result = new_result

		i = 0
		while(True):
			if(result[i][4]!=result[i+1][4]):
				arrival_stop_id = result[i][2]
				departure_stop_id = result[i+1][2]
				break
			else:
				i+=1
		list_arrive_depart_stop_id=[]
		list_arrive_depart_stop_id.append(arrival_stop_id)
		list_arrive_depart_stop_id.append(departure_stop_id)
		list_arrive_depart_stop_id.append(result)

		return list_arrive_depart_stop_id
	except:
		#extract_correct_depart_arrival_stop_id(departure_stop,arrival_stop,bus_number,headsign)
		return 0



def extract_seq_numbers_bus_stops(headsign,bus_number,arrival_stop_id,departure_stop_id,number_of_stops):
	#23-06 Adding Code
			
	sql_2 = """select mydbservlet.stops_times.bus_stop_number,mydbservlet.stops_times.stop_sequence,mydbservlet.trips_info_bus_number.direction_id,mydbservlet.stops_times.headsign from mydbservlet.stops_times,
		mydbservlet.trips_info_bus_number where stops_times.trip_id = trips_info_bus_number.trip_id and stops_times.headsign=%s
		and stops_times.bus_number = %s and (bus_stop_number=%s or bus_stop_number=%s)"""
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
				print("departure_bus_seq",departure_bus_seq)
				print("arrival_bus_seq",arrival_bus_seq)
				print("headsign",headsign_seq)
				break
			else:
				departure_bus_seq = seq_numbers[0][1]
				arrival_bus_seq = seq_numbers[1][1]
				headsign_seq = seq_numbers[0][3]
				print("inside while-else")
				print("departure_bus_seq",departure_bus_seq)
				print("arrival_bus_seq",arrival_bus_seq)
				print("headsign",headsign_seq)
				i+=1


	else:
		departure_bus_seq = seq_numbers[0][1]
		arrival_bus_seq = seq_numbers[1][1]
		headsign_seq = seq_numbers[0][3]
		print("departure_bus_seq",departure_bus_seq)
		print("arrival_bus_seq",arrival_bus_seq)
		print("headsign",headsign_seq)

	if(departure_bus_seq>arrival_bus_seq):
		exchange = departure_bus_seq
		departure_bus_seq = arrival_bus_seq
		arrival_bus_seq = exchange

	sql_intermed_bus_stops = """select distinct mydbservlet.stops_times.bus_stop_number,mydbservlet.stops_times.stop_sequence,
						mydbservlet.stops_2ttest_bus_stops.﻿stop_lat,
						mydbservlet.stops_2ttest_bus_stops.stop_lon,mydbservlet.stops_2ttest_bus_stops.stop_name from mydbservlet.stops_2ttest_bus_stops,
						mydbservlet.stops_times where mydbservlet.stops_2ttest_bus_stops.stop_id = mydbservlet.stops_times.bus_stop_number and  stops_times.bus_number=%s 
						and stops_times.headsign = %s and stops_times.stop_sequence between %s and %s """

	cursor = db.cursor()
	cursor.execute(sql_intermed_bus_stops,(bus_number,headsign_seq,int(departure_bus_seq)+1,int(arrival_bus_seq)-1,))
	intermediate_bus_stops = cursor.fetchall()
	print("intermediate bus stops",intermediate_bus_stops)
	seen = set()
	seen_add = seen.add
	remove_duplicates = [x for x in intermediate_bus_stops if not (x[1] in seen or seen_add(x[1]))]
	print("Length of intermediate_bus_stops",len(intermediate_bus_stops))
	print("Length of intermediate_bus_stops remove duplicates",len(remove_duplicates))
	
	print("List of sequence bus stops after removing duplicates",remove_duplicates)

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
		transit = "transit"
		departure_stop_transit = transit_route['legs'][0]['steps'][2]['transit_details']['departure_stop']['name']
		bus_at_transit_departure_stop = transit_route['legs'][0]['steps'][2]['transit_details']['departure_time']['text']
		headsign_second = transit_route['legs'][0]['steps'][2]['transit_details']['headsign']
		bus_number_second = transit_route['legs'][0]['steps'][2]['transit_details']['line']['short_name']
		#bus_num = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['line']['short_name']
		number_of_stops_second = transit_route['legs'][0]['steps'][2]['transit_details']['num_stops']
		arrival_stop_final = transit_route['legs'][0]['steps'][2]['transit_details']['arrival_stop']['name']
		list_with_direction = [departure_stop,bus_at_departure_stop,headsign_first,bus_number_first,number_of_stops_first,arrival_stop_transit,transit,departure_stop_transit,bus_at_transit_departure_stop,headsign_second,bus_number_second,number_of_stops_second,arrival_stop_final]

		

	else:

		departure_stop = transit_route['legs'][0]['steps'][1]['transit_details']['departure_stop']['name']
		bus_at_departure_stop = transit_route['legs'][0]['steps'][1]['transit_details']['departure_time']['text']
		headsign_first = transit_route['legs'][0]['steps'][1]['transit_details']['headsign']
		bus_number_first = transit_route['legs'][0]['steps'][1]['transit_details']['line']['short_name']
		#bus_num = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['line']['short_name']
		number_of_stops_first = transit_route['legs'][0]['steps'][1]['transit_details']['num_stops']
		arrival_stop_transit = transit_route['legs'][0]['steps'][1]['transit_details']['arrival_stop']['name']
		transit = "transit"
		departure_stop_transit = transit_route['legs'][0]['steps'][3]['transit_details']['departure_stop']['name']
		bus_at_transit_departure_stop = transit_route['legs'][0]['steps'][3]['transit_details']['departure_time']['text']
		headsign_second = transit_route['legs'][0]['steps'][3]['transit_details']['headsign']
		bus_number_second = transit_route['legs'][0]['steps'][3]['transit_details']['line']['short_name']
		#bus_num = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['line']['short_name']
		number_of_stops_second = transit_route['legs'][0]['steps'][3]['transit_details']['num_stops']
		arrival_stop_final = transit_route['legs'][0]['steps'][3]['transit_details']['arrival_stop']['name']
		list_with_direction = [departure_stop,bus_at_departure_stop,headsign_first,bus_number_first,number_of_stops_first,arrival_stop_transit,transit,departure_stop_transit,bus_at_transit_departure_stop,headsign_second,bus_number_second,number_of_stops_second,arrival_stop_final]

	return list_with_direction




	

def findroutedetails(request):
	source = request.POST['origin']
	destination = request.POST['destination']
	print(source)
	print(destination)
	# importing required libraries 
	import requests, json, pymysql

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

	# bydefault driving mode considered 

	# print the vale of x 
	#print(x['geocoded_waypoints']) 
	#print(x['routes'])
	#print(x['geocoded_waypoints']) 
	#print("-----------------------------------")
	if(len(x['routes'])!=0):
		sql_2 = """select distinct mydbservlet.stops_times.bus_number from mydbservlet.stops_times"""
		db = pymysql.connect(host="127.0.0.1", user="root", passwd="Ganesha-46", db="mydbservlet")
		cursor = db.cursor()
		cursor.execute(sql_2,)
		list_all_bus_numbers = cursor.fetchall()
		list_all_bus_numbers = list(list_all_bus_numbers)
		print("List of all Bus Numbers in Dublin",list_all_bus_numbers)
		list_with_alternate_routes = []
		list_intermediate_bus_stops_alternate_stops = []
		for i in x['routes']:
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

				list_with_direction = [total_duration, total_time,html_inst1,dist_bus_stop_walk,time_to_bus_stop_walk,html_inst2,bus_distance,bus_time,departure_stop,bus_at_departure_stop,headsign,bus_number,number_of_stops,arrival_stop,html_inst3,distance_to_dest,time_by_walk_dest]
				list_with_alternate_routes.append(list_with_direction)

				if(i['legs'][0]['steps'][1]['transit_details']['line']['short_name'].upper() in list(map(itemgetter(0),list_all_bus_numbers))):

					departure_stop ='%'+departure_stop+'%'
					arrival_stop ='%'+arrival_stop+'%'

					list_arrive_depart_stop_id=extract_correct_depart_arrival_stop_id(departure_stop,arrival_stop,bus_number,headsign)
					arrival_stop_id = list_arrive_depart_stop_id[0]
					departure_stop_id = list_arrive_depart_stop_id[1]
					result = list_arrive_depart_stop_id[2]

									
					
					number_of_stops = int(number_of_stops)
					print("Bus Number is",bus_number)
					remove_duplicates = extract_seq_numbers_bus_stops(headsign,bus_number,arrival_stop_id,departure_stop_id,number_of_stops)
					
					list_intermediate_bus_stops_alternate_stops.append(remove_duplicates)
					print("-----------------------------------------------------------------------------------------")
				else:
					pass

			else:
				
				print("Routes from google apis",i)
				list_with_direction = get_transit_details(i)
				list_with_alternate_routes.append(list_with_direction)

				departure_stop = list_with_direction[0]
				headsign_first = list_with_direction[2]
				bus_number_first = list_with_direction[3]
				number_of_stops_first = list_with_direction[4]
				arrival_stop_transit = list_with_direction[5]
				departure_stop_transit = list_with_direction[7]
				headsign_second = list_with_direction[9]
				bus_number_second = list_with_direction[10]
				number_of_stops_second = list_with_direction[11]
				arrival_stop_final = list_with_direction[12]
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

					list_arrive_depart_stop_id=extract_correct_depart_arrival_stop_id(departure_stop,arrival_stop_transit,bus_number_first,headsign_first)
					if(list_arrive_depart_stop_id!=0):
						arrival_stop_id_first = list_arrive_depart_stop_id[0]
						departure_stop_id_first = list_arrive_depart_stop_id[1]
						result = list_arrive_depart_stop_id[2]
						number_of_stops_first = int(number_of_stops_first)
						print("Bus Number first is",bus_number_first)
						remove_duplicates = extract_seq_numbers_bus_stops(headsign_first,bus_number_first,arrival_stop_id_first,departure_stop_id_first,number_of_stops_first)
						list_remove_duplicates.append(remove_duplicates)

						#---------------------TRANSIT PART SECOND LEG INFO-------------------------------------------#	
						departure_stop_transit ='%'+departure_stop_transit+'%'
						arrival_stop_final ='%'+arrival_stop_final+'%'
						list_arrive_depart_stop_id=extract_correct_depart_arrival_stop_id(departure_stop_transit,arrival_stop_final,bus_number_second,headsign_second)
						if(list_arrive_depart_stop_id!=0):

							arrival_stop_id_second = list_arrive_depart_stop_id[0]
							departure_stop_id_second = list_arrive_depart_stop_id[1]
							result = list_arrive_depart_stop_id[2]
							number_of_stops_second = int(number_of_stops_second)
							print("Bus Number second is",bus_number_second)
							remove_duplicates = extract_seq_numbers_bus_stops(headsign_second,bus_number_second,arrival_stop_id_second,departure_stop_id_second,number_of_stops_second)
							list_remove_duplicates.append(remove_duplicates)
							list_intermediate_bus_stops_alternate_stops.append(list_remove_duplicates)
						else:
							list_with_alternate_routes.pop()
					else:
						list_with_alternate_routes.pop()



					



				else:
					pass

		'''

		seq_numbers = list(seq_numbers)
		if(len(seq_numbers)>2):
			selected_seq_numbers = [0]*2
			i = 0
			if(i<len(seq_numbers) and seq_numbers[i]!=seq_numbers[i+1]):


		'''
		print("-----------------------------------------------------------------------------------------")
		print("List of intermediate_bus_stops_with individual sequence numbers",list_intermediate_bus_stops_alternate_stops)
		args={}
		result = json.dumps(result)
		args['result']=result
	
		return HttpResponse(json.dumps({'result': result, 'list_with_alternate_routes': list_with_alternate_routes}))
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
    




