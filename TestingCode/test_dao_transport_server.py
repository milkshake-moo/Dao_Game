
"""
This file is intended to help test the DaoTransport class.

This file contains a script that will act as a server object and do some
hardcoded interactions with a client script

Add lots of comments here so that this can be used as a reference when working 
with the DaoTransport class
"""

import sys
# set sys path to allow imports from the parent directory
sys.path.append('../Dao_Game')


# import all the things!
from Backbone.DaoTransport import DaoTransport
import Backbone.DaoMsgDef as DaoMsg
 


# constants and common variables
ip = "localhost"
server_port = 8082
client_port = 8081
wait_time_seconds = 60



# main function for testing stuff
def main():

    print()
    print("TESTING THE DAOTRANSPORT CLASS: ")
    print()

    # create the server DaoTransport object
    # this will create a socket configured to listen for incomming connections
    # this socket will use the ip and run on the port that is provided
    server = DaoTransport(is_server=True, ip=ip, port=server_port)


    # make some standard dao messages to send
    msg_1 = DaoMsg.build_challenge_response_msg(player_name="Nic", accepted_status=True)
    msg_2 = DaoMsg.build_draw_response_msg(accepted_status=False)
    msg_3 = DaoMsg.build_legal_move_msg(dao_piece=DaoMsg.tempData(), new_position=DaoMsg.tempData())

    
    # wait for an incomming client connection
    print("Server Accepted client connection: ",server.wait_for_client_connect(wait_time_seconds))

    
    # receive a msg from the client
    rsp_1 = server.wait_for_incomming_dao_msg(wait_time_seconds)
    print("Received Daomsg 1: ", rsp_1 != None)
    # send the first dao message to the client
    print("Sending Daomsg 1: ",server.send_dao_msg(msg_1))

    # receive a msg from the client
    rsp_2 = server.wait_for_incomming_dao_msg(wait_time_seconds)
    print("Received Daomsg 2: ", rsp_2 != None)
    # send the second dao message to the client
    print("Sending Daomsg 2: ",server.send_dao_msg(msg_2))

    # receive a msg from the client
    rsp_3 = server.wait_for_incomming_dao_msg(wait_time_seconds)
    print("Received Daomsg 3: ", rsp_3 != None)
    # send the thrid dao message to the client
    print("Sending Daomsg 3: ",server.send_dao_msg(msg_3))


    # close the DaoTransport - This closes the socket on the computer
    print("Closing Server: ",server.close())



    # print out information about all of the messages we received
    print()
    print("SERVER RECEIVED MESSAGES:")
    print()
    player_name, player_color = DaoMsg.extract_challenge_to_game_msg(rsp_1)
    print(rsp_1.msg_code)
    print(rsp_1.payload_length)
    print(player_name)
    print(player_color)
    print()
    print(rsp_2.msg_code)
    print(rsp_2.payload_length)
    print()
    print(rsp_3.msg_code)
    print(rsp_3.payload_length)






# start the client script when this program is run
if __name__ == "__main__":
    main()



