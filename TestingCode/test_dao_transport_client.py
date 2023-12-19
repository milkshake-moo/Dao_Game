
"""
This file is intended to help test the DaoTransport class and the DaoTransportInterface class.

This file contains a script that will act as a client object and do some
hardcoded interactions with a server script

Add lots of comments here so that this can be used as a reference when working 
with the DaoTransport class
"""

import sys
# set sys path to allow imports from the parent directory
sys.path.append('../Dao_Game')


# import all the things!
import Backbone.DaoMsgDef as DaoMsg
from Backbone.DaoTransport import DaoTransport


# constants and common variables
ip = "localhost"
ip = '127.0.0.1'
server_port = 8082
client_port = 8081
wait_time_seconds = 60

#TODO:  Test this for connecting from different computers



# main function for testing stuff
def main():

    print()
    print("TESTING THE DAOTRANSPORT CLASS: ")
    print()

    # create the client DaoTransport object
    # this will create a socket that isn't configured to listen for incomming commuinications
    # this socket will use the ip and run on the port that is provided
    client = DaoTransport(is_server=False, ip=ip, port=client_port)


   # make some standard dao messages to send
    msg_1 = DaoMsg.build_challenge_to_game_msg(player_name="TJ", player_color="white")
    msg_2 = DaoMsg.build_request_draw_msg()
    msg_3 = DaoMsg.build_legal_move_msg(dao_piece=DaoMsg.tempData(), new_position=DaoMsg.tempData())
    

    # connect to the server
    client.connect_to_server(server_ip=ip, server_port=server_port)

    # send the first dao message to the server
    print("Sending Daomsg 1: ",client.send_dao_msg(msg_1))
    # receive a msg from the server
    rsp_1 = client.wait_for_incomming_dao_msg(wait_time_seconds)
    print("Received Daomsg 1: ", rsp_1 != None)

    # send the second dao message to the server
    print("Sending Daomsg 2: ",client.send_dao_msg(msg_2))
    # receive a msg from the server
    rsp_2 = client.wait_for_incomming_dao_msg(wait_time_seconds)
    print("Received Daomsg 2: ", rsp_2 != None)

    # send the thrid dao message to the server
    print("Sending Daomsg 3: ",client.send_dao_msg(msg_3))
    # receive a msg from the server
    rsp_3 = client.wait_for_incomming_dao_msg(wait_time_seconds)
    print("Received Daomsg 3: ", rsp_3 != None)


    # close the DaoTransport - This closes the socket on the computer
    print("Closing Client: ",client.close())


    # print out information about all of the messages we received
    print()
    print("CLIENT RECEIVED MESSAGES:")
    print()
    player_name, accepted_status = DaoMsg.extract_challenge_response_msg(rsp_1)
    print(rsp_1.msg_code)
    print(rsp_1.payload_length)
    print(player_name)
    print(accepted_status)
    print()
    accepted_status = DaoMsg.extract_draw_response_msg(rsp_2)
    print(rsp_2.msg_code)
    print(rsp_2.payload_length)
    print(accepted_status)
    print()
    print(rsp_3.msg_code)
    print(rsp_3.payload_length)


# start the client script when this program is run
if __name__ == "__main__":
    main()

