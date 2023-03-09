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
	connectionSocket, addr = serverSocket.accept() # lots of documentation says this; dont understand myself but keeping for now
	
	# If an exception occurs during the execution of try clause
	# the rest of the clause is skipped
	# If the exception type matches the word after except
	# the except clause is executed
	try:
		# Receives the request message (of max size 4096) from the client (& decodes into string)
		message = connectionSocket.recv(4096).decode() # Custom Code

		# message looks like 
		# 	GET /localhost:6789/helloworld.html HTTP/1.1
		# 	...
		request = message.split()[1]		# /localhost:6789/helloworld.html
		
		serverAddr = request.split('/')[1] 	# localhost:6789
		f = request.split('/')[2]			# helloworld.html

		# Send the HTTP response header line to the connection socket
		# Fill in start

		# Fill in end
 
		# Send the content of the requested file to the connection socket
		
		# Close the client connection socket
		connectionSocket.close()

	except IOError:
		# Send HTTP response message for file not found
		# Fill in start
		connectionSocket.send("404 Not Found".encode())
		# Fill in end
        
		# Close the client connection socket
		# Fill in start
		connectionSocket.close()
		# Fill in end

serverSocket.close()  