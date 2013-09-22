#! /usr/bin/env python
from math import log

f = open('sniffer-home.txt', 'r')

ipsPreguntan = {}
ipsResponden = {}
ipsPorLasQueSePregunta = {}
numeroPreguntas = 0
numeroRespuestas = 0
while 1:
	line1 = f.readline()
	if not line1:
		break
	paquete = line1.split()
	if paquete[3] == "who-has":
		ipsPreguntan[paquete[1]] = ipsPreguntan.get(paquete[1], 0.0) + 1.0
		ipsPorLasQueSePregunta[paquete[2]] = ipsPorLasQueSePregunta.get(paquete[2], 0.0) + 1.0
		numeroPreguntas = numeroPreguntas + 1
	if paquete[3] == "is-at":
		ipsResponden[paquete[1]] = ipsResponden.get(paquete[1], 0.0) + 1.0
		numeroRespuestas = numeroRespuestas + 1

print "IPs Preguntan"
H = 0;
for ip in ipsPreguntan.keys():
	num = ipsPreguntan.get(ip)
	p = num/numeroPreguntas
	I = log(p,2)*-1
	H = H + p*log(p,2)
	print "ip: "+ip+"  total: "+str(num)+"  p: "+str(p)+"  I:"+str(I)
print "H = "+str(H*-1)
H = 0
print "IPs Responden"
for ip in ipsResponden.keys():
	num = ipsResponden.get(ip)
	p = num/numeroRespuestas
	I = log(p,2)*-1
	H = H + p*log(p,2)
	print "ip: "+ip+"  total: "+str(num)+"  p: "+str(p)+"  I:"+str(I)
print "H = "+str(H*-1)
H = 0
print "IPs por las que se pregunta"
for ip in ipsPorLasQueSePregunta.keys():
	num = ipsPorLasQueSePregunta.get(ip)
	p = num/numeroPreguntas
	I = log(p,2)*-1
	H = H + p*log(p,2)
	print "ip: "+ip+"  total: "+str(num)+"  p: "+str(p)+"  I:"+str(I)
print "H = "+str(H*-1)
