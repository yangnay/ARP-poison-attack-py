伪装为网关，抓包保存。 功能：伪装为网关，抓包保存。 使用scapy库

此代码是定向欺骗，广播欺骗可以自己修改代码。

必须在Linux下以root身份运行。

运行代码前记得设置IP转发功能：sysctl net.ipv4.ip_forward=1


例： sudo python arper.py 
WARNING: No route found for IPv6 destination :: (no default route?) 
[] Setting up eno1 30:0e:d5:c7:33:b7 
[]Gateway 10.63.63.250 is at 30:0e:d5:c7:33:b7 
[]Target_ip 10.63.1.45 is at 00:e0:b4:16:18:a3 
[] Beginning the arp poison.[CTRL -C to stop.] 
[]Starting sniffer for 1000 packets 
[] Restoring target ... 
已杀死
