# Import socket module
from socket import *
	
# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# define local host & port to connect to
HOST = "127.0.0.1"
PORT = 8888
# start socket server
serverSocket.bind((HOST, PORT))
serverSocket.listen()

# Server should be up and running and listening to the incoming connections
while True:
	print('Ready to serve...')
	
	# Set up a new connection from the client
	client_sock, client_addr = serverSocket.accept()
	
	try:
		# Receives the request message (of max size 4096) from the client (& decodes into string)
		message = client_sock.recv(4096).decode() # Custom Code

		# message looks like 
		# 	GET /localhost:6789/helloworld.html HTTP/1.1
		# 	Host: localhost:8888
		#	...
		client_request = message.split()[1]				# /localhost:6789/helloworld.html

		destination = client_request.split('/')[1] 		# localhost:6789
		filename 	= client_request.split('/')[2] 		# helloworld.html

		dest_addr 	= destination.split(':')[0]			# localhost
		dest_port 	= int(destination.split(':')[1])	# 6789

		# Connect to the destination server
		s = socket(AF_INET, SOCK_STREAM) 
		s.connect((dest_addr, dest_port))
 
		# Send the content of the requested file to destination server
		# Proxy request should look like this: GET /<filename> HTTP/1.1\r\nHost:localhost:6789\r\n\r\n
		proxy_request = "GET /" + filename + " HTTP/1.1\r\nHost:" + destination + "\r\n\r\n"
		s.sendall(proxy_request.encode())

		# This is where the cache implementation will take place. Most likely will replace entire while loop
		# Receive destination server response and send it to client
		while True:
			# receive data from web server
			data = s.recv(4096)

			# Keep sending until no more data
			if len(data) > 0:
				client_sock.sendall(data) # send to client
			else:
				break
		
		# Close the client connection socket
		client_sock.close()

	except IOError:
		# Send HTTP response message for file not found
		client_sock.send("HTTP/1.1 404 Not Found".encode())
        
		# Close the client connection socket
		client_sock.close()

serverSocket.close()  