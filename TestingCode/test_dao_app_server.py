
"""
This is a testing file to test aspects of the Dao App class when it is used to run a server.

The functions in the main method exist to test basic things about the Dao app when connecting to another Dao App
"""

import sys
# set sys path to allow imports from the parent directory
sys.path.append('../Dao_Game')

# imports and things
from Backbone.DaoMsgDef import StandardDaoMsg
#from Backbone.DaoTransport import *
from Backbone.DaoApp import DaoApp
from Backbone.DaoGameObject import DaoPlayer



# main function for running testing code
def main():
    # configure user and connection data for testing
    local_user = DaoPlayer("DatBoi", "white")
    ip = "localhost"
    port = 8082

    # configure an instance of the Dao App using this data
    app = DaoApp()

    # TEMPORARY BEHAVIOR
    # TODO remove after initial gui screen is added

    # hardcode constants
    print("Preparing App Data...")
    app.local_address = ip
    app.local_port = port
    app.is_server = True
    app.player = local_user

    # initialze transport layer
    print("Initializing transport layer...")
    app.init_transport_interface(app.is_server, app.local_address)

    # host a server instance and wait for the client to connect
    print("Initializing socket server instance...")
    status = app.host_server_app()
    #assert status, "Client failed to connect"

    # expect to receive a dao game request
    print("Waiting to receive a request for a dao game...")
    # use the main update loop until there is a game in progress
    while (app.dao_game == None):
        app.init_main_update_loop()



# run the main function when this script is run
if __name__ == "__main__":
    main()