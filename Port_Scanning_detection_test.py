import subprocess
import paramiko
import time
host = "jharri32"

k = paramiko.RSAKey.from_private_key_file("C:\Users\juwan\Documents\key.pem") #gets the private key for ssh connection  
scan=0

ssh2=paramiko.SSHClient()
ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh2.connect(hostname = "jharri32", username = "ta", pkey = k) #starts the ssh connnection
shells=ssh2.invoke_shell() #allows for more than one command to be enter for a ssh session 
shells.send("cd /usr/local/bro/spool/bro \n") 
time.sleep(1) #wait for a second
data=shells.recv(9999) #recive that data 

p1 = subprocess.Popen(['nmap','-sT',host], stdout=subprocess.PIPE) #start the TCP connect scan 
# Run the command
output = p1.communicate()[0] #stores teh output of the TCP connect scans
print output
shells.send("cat notice.log\n")  #opens notice.log file 
time.sleep(1) #wait for a second
data=shells.recv(9999) #recive that data 
print data
if "Scan::Port_Scan" in data: #looks to see of bro has found a port scan
	print "TCP connect scan detected"
	scan+=1
	
time.sleep(10) #waits ten seconds
p1 = subprocess.Popen(['nmap','-sS','-e','eth4','-S','192.168.137.30',host], stdout=subprocess.PIPE) #starts the SYN scan with a spoof IP address
# Run the command
time.sleep(1)
output = p1.communicate()[0]
print output
time.sleep(1) #waits a second
shells.send("cat notice.log\n") #opens notice.log file 
time.sleep(1) #wait for a second
data=shells.recv(9999) #recive that data 
print data
if "192.168.137.30" in data: #looks for the spoof ip address 
	print "SYN Stealth scan detected"
	scan+=1
	
time.sleep(10)
p1 = subprocess.Popen(['nmap','-sU','-e','eth4','-S','192.168.137.35',host], stdout=subprocess.PIPE) #starts the UPD scan
# Run the command
time.sleep(1)
output = p1.communicate()[0]
print output
shells.send("cat weird.log\n") #opens the weird.log file
time.sleep(1) #wait for a second
data=shells.recv(9999) #recive that data 
print data
if "192.168.137.35" in data:
	print " UDP scan detected"
	scan+=1

time.sleep(10)
p1 = subprocess.Popen(['nmap','-sO','-e','eth4','-S','192.168.137.40',host], stdout=subprocess.PIPE) #starts the IP protocol scan
# Run the command
time.sleep(1)
output = p1.communicate()[0]
print output
shells.send("cat weird.log\n") 
time.sleep(1) #wait for a second
data=shells.recv(9999) #recive that data 
print data
if "unknown_protocol" in data:
	print "IP Protocol scan detected"
	scan+=1
print str(scan)+"/4 scan detected"