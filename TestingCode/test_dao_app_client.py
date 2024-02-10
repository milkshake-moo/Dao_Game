
"""
This is a testing file to test aspects of the Dao App class when it is used to connect to another Dao App that acts as a server.

The functions in the main method exist to test basic things about the Dao app when connecting to another Dao App
"""

import sys
# set sys path to allow imports from the parent directory
sys.path.append('../Dao_Game')

# imports and things
from Backbone.DaoMsgDef import *
from Backbone.DaoTransport import *
from Backbone.DaoApp import *
from Backbone.DaoGameObject import *




# main function for running testing code
def main():
    # configure user and connection data for testing
    local_user = DaoPlayer("donny", "black")
    ip = "localhost"
    port = 8081
    server_ip = "localhost"
    server_port = 8082

    # configure an instance of the Dao App using this data
    app = DaoApp()

    # TEMPORARY BEHAVIOR
    # TODO remove after initial gui screen is added

    # hardcode app data
    print("Preparing App Data...")
    app.local_address = ip
    app.local_port = port
    app.is_server = False
    app.player = local_user

    # initialze transport layer
    print("Initializing transport layer...")
    app.init_transport_interface(app.is_server, app.local_address)

    # connect to a server instance of this application
    print(f"Connecting to server at: {server_ip}:{server_port}")
    app.peer_port = server_port
    status = app.connect_to_server_app(server_ip)
    assert status, "Failed to connect to target server"
    
    # testing delay
    #print("Waiting for a few seconds before continuing...")
    #time.sleep(3)

    # request a dao game
    print("Requesting a Dao game...")
    request = build_challenge_to_game_msg(app.player.name, app.player.color)
    app.outstanding_request = True
    # use the transport layer of the app to send the request to the server
    status = app.dao_transport.send_dao_msg(request)
    print(f"Request status: {status}")

    # testing delay
    #print("Waiting for a few seconds before continuing...")
    #time.sleep(3)

    # wait for a response
    print("Awaiting challenge response...")
    # run the main update loop until a response has been received
    while (app.dao_game == None):
        app.init_main_update_loop()



# run the main function when this script is run
if __name__ == "__main__":
    main()