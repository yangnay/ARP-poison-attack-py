 功能：伪装为网关，抓包保存。 
 
 使用scapy库

此代码是定向欺骗，广播欺骗可以自己修改代码。

必须在Linux下以root身份运行。

运行代码前记得设置IP转发功能：sysctl net.ipv4.ip_forward=1


sudo python arper.py 目标ip 网关ip

例：


sudo python arper.py 10.63.1.45 10.63.63.250
