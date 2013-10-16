#! /usr/bin/env python

import logging
import httplib2
import json
import sys
from math import *
import datetime
from time import sleep
from sets import Set

logging.getLogger("scapy").setLevel(1)

from scapy.all import *
from time import *

key = "6f7ef1159eb53bba3ebd9e24969aa216d0dec8ce85e483021c14da8546985653"
geoipUrl = "http://api.ipinfodb.com/v3/ip-city/?key=" + key +"&format=json"

def traceroute(ip):
	myTtl = 1
	cantRTTs = 0
	muestras = Set([])
	R = 0
	RTT1 = 0
	RTT2 = None
	std_dev = 0
	host = IP()
	resp, content = httplib2.Http(timeout=2).request(geoipUrl)
	decoded = json.loads(content)
	print str(myTtl) +" "+host.src + "  "+ decoded["cityName"] + ", "+decoded["regionName"]+", "+decoded["countryName"] + "   Lat="+str(decoded["latitude"])+ " Long="+str(decoded["longitude"])

	distancias = (host.src,decoded["cityName"] + " "+decoded["countryName"],decoded["latitude"],decoded["longitude"]),

	while True and myTtl < 21:
		ipPacket = IP(dst=ip, ttl=myTtl)
		t1=time()
		ans = sr(ipPacket/ICMP(), timeout=5, verbose=0)
		
		if(len(ans[0]) == 0):
			print str(myTtl)+" * no response *"
			myTtl = myTtl + 1
			RTT1 = None
			continue
		t2=time()
		timeStr = str((t2-t1)*1000) + " ms"
		RTT2 = t2-t1
		if not (RTT1==None):
			cantRTTs = cantRTTs + 1
			muestras.add(RTT2-RTT1)
		
		s1 = sum(x for x in muestras)
		s2 = sum(x*x for x in muestras)
		R = s1/cantRTTs
		if(cantRTTs>1):
			std_dev = math.sqrt((cantRTTs * s2 - s1 * s1)/(cantRTTs * (cantRTTs - 1)))
		RTT1 = RTT2

		ipAns = ans[0][0][1]
		#print str(myTtl) +" "+ipAns.src
		try:
			resp, content = httplib2.Http(timeout=2).request(geoipUrl+"&ip="+ipAns.src)
			#print content
			decoded = json.loads(content)
			print str(myTtl) +" "+ipAns.src + "  "+ decoded["cityName"] + ", "+decoded["regionName"]+", "+decoded["countryName"] + "   Lat="+str(decoded["latitude"])+ " Long="+str(decoded["longitude"]) + "   Time="+timeStr
			if decoded["countryName"] != "-":
				distancias += (ipAns.src,decoded["cityName"] + " "+decoded["countryName"] ,decoded["latitude"],decoded["longitude"]),
		except:
			print str(myTtl) +" "+ipAns.src+ "   Time="+timeStr

		
		if (ans[0][0][0].dst == ipAns.src):
			break;

		myTtl = myTtl + 1

	
	#print distancias
	distanciaTotal = 0
	print "\n"
	for i in range(len(distancias)-1):
		aux = haversine(distancias[i][2], distancias[i+1][2], distancias[i][3], distancias[i+1][3]) 
		print "Desde " + distancias[i][1] + " Hasta " + distancias[i+1][1] + " " + str(aux)
		distanciaTotal += aux

	print "\nLa distancia total recorrida hasta llegar al enlace final fue de: " + str(distanciaTotal)


def haversine(lat1, lat2, lon1, lon2):
	lat1, lat2, lon1, lon2 = float(lat1), float(lat2), float(lon1), float(lon2)
	lat1, lat2, lon1, lon2 = radians(lat1), radians(lat2), radians(lon1), radians(lon2)
	res = 2*6378.14 * asin(sqrt(sin((lat1-lat2)/2)**2 + cos(lat1) * cos(lat2) * sin((lon1-lon2)/2)**2))
	return res

	#http://en.wikipedia.org/wiki/Haversine_formula


def batchTrace():
	f = open("IPs", 'r')
	sys.stdout = open("resultados", 'w')
	temp = f.read().splitlines()
	for lines in temp:
		print("trace de la ip: " + lines + "\n")
		traceroute(lines)
		print("\n\n\n")
	f.close()
	sys.stdout = sys.__stdout__

	#http://www.projecthoneypot.org
	



if __name__ == "__main__":
    interact(mydict=globals(), mybanner="TRACEROUTE")
