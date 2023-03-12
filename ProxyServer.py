# Import socket module
from socket import *

def fetch_from_cache(filename):
	try:
		# Check if file is in cache
		cache_name = filename + '.cache'
		f = open(cache_name.replace('/', '~'), 'rb')
		content = f.read()
		f.close()
		# If we have it, let's send it
		print("Found " + filename + " in cache")
		return content
	except IOError:
		print(filename + " not in cache")
		return None

def save_in_cache(filename, content):
	print("Saving " + filename + " in cache")
	cache_name = filename + '.cache'
	cached_file = open(cache_name.replace('/', '~'), 'wb')
	cached_file.write(content)
	cached_file.close()

# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# define local host & port to connect to
HOST = "0.0.0.0"
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
		# Receives the request message
		message = client_sock.recv(4096).decode()

		# Comment examples: localhost:6789/helloworld.html	|	starmen.net/mother3/screenshots/

		# Parse necessary information
		# message = GET /localhost:6789/helloworld.html HTTP/1.1 ...
		client_request = message.split()[1].split('/')		# ['', 'localhost:6789', 'helloworld.html']	|	['', 'starmen.net', 'mother3', 'screenshots', '']

		destination = client_request[1] 					# localhost:6789	|	starmen.net
		filename = '/' + '/'.join(client_request[2:]) 		# /helloworld.html	|	/mother3/screenshots/

		dest_addr 	= destination.split(':')[0]				# localhost			|	starmen.net
		if ':' in destination:
			dest_port = int(destination.split(':')[1])		# 6789
		else:
			dest_port = 80									# 80

		# check cache for file before sending request to destination server
		requested_file = fetch_from_cache(filename) # encode cache filename 

		# file is not in cache, send request to destination server
		if requested_file == None:
			print("Connecting to web server")

			requested_file = b''

			# Connect to the destination server
			dest_sock = socket(AF_INET, SOCK_STREAM) 
			dest_sock.connect((dest_addr, dest_port))
 
			# Send the content of the requested file to destination server
			proxy_request = "GET " + filename + " HTTP/1.1\r\nHost: " + destination + "\r\nConnection: close\r\n\r\n"

			dest_sock.sendall(proxy_request.encode())

			# Receive destination server response and send it to client
			while True:
				# receive data from web server
				data = dest_sock.recv(4096)

				# Keep sending until no more data
				if len(data) == 0:
					save_in_cache(filename, requested_file)
					break

				requested_file += data

		# Send the HTTP response header line to the connection socket
		client_sock.send("HTTP/1.1 200 OK\r\n\r\n".encode())

		# Send the content of the requested file to the connection socket
		client_sock.sendall(requested_file)
		
		# Close the client connection socket
		client_sock.close()

	except (IOError, IndexError):
		# Send HTTP response message for file not found
		client_sock.send("HTTP/1.1 404 Not Found\r\n".encode())
        
		# Close the client connection socket
		client_sock.close()

serverSocket.close()  