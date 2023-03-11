# Import socket module
from socket import *

# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# define local host & port to connect to
HOST = "0.0.0.0"
PORT = 6789

# start socket server
serverSocket.bind((HOST, PORT))
serverSocket.listen()

# Server should be up and running and listening to the incoming connections
while True:
	print('Ready to serve...')
	
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()
	
	try:
		# Receives the request message (of max size 4096) from the client (& decodes into string)
		message = connectionSocket.recv(4096).decode() # Custom Code

		# Extract the filename from the second space-delimited element
		filename = message.split()[1]

		# Exclude the character '\' and open the file in byte mode
		f = open(filename[1:], 'rb')

		# Store the entire content of the requested file in a temporary buffer
		outputdata = f.read()

		# Send the HTTP response header line to the connection socket
		connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
 
		# Send the content of the requested file to the connection socket
		connectionSocket.sendall(outputdata)
		
		# Close the client connection socket
		connectionSocket.close()

	except IOError:
		# Send HTTP response message for file not found
		connectionSocket.send("HTTP/1.1 404 Not Found".encode())
        
		# Close the client connection socket
		connectionSocket.close()

serverSocket.close()  