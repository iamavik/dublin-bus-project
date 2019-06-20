from django.shortcuts import render
from django.http import HttpResponse
import pymysql,json


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
	url ='https://maps.googleapis.com/maps/api/directions/json?'

	#https://maps.googleapis.com/maps/api/directions/json?alternatives=true&origin=bieberstrasse,+dusseldorf&destination=norf,+neuss&sensor=false&mode=transit&departure_time=1399399424&key=AIzaSyBi-bH5_sngxNibrgygRZDhmAv2fK5hzus
	#API to get alternate routes
	#https://maps.googleapis.com/maps/api/directions/json?alternatives=true&origin=universitycollegedublin&destination=templebar,dublin&sensor=false&mode=transit&key=AIzaSyBi-bH5_sngxNibrgygRZDhmAv2fK5hzus
	# Get method of requests module 
	# return response object 
	r = requests.get(url + 'origin=' + origin +'&destination=' + dest +'&mode='+"transit"+'&key=' + api_key) 

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
		total_duration = x['routes'][0]['legs'][0]['duration']['text']
		#print("-----------------------------------")
		total_time = x['routes'][0]['legs'][0]['distance']['text']
		html_inst1 = x['routes'][0]['legs'][0]['steps'][0]['html_instructions']
		dist_bus_stop_walk = x['routes'][0]['legs'][0]['steps'][0]['distance']['text']
		time_to_bus_stop_walk = x['routes'][0]['legs'][0]['steps'][0]['duration']['text']
		html_inst2 = x['routes'][0]['legs'][0]['steps'][1]['html_instructions']
		bus_distance = x['routes'][0]['legs'][0]['steps'][1]['distance']['text']
		bus_time = x['routes'][0]['legs'][0]['steps'][1]['duration']['text']
		departure_stop = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['departure_stop']['name']
		#dept_stop = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['departure_stop']['name']
		bus_at_departure_stop = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['departure_time']['text']
		headsign = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['headsign']
		bus_number = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['line']['short_name']
		#bus_num = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['line']['short_name']
		number_of_stops = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['num_stops']
		arrival_stop = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['arrival_stop']['name']
		#arr_stop = x['routes'][0]['legs'][0]['steps'][1]['transit_details']['arrival_stop']['name']
		html_inst3 = x['routes'][0]['legs'][0]['steps'][2]['html_instructions']
		distance_to_dest = x['routes'][0]['legs'][0]['steps'][2]['distance']['text']
		time_by_walk_dest = x['routes'][0]['legs'][0]['steps'][2]['duration']['text']

		list_with_direction = [total_duration, total_time,html_inst1,dist_bus_stop_walk,time_to_bus_stop_walk,html_inst2,bus_distance,bus_time,departure_stop,bus_at_departure_stop,headsign,bus_number,number_of_stops,arrival_stop,html_inst3,distance_to_dest,time_by_walk_dest]
		
		departure_stop ='%'+departure_stop+'%'
		arrival_stop ='%'+arrival_stop+'%'
		sql = """select ﻿stop_lat,stop_lon,STOP_ID_LAST_4,stop_name from mydbservlet.stops_2ttest_bus_stops where stop_name LIKE %s or stop_name LIKE %s""" 
		db = pymysql.connect(host="127.0.0.1", user="root", passwd="Ganesha-46", db="mydbservlet")
		cursor = db.cursor()
		cursor.execute(sql,(departure_stop,arrival_stop,))
		result = cursor.fetchall()
		result = json.dumps(result)
		args={}
		args['result']=result
		print(result)
		
		return HttpResponse(json.dumps({'result': result, 'list_with_direction': list_with_direction}))
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
	print(weather_data)
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
    


