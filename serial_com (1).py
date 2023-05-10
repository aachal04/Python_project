import time
import re
import serial 
import flask
from time import sleep
from flask import Flask, jsonify


def serial_read_write(command):
    try:
        # Open a serial connection to the device
        ser = serial.Serial("/dev/ttyACM0", 9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
    
        # Send a command to the device to request the version number
        ser.write(str.encode(command))
        # Read the response from the device
        received_data = ser.read()
        sleep(0.03)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        print(received_data)
        return received_data
    except Exception as exp:
        print("Exception in code at serial_read_write() function!! : ",exp)
    
# Creates the flask instance    
app = Flask(__name__)

# Initialize a list to store the data received from the device
get_data = [{"version": ""}]

# Define a route for getting the version number from the device
@app.route('/4950/version', methods=['GET'])
def get():
    try:
        # Extract the version number from the received data using a regular expression
        res1 = serial_read_write('VERSION\n\r')
        str1 = "Invalid"
        res = bytes(str1,'utf-8')
        if res in res1:
            print("Give valid command!!")
            return "Invalid Command"
        else:
            result = re.findall(r"[-+]?\d*\.\d+[a-z]?|\d+[a-z]", res1.decode("utf-8"))
            print(' '.join(map(str, result)))
            # Store the version number in the get_data list
            get_data[0]['version'] = result

        # Return the get_data list as a JSON response
        return jsonify({'4950': get_data})
    except Exception as exp:
        print("Exception in code at URI /4950/version in get() function!! : ",exp)


# Define a list to store the data that can be updated
data = [{"DCR": "50"}]

# Define a route for updating the DCR value on the device
@app.route('/4950/dcr/<string:put_data>', methods=['PUT'])
def put(put_data):
    try:
        res2 = serial_read_write('R' + str(put_data) + '\r\n')
        str1 = "Invalid"
        res1 = bytes(str1,'utf-8')
        if res1 in res2:
            print("Give valid command!!")
            return "Invalid Command"
        else:
            # Extract the updated DCR value from the received data using a regular expression
            result = re.findall(r"[-+]?\d*\.\d+|\d+", res2.decode("utf-8"))
            print(' '.join(map(str, result)))
            # Store the updated DCR value in the data list
            data[0]['DCR'] = result

        # Return the data list as a JSON response
        return jsonify({'4950': data})
    except Exception as exp:
        print("Exception in code at URI /4950/dcr/<string:put_data> in  put() function!! : ",exp)

if __name__ == "__main__":
    app.run(debug=True)
