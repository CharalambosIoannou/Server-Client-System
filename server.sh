echo "This is the bash file for the Server"
echo "The server uses '127.0.0.1' as a host and the port 15000"
echo "When the client is connected the server informs the user"
echo "The server works by receiving the artist's name and looks it up in the text file to find the corresponding song(s)"
echo "This is done by reading the text file and placing each line in a list. Then any songs where their artist name is in a new line are merged with their artists"
echo "Any additional characters like numbers or dashes are removed"
echo "Then for every element in the list an equals sign is inserted to separate the artist name with the song"
echo "The song name and their artist name are then placed in a dictionary in this order."
echo "The server finds the key-value pairs for the songs and artists and checks if a value matches the input from the user"
echo "If it does then the song name is returned as a string. If multiple songs are found then they are returned as strings and separated with a comma"
echo "If the user entered a completely wrong artist's name then the error that is send is 'No-existing artist' "
echo "If the user entered an artist name that is similar to a name in the dictionary, for example entering 'Michael Jackson' instead of 'MIchael Jackson' "
echo "then the error that is send is 'No songs associated to a given artist' "
echo "This can happen indefenetly until the client sends the command 'q' which stands for quit."
echo "When q is received the connection is closed, the server sends a message to the client informing about the close in connection "
echo "and the total time the client was connected is shown in seconds"


#!/bin/bash

python3 server.py 


