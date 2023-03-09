# Import socket module
from socket import *

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

# Fill in start

# define local host & port to connect to
HOST = "127.0.0.1"
PORT = 8888

# start socket server
serverSocket.bind((HOST, PORT))
serverSocket.listen()

# Fill in end 

# Server should be up and running and listening to the incoming connections
while True:
	print('Ready to serve...')
	
	# Set up a new connection from the client
	client_sock, client_addr = serverSocket.accept() # lots of documentation says this; dont understand myself but keeping for now
	
	# If an exception occurs during the execution of try clause
	# the rest of the clause is skipped
	# If the exception type matches the word after except
	# the except clause is executed
	try:
		# Receives the request message (of max size 4096) from the client (& decodes into string)
		message = client_sock.recv(4096).decode() # Custom Code

		# message looks like 
		# 	GET /localhost:6789/helloworld.html HTTP/1.1
		# 	...
		request = message.split()[1]			# /localhost:6789/helloworld.html

		destination = request.split('/')[1] 	# localhost:6789
		dest_addr = destination.split(':')[0]	# localhost
		dest_port = destination.split(':')[1]	# 6789

		# Connect to the destination server
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.connect((dest_addr, dest_port))
 
		# Send the content of the requested file to destination server
		s.sendall(request)

		# Receive destination server response and send it to client
		while True:
			# receive data from web server
			data = s.recv(4096)

			# Keep sending until no more data
			if (len(data) > 0):
				client_sock.send(data) # send to browser/client
			else:
				break
		
		# Close the client connection socket
		client_sock.close()

	except IOError:
		# Send HTTP response message for file not found
		# Fill in start
		client_sock.send("404 Not Found".encode())
		# Fill in end
        
		# Close the client connection socket
		# Fill in start
		client_sock.close()
		# Fill in end

serverSocket.close()  