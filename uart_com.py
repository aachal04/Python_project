import time
import re
import serial
from time import sleep
ser = serial.Serial("/dev/ttyACM0", 9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)       
ser.write(str.encode('VERSION\r\n'))
received_data = ser.read()              #read serial port
sleep(0.03)
data_left = ser.inWaiting()             #check for remaining byte
received_data += ser.read(data_left)
print (received_data)                   #print received data
result = re.findall(r"[-+]?\d*\.\d+|\d+[g]$", received_data.decode("utf-8"))
print(' '.join(map(str, result)))
# sl_data = slice(17,25)
# result = received_data[sl_data]
# a = result.strip() 
# print(a)