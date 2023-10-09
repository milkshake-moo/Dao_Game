
"""
This is a test socket programming client script

This script will sit and wait for user input and then send some info to a
server script to be handled

This exists to figure out how sockets work and as reference code for later

To start this script, run: "py test_socket_client.py" in a command window
or run it in a dedicated terminal through VS Code
NOTE:  The server script should be run first, the client tries to connect on startup

Behavior:
    - Script launches
    - creates a socket
    - attempts to connect to a server script
    - The following Loops forever:
        - waits for user input
        - sends user input to the server script
        - waits for a response from the server
"""

# imports
import socket
import time

# constants for networking
clientPort = 8081       # this is the port the client socket will run on
serverPort = 8082       # this is the port the server socket will run on
                        # these have to be different if running both scripts on the same computer

ip = "localhost"        # This is the ip address both sockets are configured to use / connect to
                        # this is equivelent to 127.0.0.1

delay_for_wait = 0.01   # this is an added delay for the loop
                        # This isn't really needed, but I did play around with it in testing


# setup function to initialze network stuff at the start of the script
def setupSocket():
    clientSocket = None
    print("")
    try:
        # AF_INET tells the socket to use IPv4 addresses
        # SOCK_STREAM tells the socket to use a TCP connection
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientInfo = (ip, clientPort)
        clientSocket.bind(clientInfo)
        print("Socket Created")
    except socket.error as err:
        print("Socket creation failed: %s" %(err))
    return clientSocket


# connect to the server script
def connectToServer(socket):
    # attempt to connect to a socket running at the hardcoded ip / port
    serverInfo = (ip, serverPort)
    socket.connect(serverInfo)
    print("Connected To the Server!")


# Call this to prompt the user to enter some text in the console
def getUserInput():
    userInput = input("\nEnter some text: ")
    return userInput


# funciton to send something to the server
def sendToServer(text, socket):
    wasDataSent = False
    # this protects against detecting user input and sending an empty message to the server
    if len(text) > 0:
        # this is where the message is actually set to the server
        socket.sendall(text.encode())
        wasDataSent = True
    else:
        print("You must enter some text.")
    return wasDataSent


# main function for client loop
def main():
    # do initial setup stuffs
    clientSocket = setupSocket()
    connectToServer(clientSocket)
    # loop forever until keyboard interrupt (ctrl C)
    while True:
        try:
            # wait for user input from the console
            userInput = getUserInput()
            # send user input to the server
            wasDataSent = sendToServer(userInput, clientSocket)
            # if some data was sent, expect a response
            if wasDataSent:
                # wait for response from the server
                response = clientSocket.recv(1024).decode()
                # print the response
                print("")
                print("Resonse from Server Received!: ")
                print(response)
            # delay before next loop
            time.sleep(delay_for_wait)
        except KeyboardInterrupt:
            # if a keyboard interrupt occurs, we exit
            break


# start the client script when this program is run
if __name__ == "__main__":
    main()





    
