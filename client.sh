echo "This is the bash file for the client"
echo "The client uses '127.0.0.1' as a host and the port 15000"
echo "The client connects automatically to the server"
echo "When the client is connected to the server it informs the user"
echo "The client receives the artist name from the user and encodes the input and sends it to the server"
echo "The server responds with an answer and the client receives this answer (songs or error) from the server. The songs and the errors are transmitted and represented as strings"
echo "This can happen indefenetly until the client sends the command 'q' which stands for quit"
echo "When q is received from the user, the client sends this to the server, then the server closes the connection and sends a message back to the client"
echo "and the connection is closed and the user is informed. Then the user should press enter to close the terminal"

#!/bin/bash

python3 client.py 
