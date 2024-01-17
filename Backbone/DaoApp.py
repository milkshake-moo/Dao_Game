
"""
This file houses the Dao App.
The Dao App is the thing that will tie everything together into a working program

The Dao App will connect the gui, game object, and transport layer together to be a functioning dao game
"""


import sys
# set sys path to allow imports from the parent directory
sys.path.append('../Dao_Game')


# import all the thigsssssss!
from DaoGameObject import *
from DaoTransport import *
from DaoMsgDef import *
from DaoGui import *







# Dao App class
class DaoApp():
    """
    This class will connect a gui and a transport layer to a dao game object
    This is overarching class you will use to run the whole dao program
    """

    # initialize stuff for the class
    def __init__(self):
        # setup variables that have constant values
        self.local_port = None          # the port to use for the transport service on the local machine
        self.peer_port = None           # the port to connect to on a remote machine

        # vars to store player / program info
        self.is_server = False          # tracks whether we are hosting the game session or joining a remote session
        self.player = None              # the person locally using the dao app through the gui
        self.local_address = None       # the ip of our local machine
        self.peer_address = None        # the ip of the remote Dao App we will connect to / that is connecting to us
        
        # Major Dao Objects
        self.dao_game = None            # The DaoGameObject where the game of Dao is actually played / tracked
        self.dao_transport = None       # The Transport layer that lets a remove user interact with us and us with them
        self.dao_gui = None             # The gui that the local user will interact with



    # function to start a game of Dao


    # function to create the Dao gui object and set it as the apps active interface
    def init_dao_gui(self):
        self.dao_gui = DaoGui(self)















# main method for running an instance of the Dao App class when this python file is run
# moving this to a seperate file just for running the Dao application might be a better idea
def main():
    # create the dao application instance
    main_app = DaoApp()

    # TESTING CODE

    # build a dao object
    player_0 = DaoPlayer("donny", "black")
    player_1 = DaoPlayer("MilkshakeMoo", "white")
    main_app.dao_game = DaoGameObject(player_0, player_1)
    main_app.player = player_0
    # initialize the dao_gui interface for testing
    main_app.init_dao_gui()





# init main when this is run
if __name__ == "__main__":
    main()


