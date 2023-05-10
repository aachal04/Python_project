"""
!/usr/bin/env python
 file      ssh_4950_handler.py
		   This script use to communicate with 4950 system.

 author    Glide Technology Pvt. Ltd. <www.glidemtech.com>
 version   1.0
 date      1, December, 2022

Description: Running three python processes in parallel 
			 while sharing data in between
			 return : adc parameter data (pse,pd,current,sense)
"""

import socket
from time import perf_counter, sleep
from numpy import int16
from threading import Thread 
import os
# from queue import Queue
import json
from paramiko.client import SSHClient, AutoAddPolicy
from datetime import datetime as dt
from collections import deque


# Macros
NOW = dt.now().strftime('%Y%m%d_%H%M') #.%f)[:-3]
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
fname = os.path.join(desktop, "adc_logs" + NOW + ".txt")
ADC_16BIT_RES  = 0.00015259 # ADS8584S 16-Bit ADC resolution, 159.52 uV
ADC_16_BIT_SCALE_FACTOR = 216.9/16.9 # Resistor Voltage Divider
USERNAME_4950   =   "root"
PASSWORD_4950   =   "telebyteadmin"
PORT_4950       =    22
IP_4950 = "192.168.6.38"
reading_count = 0
result = {
	"current" : [],
	"pse_cor" : [],
	"pd_cor"  : [],
	"ch4_adc" : []
}
def get_my_ip_address(remote_server="google.com"):
	"""
	Return the/a network-facing IP number for this system.
	"""
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		s.connect((remote_server, 80))
		return s.getsockname()[0]



def threading(ipAdd_4950):
	start = perf_counter()
	try:
		host_ip = get_my_ip_address(ipAdd_4950)
	except:
		host_ip = get_my_ip_address()

	print(host_ip)
	dataQueue = deque()
	flag = deque()
	try:
		server = Thread(target=run_server, args=(dataQueue,flag))
		ssh = Thread(target=ssh_init_connect_4950, args=(flag, host_ip,ipAdd_4950))
		
		server.start()
		ssh.start()
		server.join()
		ssh.join()
		
		return_data = buffer(dataQueue)
		# with open("adc_data.json","a") as file:
		#     json.dump(return_data, file)
		# print(return_data['current'])
		print(f"took {perf_counter() - start}")
		return return_data	

	except Exception as err:
		print("Caught Exception in function threading: ",err)
		return err
#--------------------------adc server-----------------------
def run_server(q,flag,conn=None):
	start = perf_counter()
	# socket.setdefaulttimeout(10)
	s = socket.socket()
	# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	port = 5899
	c = None
	s.bind(('', port))  
	s.listen(5)

	if(s.fileno() > -1):
		# print ("socket is listening")
		flag.append(True)
	timestamp = perf_counter()
	if flag.__len__() > 0:
		print("Connecting with ssh")
	try:
		c, addr = s.accept()
		print ('Got connection from', addr)
		n = 0
		err_count = 0
		while True:
			try:
				data = c.recv(1).hex()
				if data != "":
					q.append(data)
					n += 1
				# if perf_counter() - timestamp > 2.0:
				# 	print(data, n-8)
				# 	timestamp = perf_counter()
					# pass
				if not data:
					break
			except Exception as e:
				print("Caught Exception in function run_server in while loop:	",e)
				sleep(.5)
				err_count += 1
				if err_count > 3:
					break
		q.append(None)
		print(f" received {n-8} bytes ,took {perf_counter()-start:.4} seconds")
	except Exception as err:	
		print("Caught Exception in function run_server:	",err)
		q.put(None)
		if c is None:
			return
	c.close()
	return

