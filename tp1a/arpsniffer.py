#!/usr/bin/env python
from scapy.all import ARP, sniff

ARP_REQUEST = 1
ARP_REPLY = 2

def packet_logger(p):
    if ARP in p and p[ARP].op in (ARP_REQUEST, ARP_REPLY):
        line = p.sprintf("%ARP.hwsrc% %ARP.psrc% %ARP.pdst% %ARP.op%")
        f.write(line)
        f.write('\n')
        return line

f = open('sniffer.txt', 'w')
sniff(prn=packet_logger, filter="arp", store=0)
