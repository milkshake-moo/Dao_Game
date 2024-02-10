
"""
This file houses the Dao App.
The Dao App is the thing that will tie everything together into a working program

The Dao App will connect the gui, game object, and transport layer together to be a functioning dao game
"""


import sys
# set sys path to allow imports from the parent directory
sys.path.append('../Dao_Game')


# import all the thigsssssss!
from Backbone.DaoGameObject import *
from Backbone.DaoTransport import *
from Backbone.DaoMsgDef import *
from Backbone.DaoGui import *







# Dao App class
class DaoApp():
    """
    This class will connect a gui and a transport layer to a dao game object
    This is the overarching class you will use to run the whole dao program
    """

    # initialize stuff for the class
    def __init__(self):
        # setup variables that have constant values
        self.local_port = None          # the port to use for the transport service on the local machine
        self.peer_port = None           # the port to connect to on a remote machine
        self.connection_timeout = 60    # the amount of time (seconds) to wait for a client to connect when hosting a server
        self.update_app_period = 50     # time in (ms) between app updates.  Gui interfaces should schedule these events

        # vars to store player / program info
        self.is_server = False          # tracks whether we are hosting the game session or joining a remote session
        self.player = None              # the person locally using the dao app through the gui
        self.local_address = None       # the ip of our local machine
        self.peer_address = None        # the ip of the remote Dao App we will connect to / that is connecting to us
        self.outstanding_request = False# tracks if we are currently requesting a new game or a draw from the connected player
        self.terminate_app = False      # the flag that triggers closing the main app update loop, setting this to true will close the app safely
        
        # Major Dao Objects
        self.dao_game = None            # The DaoGameObject where the game of Dao is actually played / tracked
        self.dao_transport = None       # The Transport layer that lets a remote user interact with us and us with them
        self.dao_gui = None             # The gui that the local user will interact with
        
        # Objects to track the state of the dao game
        self.dao_game_ids_to_piece = {} # This maps a piece id to the corresponding DaoPiece in the active dao game object

        # initialize the main game loop / the application
        #TODO: enable this code once the app is more complete and self contained
        #self.init_main_update_loop()



    #================== Initialization functions =========================
    """
    The following functions create instances of all the objects managed by the Dao App
    """
        

    # function to handle initializing a dao transport interface object
    def init_transport_interface(self, is_server, local_ip):
        # save configured values
        self.is_server = is_server
        self.local_address = local_ip
        # instantiate the dao transport object
        self.dao_transport = DaoTransport(is_server, self.local_address, self.local_port)


    # function to create a new game of dao (dao game object)
    def new_dao_game(self, player_0 : DaoPlayer, player_1 : DaoPlayer):
        #NOTE: The order you put players into this function is important, player_0 joins team 0 and player_1 joins team 1
        # create a new dao game object which will replace any existing one
        self.dao_game = DaoGameObject(player_0, player_1)
        # map all the pieces in the game with their id's
        self.dao_game_ids_to_piece = {}
        for piece in self.dao_game.get_dao_pieces():
            self.dao_game_ids_to_piece[piece.id] = piece
        # reset the players and piece positions in the gui if it has already been initialized
        if self.dao_gui is not None:
            self.dao_gui.reset_game_board() 


    # function to create the Dao gui object and set it as the apps active interface
    def init_dao_gui(self):
        self.dao_gui = DaoGui(self)
    

    # function to display the initial gui
    def init_initial_gui(self):
        #TODO: Implement the initial gui later, put the call to launch it here
        # - initial gui lets player pick a name, pick a color, see their ip address, host or connect to a game
        # PLACEHOLDER - running the dao game gui here until this is impelemted
        self.init_dao_gui()  # replace this with the real call later


    # function to kill the transport layer
    def terminate_transport_layer(self):
        #TODO: add misc cleanup behavior for in progress games, connectios, etc
        status = self.dao_transport.disconnect()
        return status


    #================== Game update functions =========================
    """
    These functions handle making updates to the dao game object or the dao gui
    """


    # function to handle a peer player move.  Returns true as long as it is a legal move for the opponent to make
    def peer_player_move(self, piece_id, board_pos):
        # get the dao piece associated with the piece id
        piece = self.dao_game_ids_to_piece[piece_id]
        # move the dao piece within the dao game object
        move_status, end_status = self.dao_game.move_dao_piece(piece, board_pos)
        # update the gui to reflect the move
        if move_status:
            self.dao_gui.remote_player_move_piece_update(piece_id, board_pos, end_status)
        return move_status





    #================== Communication functions =========================
    """
    These functions handle connecting and talking to a remote instance of the Dao App using the dao transport interface
    """

    # main update function, this will run periodically while the Dao App is running
    def periodic_transport_update(self):
        #TODO: add check for any received dao msg's
        #print("Periodic transport is Updating... ")
        new_msg = self.dao_transport.check_for_incomming_dao_msg()
        if new_msg != None:
            # we received a new message from the connected program!  now handle it
            print("Dao Msg Received!  Handling msg...")
            status = self.handle_received_dao_msg(new_msg)
            print(f"Handling status: {status}")

        #TODO: pipe received msg to handler function to decide what to do with a received msg
        pass


    # function to connect to a Dao App acting as a server
    def connect_to_server_app(self, peer_address):
        # store the address we are connecting to
        self.peer_address = peer_address
        # attempt to establish a connection with a dao app at that address (BLOCKING CALL)
        status = self.dao_transport.connect_to_server(peer_address, self.peer_port)
        return status


    # function to host a server using this Dao App
    def host_server_app(self):
        # wait for another dao app to connect to this dao app
        status = self.dao_transport.wait_for_client_connect(self.connection_timeout)
        #TODO: add better error handling
        # Assert false if no client connected
        assert status


    # function to handle sending a dao move to the connected app
    def send_local_move_data_to_peer(self, piece : DaoPiece, new_board_pos : tuple):
        # extract the data needed to format a move piece message
        id = piece.id
        message = build_legal_move_msg(id, new_board_pos)
        # send the move piece message to the connected client
        self.dao_transport.send_dao_msg(msg=message)
    

    # function to handle a received dao msg and then do stuff with it depending on what it is
    def handle_received_dao_msg(self, msg : StandardDaoMsg):
        status = False
        # figure out what kind of message this is
        code = msg.msg_code
        
        # Do stuff depending on what kind of message the opponent sent us
        if code == DaoMsgCode_e.challenge_to_game:
            # the opponent is challenging us to a game (or a rematch, but logically they're the same)
            # extract the request data and create a dao player object for the challenger
            opponent_name, opponent_color = extract_challenge_to_game_msg(msg)
            opponent = DaoPlayer(opponent_name, opponent_color)

            #TODO: create a popup in the active gui to accept or decline
            #TODO: set any flags for outstanding game request that are needed
            #TODO: Automatically reject the request if there is an ongoing game

            #TODO: THIS IS HARDCODED TO ACCEPT, remove this behavior once gui implementation is complete
            response = build_challenge_response_msg(player_name=self.player.name, player_color=self.player.color, accepted_status=True)
            # create a new dao game with the user data from the challenge request, the requesting player is always player_0
            self.new_dao_game(opponent, self.player)
            # send this response back to the challenger
            self.dao_transport.send_dao_msg(response)
            # since we accepted, disregard any outstanding game request we may have sent to the opponent
            self.outstanding_request = False
            status = True
            
        elif code == DaoMsgCode_e.challenge_response:
            # we recieved a response to our game request
            # ensure we were waiting on a response to an outstanding request
            if self.outstanding_request:
                # there is no longer an outstanding request
                self.outstanding_request = False

                # extract the data from the response and create a dao player object for the opponent
                opponent_name, opponent_color, challenge_status = extract_challenge_response_msg(msg)
                opponent = DaoPlayer(opponent_name, opponent_color)

                # check to see if the opponent accepted our challenge
                if challenge_status:
                    # opponent accepted! create a new dao game, we requested the game, so we are player 0
                    self.new_dao_game(self.player, opponent)
                    status = True

        elif code == DaoMsgCode_e.request_draw:
            # the opponent is requesting a draw
            status = True
            pass

        elif code == DaoMsgCode_e.draw_response:
            # the opponent responded to our draw request
            status = True
            pass

        elif code == DaoMsgCode_e.legal_move:
            # the opponent made a legal move on their dao board
            # extract the move data that the opponent sent
            piece_id, new_position = extract_legal_move_msg(msg)
            # perform this new move locally so the local player can see it
            status = self.peer_player_move(piece_id=piece_id, board_pos=new_position)
            pass

        else:
            status = False
        # if the message was successfully handled, return true
        return status




