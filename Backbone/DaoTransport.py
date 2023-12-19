
"""
This file contains an implementation of a Dao Transport class
This class is responsible for sending and receiving Dao Messages using sockets

This class can be instantiated by other functions and classes to allow for
communication between two different programs


Code within this file should be well commented so that it can be used for
reference later and to make understanding all this a little easier
"""

import sys
# set sys path to allow imports from the parent directory
sys.path.append('../Dao_Game')

# import all the stuff!
import Backbone.DaoMsgDef as DaoMsg
import socket
import time
import os



# global constants
CHECK_SOCKET_STATUS_DELAY = 0.01        # (seconds) This is how long python will wait between checking socket statuses if loop checking
SOCKET_SERVER_CONNECTION_TIMEOUT = 60   # (seconds) This is how long a server will wait for a client to connect before timing out




# DaoTransport Class object
class DaoTransport():
    """
    A Dao Transport class is responsible for directly interfacing with sockets and sending / receiving data.
    It is also capable of sending specific Dao messages
    - is_server:    This identifies if this Transport class will act as a socket client or socket server
    - ip:           This will be the ipv4 address used for the socket
    - port:         This will be the port used for the socket
    """

    # function to initialize values
    def __init__(self, is_server : bool, ip, port) -> None:
        # save the given parameters
        self.is_server = is_server
        self.ip = ip
        self.port = port
        # create our socket object
        self.is_socket_alive : bool = self.create_socket()
        # initialize other values
        self.connected_ip = None
        self.connected_port = None
        self.is_connected : bool = False
        self.connected_socket : socket.socket= None
        

    # This function creates a new socket object for the Transport class
    def create_socket(self):
        success = False
        new_socket = None
        try:
            # create a new socket using an IPV4 address that is configured to use TCP connections
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # getting data from the socket should not be a blocking operation
            new_socket.setblocking(False)
            new_socket.bind((self.ip, self.port))
            # server sockets should be configured to listen for incomming connections
            if self.is_server:
                new_socket.listen(1)
            success = True
        except socket.error as err:
            print("Socket creation failed: %s" %(err))
        self.main_socket = new_socket
        return success


    # BLOCKING This function will establish a connection between our socket and some server socket
    def connect_to_server(self, server_ip, server_port):
        """Returns True if it successfully connects to a server"""
        connected_to_server = False
        # make sure this instance of Dao Transport is using a client socket
        assert not self.is_server, "A server cannot connect to another server"
        try:
            self.main_socket.setblocking(True)
            self.main_socket.connect((server_ip, server_port))
            self.main_socket.setblocking(False)
            self.connected_ip = server_ip
            self.connected_port = server_port
            self.is_connected = True
            connected_to_server = True
            print("Successfully connected to server!")
        except Exception as e:
            print("Could not connect to server!: %s"%(e))
        return connected_to_server


    # BLOCKING This function will wait for a client socket to connect to our server socket
    def wait_for_client_connect(self, timeout):
        """This returns True if a connection was accepted, False otherwise"""
        # make sure this instance of Dao Transport is using a server socket
        assert self.is_server, "A client cannot accept incomming connections"
        did_client_connect = False
        # wait for incomming connections for timeout time
        start_time = time.time()
        while time.time() < start_time + timeout:
            try:
                # attempt to accept an incomming connection
                connected_socket, connected_ip = self.main_socket.accept()
                # if this attemtp is successful, save the socket info and return
                connected_socket.setblocking(False)
                self.connected_socket = connected_socket
                self.connected_ip = connected_ip
                self.is_connected = True
                did_client_connect = True
                break
            except BlockingIOError:
                time.sleep(CHECK_SOCKET_STATUS_DELAY)
            except Exception as e:
                print("An error occured while waiting for a connection! %s"%(e))
                break
        if time.time() > start_time + timeout:
            print("Timed out while waiting for an incomming connection")
            
        return did_client_connect
    

    # This function will close the main socket 
    def close(self):
        """Returns true if the socket was closed"""
        closed = False
        # check to make sure that the socket exists
        if self.is_socket_alive:
            # if this is a server, we should also close any incomming connections
            if self.is_server and self.is_connected:
                self.disconnect(was_connection_aborted=False)
            # shutdown the connection to the connected socket if there is one
            if self.is_connected:
                self.main_socket.shutdown(0)
            # close the main socket
            self.main_socket.close()
            self.is_socket_alive = False
            closed = True
        return closed
        

    # This functin will handle disconnects from a connected socket
    def disconnect(self, was_connection_aborted : bool = False):
        """Returns true if it disconnects from a connected socket"""
        disconnected = False
        # our socket must exist in order to have a connection
        if self.is_socket_alive:
            if self.is_server and not was_connection_aborted:
                # server sockets close the connected socket
                if self.is_connected: 
                    self.is_connected = False
                    try:
                        self.connected_socket.shutdown(0)
                        self.connected_socket.close()
                    except Exception as e:
                        print("Encountered Exception when attempting to close the connected socket: %s" %(e.__ne__))
                        print("%s" %(e))
                    self.connected_ip = None
                    self.connected_port = None
                    self.connected_socket = None
                    disconnected = True
            elif self.is_server and was_connection_aborted:
                # handling a connection aborted event, the connected socket disconnected from us
                self.is_connected = False
                self.connected_ip = None
                self.connected_port = None
                self.connected_socket = None
                # we did not initiate the disconnection, only responding to it, so disconnected remains false
            elif not self.is_server:
                # client sockets close and recreate themselves
                if self.is_connected:
                    self.is_connected = False
                    self.close()
                    self.is_socket_alive = self.create_socket()
                    self.connected_ip = None
                    self.connected_port = None
                    self.connected_socket = None
                    disconnected = True
        # return the disconnected status
        return disconnected


    # This function will check to see if the Transport class has received any new Dao messages
    def check_for_incomming_bytes(self):
        """Returns a byte array if successful, a 'None' type if not"""
        msg : bytes = None
        # if we're not connected to another socket, don't try to sampel the socket
        if not self.is_connected:
            print("Not connected!  There is no information to read")
            return msg
        try:
            # check the incomming socket for new information
            if self.is_server:
                msg = self.connected_socket.recv(1024)
            else:
                msg = self.main_socket.recv(1024)
        # A BlockingIOError occurs if there was nothing to read from the socket
        except BlockingIOError:
            pass
        # A ConnectionAbortedError occurs if the incomming socket is no longer connected
        except (ConnectionAbortedError, ConnectionResetError):
            print("Connection was aborted!")
            self.disconnect(was_connection_aborted=True)
        # Idk if other exceptions can occur, but catch and print them if they do
        except Exception as e:
            print("Encountered Exception: %s" %(e.__ne__))
            print("%s" %(e))
        
        # if we receive a zero byte length array, then we know socket has or is about to disconnect
        if msg != None and len(msg) == 0:
            msg = None
            # add additional disconnect behavior?
            self.disconnect(was_connection_aborted=True)
        return msg


    # BLOCKING This function will wait until there is an incomming message
    def wait_for_incomming_bytes(self, timeout : int):
        """Returns a byte array if successful, and a 'None' type if not"""
        # this will repeatidly call check_for_incomming_bytes until something arrives or timeout time has passed
        msg : bytes = None
        start_time = time.time()
        while time.time() < start_time + timeout:
            if self.is_connected:
                # check for an available message
                msg = self.check_for_incomming_bytes()
                if msg != None:
                    # we received a msg
                    break
            else:
                # we disconnected for some reason, stop waiting for an incomming message
                break
        return msg


    # this function will return a Standard Dao Msg object if we have received one
    def check_for_incomming_dao_msg(self):
        """Returns a standard dao message object if successful and a 'None' type if not"""
        msg : DaoMsg.StandardDaoMsg = None
        msg_bytes = None
        # check the inbox for any new messages
        if self.is_connected:
            msg_bytes = self.check_for_incomming_bytes()
        # create a Standard Dao Msg out of the received bytes if there were any
        if msg_bytes != None:
            msg = DaoMsg.StandardDaoMsg()
            msg.buildFromBytes(msg_bytes)
        # return the Standard Dao msg
        return msg
    
    
    # BLOCKING This function will wait until there is an incomming Standard Dao msg and then return it
    def wait_for_incomming_dao_msg(self, timeout : int):
        """Returns a standard dao message object if successful and a 'None' type if not"""
        msg : DaoMsg.StandardDaoMsg = None
        msg_bytes = None
        # wait timeout time for incomming bytes
        if self.is_connected:
            msg_bytes = self.wait_for_incomming_bytes(timeout)
        # if we received anything, assemble it into a standard dao message
        if msg_bytes != None:
            msg = DaoMsg.StandardDaoMsg()
            msg.buildFromBytes(msg_bytes)
        # return the standard dao msg
        return msg


    # This function will send some bytes to a connected socket
    def send_bytes(self, msg : bytes):
        """Returns the number of bytes sent"""
        bytes_sent = 0
        if self.is_connected:
            if self.is_server:
                bytes_sent = self.connected_socket.sendall(msg)
            else:
                bytes_sent = self.main_socket.sendall(msg)
        return bytes_sent
    

    # This function will send a Standard Dao Msg to a connected socket
    def send_dao_msg(self, msg : DaoMsg.StandardDaoMsg):
        """Returns True if the msg was sent"""
        sent = False
        if self.is_connected:
            sent_bytes = self.send_bytes(msg.getBytes())
            if sent_bytes != 0: sent = True
        return sent
    

    # BLOCKING This funciton will send a Standard Dao Msg and then wait for a response
    def send_msg_and_get_response(self, msg : DaoMsg.StandardDaoMsg, timeout : int):
        """Returns a Standard Dao Message if it was able to receive one"""
        rsp : DaoMsg.StandardDaoMsg = None
        # send the outgoing dao message
        status = self.send_dao_msg(msg)
        # if we were successfully able to send the message, wait for a response message
        if status:
            status = self.wait_for_incomming_dao_msg(timeout)
        # return the rsp
        return rsp
        

    # BLOCKING This function will send a challege request and await the response
    def send_challenge_and_get_response(self, local_player_name : str, local_player_color : str, timeout : int):
        """This sends a 'challenge to game' dao msg and waits for a 'challege response' message.  
        This will return the contents of the challege response message"""
        remote_player_name : str = None
        accepted_status : bool = None
        # create a challenge request message
        msg = DaoMsg.build_challenge_to_game_msg(player_name=local_player_name, player_color=local_player_color)
        # send the message and get a response
        rsp = self.send_msg_and_get_response(msg, timeout)
        # extract the data from the response
        if rsp != None and rsp.msg_code == DaoMsg.DaoMsgCode_e.challenge_response:
            remote_player_name, accepted_status = DaoMsg.extract_challenge_response_msg(rsp)
        else:
            # TODO:  Throw an error here if no response / wrong msg_code was received?
            pass 
        return remote_player_name, accepted_status


    # BLOCKING This function will send a draw request and await the response
    def send_draw_and_get_response(self, timeout : int):
        """This sends a 'request draw' dao msg and waits for a 'draw response' message.  
        This will return the contents of the challege response message"""
        accepted_status : bool = None
        # create the draw request
        msg = DaoMsg.build_request_draw_msg()
        # send the message and get a response
        rsp = self.send_msg_and_get_response(msg, timeout)
        # extrac the data fro mthe response
        if rsp != None and rsp.msg_code == DaoMsg.DaoMsgCode_e.draw_response:
            accepted_status = DaoMsg.extract_draw_response_msg(rsp)
        else:
            # TODO:  Throw an error here if no response / wrong msg_code was received?
            pass
        return accepted_status


    # TODO:  Add more helpful send functions for certain types of msg_codes?   
    #        It might be better to handle this outside of this class and more modularly