#--------------------------adc data-----------------------
def calc(reading):
	global result
	#print(reading[2])
	if "ch4_adc" not in result.keys():
		result["ch4_adc"] = []
	if "current" not in result.keys():
		result["current"] = []
	if "pse_cor" not in result.keys():
		result["pse_cor"] = []
	if "pd_cor" not in result.keys():
		result["pd_cor"] = []
	try:
		current = (reading[2] * ADC_16BIT_RES)#+0.001#0.007
		pse_volt = ( reading[0] * ADC_16BIT_RES * ADC_16_BIT_SCALE_FACTOR) # + (0.170 * current)
		pd_volt = ( reading[1] * ADC_16BIT_RES * ADC_16_BIT_SCALE_FACTOR) # - (0.170 * current)
		result["ch4_adc"].append(r( reading[3] * ADC_16BIT_RES * ADC_16_BIT_SCALE_FACTOR))
		pse_offset = 0.173 * current
		pd_offset = (-1) * 0.205 * current
		result["current"].append(r(current))
		# print("append data :",result["current"])
		result["pse_cor"].append(r((1.0129 * pse_volt) - 0.0311 + pse_offset))
		result["pd_cor"].append(r((0.9988 * pd_volt) + 0.0754  + pd_offset ))
	# 	return result
	except Exception as err:	
		print("Caught Exception in function calc:	",err)
		# q.put(None)
		# if c is None:
		# 	return

# function to round the reading upto 3 decimal points
r = lambda n : round(n,5)
# function for unsigned hex_string to signed number conversion        
signed = lambda hex_string : int16(int(hex_string, 16))

# Process the hex string to extract hex values 
def getReadings(data):
	if type(data) != list:
		data = data.split()
	vals = []
	for i in range(0,len(data),2):
		if type(data[i]) != str:
			continue
		string_val = data[i] + data[i+1]
		# will not work if the list is not even in lenght
		vals.append(signed(string_val))
	calc(vals)

#----------------ssh connection-------------
def ssh_init_connect_4950(flag, host_ip,ipAdd_4950):
	while True:
		if flag.__len__() == 0:
			continue
		
		host = SSHClient()
		host.load_system_host_keys()
		host.set_missing_host_key_policy(AutoAddPolicy())
		host.connect(hostname=ipAdd_4950,
				username=USERNAME_4950,
				password=PASSWORD_4950,
				port=PORT_4950)
		print("ssh connect")
		host_ip = str(host_ip)
		stdin, stdout, stderr = host.exec_command(f"Set log 2 {host_ip} 5899", get_pty=True)

		flag.append(False)
		st = stdout.readlines()
		print(st)
		host.close()
		return

def buffer(dataQueue):
	global result
	result["current"].clear()
	result["pse_cor"].clear()
	result["pd_cor"].clear()
	result["ch4_adc"].clear()
	start = perf_counter()
	
	HEX_STRING = []
	data_str = "" 
	count = 0
	# validation_str = ""
	while True:
		try:
			if dataQueue.__len__() == 0:
				continue
			msg = dataQueue.popleft()
			if msg is None:
				break
			if count == 4:
				#print(f"amount:	{data_str}")
				pass
			if count > 7:
				HEX_STRING.append(msg)
				if len(HEX_STRING)%8 == 0:
					getReadings(HEX_STRING)
					HEX_STRING = []
			elif count < 4:
				data_str += msg
			else:
				if msg == "00":
					# validation_str += "%%%%%%%%%%%%"
					pass
				else:
					print("Failing... ")
			if count == 7:
				#print(validation_str)
				pass
			count += 1
		except Exception as err:
			logger(f"Caught Exception while processing log data: {err}")
			sleep(0.5)
	print(f"Done, Processed: {(count-8)} bytes, Got :{(count - 8)/8}Samples ,took {perf_counter()-start:.4} seconds")
	return result

def logger(fname, msg):
	t = dt.now().strftime("%D_%T.%f")[:-4]
	with open(fname,"a") as f:
		f.write(t + "	" + msg + "\n")
	f.close()

if __name__ == "__main__":
	threading(IP_4950)
