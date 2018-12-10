import socket
import datetime
import time
import logging


#predifined host and port number selected by me. The host address is the local address and the port is just a random number of a free port. Usually a number greater than 1023

    
host = '127.0.0.1'  
port = 15000
#command to create log files. This means it will create a log file named Server, every time the server is run it will rewrite the file and the logging level will be info

logging.basicConfig(filename="client.log",filemode='w', level=logging.INFO)

def Client (host,port):
    if ( 0<= port <= 1023): #these ports are busy so it won't allow the client to connect to these ports
        print("Port number is busy")
        closePrint= datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        close=datetime.datetime.now()
        return
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    try:
        sock.connect((host, port)) 
        print("Server connection is successful")
        while True:
            inp=input('Enter artists name: ')
            while (inp is "" or inp is " " or inp is "q"): #repeat until the input is not empty or not q  
                print("You did not input an artist name")
                inp=input('Enter artists name: ')
              
            timeSentPrint = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            timeSent=datetime.datetime.now()
            sock.sendall(inp.encode()) #send the artist name to the server but first encode it
                            
            data=sock.recv(1024).decode() #receive that the connection is successful
            data1=sock.recv(1024).decode() #receive song(s) or an error
            
            print('Received Connection', repr(data)) #print if connection was successfull or not 
            print('Received data', repr(data1)) #print the song(s) or an error 
            timeRecvPrint = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            timeRecv = datetime.datetime.now() #used to calculate time difference from sending and receiving data
            print("Received a response from the server: ",timeRecvPrint)
            bytesCount=0
            if (data1 != "No songs associated to a given artist") or (data !="Non-existing artist"):                    
                for a in data1: #convert data into binary and split them 8 bits at a time
                    conv=' '.join(format(ord(i),'b').zfill(8) for i in a)
                    convNumb=len(conv)/8 #divide the number of bits by 8 to find the number of bytes that were received
                    bytesCount=bytesCount+convNumb
            print("Bytes: ", bytesCount)

            difftime= abs (timeSent - timeRecv)
            time2sec=difftime.total_seconds() 

            print("It took " , str (time2sec)[:-3] , " ms to to receive a response from the server for the request to get songs for ",inp)
            
            logging.info("It took %s ms to to receive a response from the server for the request to get songs for: %s " % (str (time2sec)[:-3],inp))
            logging.info("The response length was %s  bytes "% bytesCount)
            logging.info("Received a response from the server: %s "% timeRecvPrint)
            
            inp1=input('Type q to disconnect: ')
            if (inp1 is "q"): #if the user types the letter q the client will send the letter q to the server and the server disconnects. Just before disconnecting the server sends a message to the client saying that it is disconnected
                sock.send(inp1.encode())
                test1=sock.recv(1024).decode()
                print('Received', repr(test1))
                return
                

    except ConnectionResetError:
        print("The server is not running/unavailable")
    except socket.error:
        print ('Failed to create socket')
    except:
        print("Server response not received")



Client(host,port)
input('Press ENTER to exit') # this is used when running the client from the command line. This is used so that the command line or terminal does not close directly when q is typed since data are still received. Instead the user should press enter to close the terminal.
