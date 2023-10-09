
"""
This is a test socket programming server script

This script should sit and wait to receive data from a client script
and then send back some kind of reply

This exists to figure out how sockets work and as reference code for later

To start this script, run: "py test_socket_server.py" in a command window
or run it in a dedicated terminal through VS Code
NOTE:  The server script should be run before the client script

Behavior:
    - Script launches
    - creates a socket
        - socket is configured to listen for incomming connections
    - Server will wait for an initial incomming connection
    - The following Loops forever:
        - server checks to see if there is a new message
            - server prints message from client
            - server sends a generic response back to the client
        - server checks to see if a client is still connected
            - the server will wait for a new connection if there isn't one
"""

# some info about socket stuff that took me a while to learn
"""
Blocking vs NonBlocking mode:

    - Blocking mode:
        In blocking mode, socket operations will wait for stuff to happen before returing.  This
        stops the script from being able to do anything else.

    - NonBlocking mode:
        In nonblocking mode, socket operations will check to see if something has occurred and
        throw a BlockingIOError if nothing has.  This lets the script go and do other things while
        it's waiting.

    -  EX:  msg = socket.recv(1024)
        - blocking:  Python script stops and waits until a msg is received on the socket or an error occurs
        - nonblocking:  Python script quickly checks to see if there is a msg and then returns it or an error
    
    This server script is configured to run in NonBlocking mode
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

                        # this is the response the server sends to the client
genericResponse = "Thank you for your message!"
logWhileWaiting = False # This is an optional flag that will make the server print waiting messages


# setup function to build the socket the server script will use
def setupSocket():
    print("")
    try:
        # AF_INET tells the socket to use IPv4 addresses
        # SOCK_STREAM tells the socket to use a TCP connection
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setblocking(False) # set socket to run in non blocking mode
        serverInfo = (ip, serverPort)
        serverSocket.bind(serverInfo)
        print("Socket Created")
        # put the socket in listen mode, allow only one incomming connection
        serverSocket.listen(1)
        return serverSocket
    except socket.error as err:
        print("Socket creation failed: %s" %(err))
        return None


# function to check a socket for new messages (non blocking)
def checkInbox(socket):
    # we assume that there is a live connection 
    connectionAlive = True
    msg = None
    try:
        # check the incomming socket for new information
        msg = socket.recv(1024).decode()
    # A BlockingIOError occurs if there was nothing to read from the socket
    except BlockingIOError:
        if logWhileWaiting: print("No incomming data...")
    # A ConnectionAbortedError occurs if the incomming socket is no longer connected
    except ConnectionAbortedError:
        print("Client connection aborted...")
        connectionAlive = False
    # Idk if other exceptions can occur, but catch and print them if they do
    except Exception as e:
        print("Encountered Exception: %s" %(e.__ne__))
        print("%s" %(e))
    # return whatever was in the inbox, and the connection status of the incomming socket
    return msg, connectionAlive


# This function will wait for an incomming connection
def waitForConnect(socket):
    print("Server is waiting for a connection... ")
    while True:
        try:
            # get the socket and ip of a client when they connect
            clientSocket, clientIp = socket.accept()
            # set the incomming clientsocket to non-blocking mode
            # this allows the server to check for new messages then go and do other things while it waits
            clientSocket.setblocking(False)
            print("Client Connected!")
            print("")
            break
        # A BlockingIOError will occur if there is no incomming connection to accept
        except BlockingIOError:
            if logWhileWaiting: print("still waiting for a connection")
            time.sleep(delay_for_wait)
        # There are probably other exceptions that can happen, print them out if they do
        except Exception as e:
            print("A different Exception occured")
            print(e.__ne__)
            break
    # return client information 
    return clientSocket, clientIp


# main function for server loop
def main():
    serverSocket = setupSocket()
    # wait for a connnection from the client
    clientSocket, clientIp = waitForConnect(serverSocket)
    # loop forever until keyboard interrupt
    while True:
        try:
            # check to see if we have received a new message
            msg, connectionAlive = checkInbox(clientSocket)
            if (msg != None) and (connectionAlive):
                # received a msg from the client
                # print the message from the client
                print("")
                print("Received a message!: ")
                print(msg)
                print("")
                # send a reply to the client
                clientSocket.sendall(genericResponse.encode())
            else:
                # There was no message to read
                if not connectionAlive:
                    # connection with the client was lost
                    # wait for a new connection
                    clientSocket, clientIp = waitForConnect(serverSocket)
                else:
                    # there is no new data to read on the connection
                    time.sleep(delay_for_wait)
        except KeyboardInterrupt:
            # if a keyboard interrupt occurs, we exit
            break


# init main when this is run
if __name__ == "__main__":
    main()






