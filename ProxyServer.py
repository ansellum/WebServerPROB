# Import socket module
from socket import *

def fetch_from_cache(filename):
	try:
		# Check if file is in cache
		f = open('cache' + filename)
		content = f.read()
		f.close()
		# If we have it, let's send it
		print("Found " + filename + " in cache")
		return content.encode()
	except IOError:
		print(filename + " not in cache")
		return None

def save_in_cache(filename, content):
	print("Saving " + filename + " in cache")
	cached_file = open('cache' + filename, 'wb')
	cached_file.write(content)
	cached_file.close()

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

		# This is where the cache implementation will take place
		# check cache for file before sending request to destination server
		requested_file = fetch_from_cache(filename)

		# file is not in cache, send request to destination server
		if requested_file == None:

			requested_file = b''

			# Connect to the destination server
			s = socket(AF_INET, SOCK_STREAM) 
			s.connect((dest_addr, dest_port))
 
			# Send the content of the requested file to destination server
			# Proxy request should look like this: GET /<filename> HTTP/1.1\r\nHost:localhost:6789\r\n\r\n
			proxy_request = "GET /" + filename + " HTTP/1.1\r\nHost:" + destination + "\r\n\r\n"
			s.sendall(proxy_request.encode())

			# Receive destination server response and send it to client
			while True:
				# receive data from web server
				data = s.recv(4096)

				# Keep sending until no more data
				if len(data) > 0:
					requested_file += data
				else:
					save_in_cache(filename, requested_file)
					break

		# Send the HTTP response header line to the connection socket
		client_sock.send("HTTP/1.1 200 OK\r\n".encode())

		# Send the content of the requested file to the connection socket
		client_sock.sendall(requested_file)
		
		# Close the client connection socket
		client_sock.close()

	except IOError:
		# Send HTTP response message for file not found
		client_sock.send("HTTP/1.1 404 Not Found".encode())
        
		# Close the client connection socket
		client_sock.close()

serverSocket.close()  