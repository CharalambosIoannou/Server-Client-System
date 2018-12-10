import socket
import re
import datetime
import time
import logging

def getSong(n):
    return n


#predifined host and port number selected by me. The host address is the local address and the port is just a random number of a free port. Usually a number greater than 1023
host = '127.0.0.1'
port = 15000      

#command to create log files. This means it will create a log file named Server, every time the server is run it will rewrite the file and the logging level will be info
logging.basicConfig(filename="server.log",filemode='w', level=logging.INFO)

def Server(host,port):
    if ( 0<= port <= 1023): #these ports are busy so it won't allow the server to connect to these ports
        print("Port number is busy")
        logging.info("Connection not successful" )

        closePrint= datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        close=datetime.datetime.now()
        return "Exception","Exception"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create TCP welcoming socket
    try:
        sock.bind((host, port))
        sock.listen() #server begins listening for incoming TCP requests
        connection, addr = sock.accept() #server waits on accept() for incoming requests and a new socket is created on return

        print('Connected Succesfully:', sock.getsockname())
        clientRequestPrint = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        clientRequest=datetime.datetime.now() #this date is used for subtracting the start time with the close time only.
        print("Client connection Request: " , clientRequestPrint)
        logging.info("Date and time of incoming client connection request: %s " % (clientRequestPrint))
        logging.info("Connected Succesfully on: %s " % (str (sock.getsockname())))
        while True:
            data=connection.recv(1024).decode() #decode the received data and get the artist name from the client 
            print("Data: ",data)
            
            if (data is "q"): #if the data received is the letter q then quit and stop the server from listening for new requests
                print("Server shutting down")
                connection.send("Server shutting down".encode())
                closePrint= datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                close=datetime.datetime.now()
                print("Close Time: ", closePrint)
                connection.close()
                sock.close()                
                return clientRequest,close

            logging.info("Received artist name from client: %s " % (data))
            connection.send("Artist request was received successfully ".encode())
    
            global str1
            songs=[]
            songsCloned=[]
            answer=[]
            with open("100worst.txt") as f:
                songsOnebyOne=map(getSong,f.readlines()) #read line by line 
                mylist = [x.strip() for x in songsOnebyOne] # place the songs in a list
                
                del mylist[:6] #remove the first 6 lines which are empty or contain information that we don't want to process
                del mylist[-23:] #remove the last 23 lines which contain information that we don't need
                for i in range(len(mylist)):
                    if (mylist[i][0].isdigit()==True): #if the line starts with a digit place it inside a list
                        songs.append(mylist[i])
                    else:
                        prev = mylist[i-1] # if the line does not start with a digit get the current element and the previous elements and merge them together. This means that it is a special case where the song name and artis are found in a separate line
                        curr= mylist[i]
                        songs.remove(prev)
                        full_song= prev + "        " + curr #combine the previous line which is the song name with the current line which is the artist name
                        songs.append(full_song)

                for i in songs:
                    songsCloned.append(re.split(r'\s{2,}', i))
            counter=0
            d={} #initialize dictionary
            for i in songsCloned:
                str1='='.join(songsCloned[counter]) #join the string together and split them using an equals sign so that we can place it in a dictionary later on
                str1=re.sub("\d+", "", str1) #remove digits from string
                str1=re.sub("-", "", str1) #remove dashes from string
                str1=str1[:-1] #remove empty space from string
                if ("Lobo" in str1): #if artist is Lobo replace the dash with the equals sign so that it has the same format as the rest of the songs-artists
                    str1=str1[:-4] + "=" + "Lobo"   
                counter=counter+1
                l=str1.split('=') #split the string that have an equal sign
                a=str (l[0]) #get the first element in the list which is the song name
                b=str (l[1]) #get the second element in the list which is the artist's name

                d[a] = str (b) #place them in a dictionary

            ans=[]
            found=0
            temp=0
            error=False
            for song, artist in d.items(): #iterate through key-value pairs     
                if (data== artist): #if the input from user is exaclty the same as the artist name in the dictionary
                    found=found+1
                    ans.append(song[1:]) #place answer in a list and remove the first extra space
                elif ((data in artist) and  ("/" in artist)  ) : #if the input from the user is an artist which has a song along with another artist and their names are separated by a "/"
                    artList=artist.split("/") #separate the string from the character "/" and place the artist names in a list
                    try:
                        indexArtList=artList.index(data)
                        
                        if (data in artist and len(data)==len(artList[indexArtList]) ) : #check if the lengths are the same to ensure the correct input is received otherwise print an error after the loop finishes
                            found=found+1
                            ans.append(song[1:])
                    except:
                        temp=1
                        break
                elif (data in artist) and  ("&" in artist): #if the input from the user is an artist which has a song along with another artist and their names are separated by a "&"

                    artList1=artist.split(" & ")
                    try:
                        indexArtList1=artList1.index(data)
                        if (data in artist and len(data)==len(artList1[indexArtList1]) ) :                         
                            found=found+1
                            ans.append(song[1:])

                    except:
                       temp=1
                       break
                if (data.lower()in artist.lower() and found==0): #convert both the input from the user and the artist to lowercase to check whether the artist name exists but the user typed the name wrong
                    print("No songs associated to a given artist")
                    connection.send("No songs associated to a given artist".encode())
                    error=True
                    break
                elif (data.upper()in artist.upper() and found==0): #convert both the input from the user and the artist to uppercase to check whether the artist name exists but the user typed the name wrong
                    print("No songs associated to a given artist")
                    connection.send("No songs associated to a given artist".encode())
                    error=True
                    break
                
                    
            if (found==0 and error==False): #check whether the user entered something completely wrong and no artist is found in the file
                print("Non-existing artist")
                connection.send("Non-existing artist".encode())
                #print("Non-existing artist")

            if (len(ans)!=0): #when there is a song(s) associated with an artist name these are converted into a string separated by comma and sent to the client
                print(ans)
                ans2string=','.join(ans)
                connection.send(ans2string.encode())

                
            sock.listen()
    except ConnectionAbortedError:
        print("Client Disconnected")
        return "Exception","Exception"
    except ConnectionResetError:
        print("Client Disconnected")
        return "Exception","Exception"
        


start = time.strftime("%d/%m/%Y %H:%M:%S") #start time
print("Start time: ",start)
logging.info("Start time: %s " % (start))
a,b=Server(host,port)
if (a is not "Exception" and b is not "Exception"): #if exceptions are received then do not do any calculations of time and date
    time=abs (b - a)
    time2sec=round (time.total_seconds()  )
    print("Time difference: ", str (time2sec) , " seconds")
    logging.info("length of time the server was connected to a client: %s " % (str (time2sec)) +  " seconds")
