#!/usr/bin/env python
# file      ssh_4950_handler.py
#           This script use to communicate with 4950 system.
#
# author    Glide Technology Pvt. Ltd. <www.glidemtech.com>
# version   1.0
# date      15, July, 2022

# dependencies
from paramiko.client import SSHClient, AutoAddPolicy
import time
import paramiko
import os
from numpy import int16

# constants

IP_4950         =   "192.168.40.141"
USERNAME_4950   =   "root"
PASSWORD_4950   =   "telebyteadmin"
PORT_4950       =    22

#----ssh connection----#
def ssh_init_connect_4950(IPaddress,cmd):
    log_data = []
    return_data = None
    print("4950 SSH connection....")
    try:
        host = SSHClient()
        host.load_system_host_keys()
        host.set_missing_host_key_policy(AutoAddPolicy())

        host.connect(hostname=IPaddress,
                    username=USERNAME_4950,
                    password=PASSWORD_4950,
                    port=PORT_4950)

        stdin, stdout, stderr = host.exec_command(cmd, get_pty=True)
        if "dcr" in cmd :
            for line in stdout:
                  print(line)
            for line in iter(stdout.readline, ""):
                # print("4950: ",line, end="")
                if "ACCEPTED" in line:
                    #print("Accepted")
                    return_data = cmd
                    break;
                elif "FAILED" in line.upper() or "Invalid" in line or "ERROR" in line.upper():
                    return_data = "Failed to Set DCR..."
                    print("4950 : ",return_data)
                    
        if "power" in cmd:
            for line in iter(stdout.readline, ""):
                #print("4950: ",line, end="")
                if "Voltage PSE" in line:
                    pse_line= line.split(":")
                    pse_volt_4950 = pse_line[1].split("V")
                    pse_volt_4950 = float(pse_volt_4950[0])
                    # print("pse_volt : ",pse_volt_4950)
                if "Voltage PD" in line:
                    pd_line= line.split(":")
                    pd_volt_4950 = pd_line[1].split("V")
                    pd_volt_4950 = float(pd_volt_4950[0])
                    # print("pd_volt : ",pd_volt_4950)
                if "Loop Current" in line:
                    curr_line= line.split(":")
                    curr_4950 = curr_line[1].split("A")
                    curr_4950 = float(curr_4950[0])
                    # print("curr_4950 : ",curr_4950)
                if "Voltage Sense" in line:
                    sense_line= line.split(":")
                    sense_4950 = sense_line[1].split("V")
                    sense_4950 = float(sense_4950[0])
                    # print("sense_4950 : ",sense_4950)
                if "ohm" in line:
                    #print("Accepted")
                    return_data = [pse_volt_4950,pd_volt_4950,curr_4950,sense_4950]
                    break;
                elif "FAILED" in line.upper() or "Invalid" in line or "ERROR" in line.upper():
                    return_data = "Failed to Show Power Details"
                    # print("4950 : ", return_data)

        if "sense" in cmd:
            for line in iter(stdout.readline, ""):
                if "ACCEPTED" in line:
                    #print("Accepted")
                    return_data = cmd
                    break;
                elif "FAILED" in line.upper() or "Invalid" in line or "ERROR" in line.upper():
                    return_data = "Failed to Set sense..."
                    # print("4950 : ",return_data)
                    
        if "post" in cmd:
            for line in iter(stdout.readline, ""):
                if "ACCEPTED" in line:
                    #print("Accepted")
                    return_data = cmd
                    
                elif "FAILED" in line.upper() or "Invalid" in line or "ERROR" in line.upper():
                    return_data = "Failed to Set post..."
                    # print("4950 : ",return_data)

        if "length" in cmd:
            for line in iter(stdout.readline, ""):
                print(line)
                if "ACCEPTED" in line:
                    #print("Accepted")
                    return_data = cmd
                    
                elif "FAILED" in line.upper() or "Invalid" in line or "ERROR" in line.upper():
                    return_data = "Failed to Set length..."
                    # print("4950 : ",return_data)
        if "inj" in cmd:
            for line in iter(stdout.readline, ""):
                if "ACCEPTED" in line:
                    #print("Accepted")
                    return_data = cmd
                    
                elif "FAILED" in line.upper() or "Invalid" in line or "ERROR" in line.upper():
                    return_data = "Failed to Set inj..."
                    # print("4950 : ",return_data)

        if "log" in cmd:
            for line in iter(stdout.readline, ""):                
                log_data += [line]
                # print(line)
                if "ACCEPTED" in line:
                    #print("Accepted")
                    return_data = log_data[2].split()
                    
                elif "FAILED" in line.upper() or "Invalid" in line or "ERROR" in line.upper():
                    return_data = "Failed to Set log..."
                    # print("4950 : ",return_data) 
        if "awgn" in cmd:
            for line in iter(stdout.readline, ""):
                if "FINISHED" in line or "ACCEPTED" in line:
                    #print("Accepted")
                    return_data = cmd
                    
                elif "FAILED" in line.upper() or "Invalid" in line or "ERROR" in line.upper():
                    return_data = "Failed to Set awgn..."
                    # print("4950 : ",return_data) 

        if "pcs" in cmd:
            for line in iter(stdout.readline, ""):
                if "FINISHED" in line or "ACCEPTED" in line:
                    #print("Accepted")
                    return_data = cmd
                    
                elif "FAILED" in line.upper() or "Invalid" in line or "ERROR" in line.upper():
                    return_data = "Failed to Set pcs..."
                    # print("4950 : ",return_data) 
        if "pwrpol" in cmd:
            for line in iter(stdout.readline, ""):
                if "FINISHED" in line or "ACCEPTED" in line:
                    #print("Accepted")
                    return_data = cmd
                    
                elif "FAILED" in line.upper() or "Invalid" in line or "ERROR" in line.upper():
                    return_data = "Failed to Set pwrpol..."
                    # print("4950 : ",return_data)
        if "probe" in cmd:
            for line in iter(stdout.readline, ""):
                if "FINISHED" in line or "ACCEPTED" in line:
                    # print("Accepted")
                    return_data = "Set probe"
                    
                elif "FAILED" in line.upper() or "Invalid" in line or "ERROR" in line.upper():
                    return_data = "Failed to Set probe..."
                    # print("4950 : ",return_data)
                 
        host.close()
        return return_data
    except Exception as e:
        print("4950 Exception occurred during ssh connect: {}".format(repr(e)))
        return repr(e)

# ssh_init_connect_4950(IP_4950,"./usb-prog/set probe b 0 2")