#================== Control functions =========================
    """
    These functions control the state of the dao app and the flow of the game
    """


    # this function just prints something to the main console output but with a text string to identify that it's from the app
    def print_from_app(text : str):
        print(f"Dao App: {text}")


    # this function is the loop that runs until the game is terminated and controls what gets updated 
    def init_main_update_loop(self):
        # setting this variable 
        terminate_app = False
        
        # main loop of the game
        #TODO: Make this into an actual loop, right now this is just called once per message call
        #while not terminate_app:

        # start loop
        
        # check the transport layer for any updates and handle them
        if self.dao_transport.is_connected:
            self.periodic_transport_update()
            
        # check to see if a dao game gui needs to be initialized and initialize it if we need to
        if (self.dao_game != None) and (self.dao_gui == None):
            self.init_dao_gui()

        # end loop
        

        # during termination, close everything
        # close any existing transport layer
        #TODO Enable this once the loop is enforced
        #if self.dao_transport.is_connected:
            #self.terminate_transport_layer()
        
        #TODO: terminate and save any game in session
        #TODO: terminate open gui
        #TODO: add other misc application closure behavior here






# main method for running an instance of the Dao App class when this python file is run
# moving this to a seperate file just for running the Dao application might be a better idea
def main():
    # create the dao application instance
    main_app = DaoApp()

    # TESTING CODE

    # build a dao object
    player_0 = DaoPlayer("donny", "black")
    player_1 = DaoPlayer("MilkshakeMoo", "white")
    #main_app.dao_game = DaoGameObject(player_0, player_1)
    main_app.player = player_0
    # initialize the dao_gui interface for testing
    main_app.new_dao_game(player_0, player_1)
    main_app.init_dao_gui()





# init main when this is run
if __name__ == "__main__":
    main()


