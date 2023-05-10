"""
22nd November' 2022

python tcp ip server

"""
# 


import socket
from time import perf_counter, sleep
from sys import exit
# server function 

def run_server(timeout=15.0,q=None,conn=None):
	socket.setdefaulttimeout(timeout)
	s = socket.socket()
	# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# s.settimeout(2)
	port = 35006
	s.bind(('', port))
	# s.setblocking(0)
	# s.setdefaulttimeout(timeout)
	# above is equivalent to directly setting default timeout to the socket module
	s.listen(5)
	if(s.fileno() > -1):
		# print("created")
		print ("socket is listening") 
	try:
		c = None
		c, addr = s.accept()
		# a = input("enter to exit")
		start = perf_counter()
		print ('Got connection from', addr)    
		# hex string to store the data
		HEX_STRING = ""
		n = 0

		t_flag = c.recv(32)
		while True:
			try:
				data = c.recv(1).hex()
				if data != "":
					if conn is not None:
						conn.send(data)
					if q is not None:
						q.put(data)
					n += 1
				if n%100 == 0:
					print(data, n)
					# sleep(.7)
				if not data:
					q.put(None)
					break
			except Exception as e:
				print(e)

		print("received:	",n)
		print(f"it took {perf_counter()-start:.4} seconds")
	except Exception as e:
		if type(e) is TimeoutError:
			print("Client is not available")
		else:
			print(e.with_traceback(e.__traceback__))
	finally:
		if c:
			c.close()


if __name__ == "__main__":
	run_server()
