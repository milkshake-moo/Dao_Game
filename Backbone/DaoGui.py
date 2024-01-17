
"""
This file houses the Dao Gui classes
The gui will be an interface the local user uses to interact with the Dao App and play the game

There needs to be a gui for the actual game and a startup gui to gather user information and initial setup
"""



import sys
# set sys path to allow imports from the parent directory
sys.path.append('../Dao_Game')


# import the thigs we need
from tkinter import *
import random

from DaoApp import DaoApp
from DaoGameObject import DaoGameEventCode_e





# Dao Gui class to play a game of dao
class DaoGui():
    """
    This class creates the interface for the actual dao board
    This controls how the user interacts with and plays the game
    """

    # initialze stuff for the gui
    def __init__(self, dao_app : DaoApp):
        # reference to the parent dao app object
        self.app = dao_app

        # initialize constants and things for the interface
        self.window_width = 1200            # width of the application window
        self.window_height = 1000           # height of the application window
        self.board_edge = 70                # size of the gap around tiles in the game
        self.tile_gap = 5                   # the gap between tiles on the board
        self.window_color = "#b88756"       # color of window everything is on #5c2f02
        self.bg_color = "#021c04"           # color of the canvas behind the game board
        self.tile_color_0 = "#ba653d"       # color of half the game board tiles
        self.tile_color_1 = "#deaf99"       # color of half the game board tiles
        self.legal_tile_color = "red"       # color of tiles that are legal moves
        self.tile_size = 100                # width and height of a tile on the game board
        self.legal_tile_size = 96           # width and height of the legal move highlight for tiles
        self.button_width = 10              # width for buttons on the interface
        self.button_height = 2              # height for buttons on the interface
        self.interface_pad = 25             # padding for interface objects
        self.button_font = 'times'          # font for button text
        self.button_text_size = 18          # size for button text
        self.message_font = 'times'         # font for message text
        self.message_text_size = 14         # size for button text
        self.piece_radius = 40              # the radius of a dao piece

        # calculate how large the canvas for the board needs to be based on the size of the game elements
        self.board_size = self.board_edge * 2 + self.tile_size * 4 + self.tile_gap * 3

        # mapping dictionaries
        self.tile_positions = {             # maps dao board locations to coordinates on the canvas (center of tile locations)
            (0,0) : (self.board_edge + self.tile_size * 0.5 + self.tile_gap * 0, self.board_edge + self.tile_size * 0.5 + self.tile_gap * 0),
            (0,1) : (self.board_edge + self.tile_size * 0.5 + self.tile_gap * 0, self.board_edge + self.tile_size * 1.5 + self.tile_gap * 1),
            (0,2) : (self.board_edge + self.tile_size * 0.5 + self.tile_gap * 0, self.board_edge + self.tile_size * 2.5 + self.tile_gap * 2),
            (0,3) : (self.board_edge + self.tile_size * 0.5 + self.tile_gap * 0, self.board_edge + self.tile_size * 3.5 + self.tile_gap * 3),
            (1,0) : (self.board_edge + self.tile_size * 1.5 + self.tile_gap * 1, self.board_edge + self.tile_size * 0.5 + self.tile_gap * 0),
            (1,1) : (self.board_edge + self.tile_size * 1.5 + self.tile_gap * 1, self.board_edge + self.tile_size * 1.5 + self.tile_gap * 1),
            (1,2) : (self.board_edge + self.tile_size * 1.5 + self.tile_gap * 1, self.board_edge + self.tile_size * 2.5 + self.tile_gap * 2),
            (1,3) : (self.board_edge + self.tile_size * 1.5 + self.tile_gap * 1, self.board_edge + self.tile_size * 3.5 + self.tile_gap * 3),
            (2,0) : (self.board_edge + self.tile_size * 2.5 + self.tile_gap * 2, self.board_edge + self.tile_size * 0.5 + self.tile_gap * 0),
            (2,1) : (self.board_edge + self.tile_size * 2.5 + self.tile_gap * 2, self.board_edge + self.tile_size * 1.5 + self.tile_gap * 1),
            (2,2) : (self.board_edge + self.tile_size * 2.5 + self.tile_gap * 2, self.board_edge + self.tile_size * 2.5 + self.tile_gap * 2),
            (2,3) : (self.board_edge + self.tile_size * 2.5 + self.tile_gap * 2, self.board_edge + self.tile_size * 3.5 + self.tile_gap * 3),
            (3,0) : (self.board_edge + self.tile_size * 3.5 + self.tile_gap * 3, self.board_edge + self.tile_size * 0.5 + self.tile_gap * 0),
            (3,1) : (self.board_edge + self.tile_size * 3.5 + self.tile_gap * 3, self.board_edge + self.tile_size * 1.5 + self.tile_gap * 1),
            (3,2) : (self.board_edge + self.tile_size * 3.5 + self.tile_gap * 3, self.board_edge + self.tile_size * 2.5 + self.tile_gap * 2),
            (3,3) : (self.board_edge + self.tile_size * 3.5 + self.tile_gap * 3, self.board_edge + self.tile_size * 3.5 + self.tile_gap * 3)
        }
        self.game_pieces_map = {}           # maps the pieces drawn on the board to piece objects within the dao game
        self.game_drawn_pieces_map = {}     # maps the logical pieces from a dao game to the pieces drawn on the canvas
        self.game_tile_map = {}             # maps the tiles drawn on the board to board positions of the dao game

        # create the main window object
        self.main_window = Tk(screenName="Dao", baseName="Dao", className="Dao")
        self.main_window.config(width=self.window_width, height=self.window_height, bg=self.window_color)

        # create all the widgets that the user can interact with
        self.game_canvas = Canvas(self.main_window, bg=self.bg_color, height=self.board_size, width=self.board_size)
        self.interface = Frame(self.main_window, bg=self.window_color, width=350, height=self.board_size)    # this will contain all the buttons and things 
        self.interface.pack_propagate(False)        # disable the frame changing size with internal widgets
        self.draw_button = Button(self.interface, text="Offer Draw", width=self.button_width, height=self.button_height)
        self.draw_button.config(font=(self.button_font, self.button_text_size))
        self.resign_button = Button(self.interface, text="Resign", width=self.button_width, height=self.button_height)
        self.resign_button.config(font=(self.button_font, self.button_text_size))
        self.notification_text = Message(self.interface, text="Here is some really long text to see how the text thing works and if it is too big", width=350, bg=self.window_color)
        self.notification_text.config(font=(self.message_font, self.message_text_size))
        self.player_turn_text = Message(self.interface, text="Player 0", width=350, bg=self.window_color)
        self.player_turn_text.config(font=(self.message_font, self.message_text_size))
        self.player_text = Frame(self.interface, bg=self.window_color)
        self.player_0_text = Message(self.player_text, text="Player 0", width=300, bg=self.window_color)
        self.player_0_text.config(font=(self.message_font, self.message_text_size + 6, 'bold'))
        self.player_vs_text = Message(self.player_text, text="v.s.", width=200, bg=self.window_color)
        self.player_vs_text.config(font=(self.message_font, self.message_text_size + 6, 'bold'))
        self.player_1_text = Message(self.player_text, text="Player 1", width=300, bg=self.window_color)
        self.player_1_text.config(font=(self.message_font, self.message_text_size + 6, 'bold'))

        # position the widgets in the window
        # TODO:  Fiddle with this to make the user interface look nicer
        self.game_canvas.pack(side='right')
        self.player_0_text.pack(side='top', pady=self.interface_pad/4)
        self.player_vs_text.pack(pady=self.interface_pad/4)
        self.player_1_text.pack(side='bottom', pady=self.interface_pad/4)
        self.player_text.pack(side='top', pady=self.interface_pad)
        self.draw_button.pack(side='top', pady=self.interface_pad/2)
        self.resign_button.pack(pady=self.interface_pad/2)
        self.notification_text.pack(side='bottom', pady=self.interface_pad/2)
        self.player_turn_text.pack(side='bottom', pady=self.interface_pad)
        self.interface.pack(side='left', padx=self.interface_pad*2, expand=False, fill='both')

        # link events to widgets
        self.game_canvas.bind('<Motion>', self.update_game_board)
        self.game_canvas.bind('<ButtonPress-1>', self.select_piece_at_cursor)
        self.game_canvas.bind('<ButtonRelease-1>', self.drop_piece_at_cursor)

        # set the names of the players playing
        self.update_player_names()
        self.update_player_turn_text()

        # draw the dao board tiles on the canvas
        self.board_tiles = []
        self.highlighted_tiles = []
        self.draw_dao_board()

        # setup the initial positions of the dao pieces on the canvas
        self.game_pieces = []
        self.draw_game_pieces()
        self.selected_piece = None
        self.selected_offset_pos = None

        # display the gui on the screen
        self.main_window.mainloop()


    # function to handle any updates needed on the canvas (triggered by mouse motion)
    def update_game_board(self, event : EventType.Motion):
        # if there is a selected piece, move it to the cursor position
        if self.selected_piece != None:
            self.move_piece_to_cursor(self.selected_piece, event)
        pass


    # function to adjust the names of the players on the gui
    def update_player_names(self):
        # get the names of the players in the game
        player_0_name = self.app.dao_game.player_0.name
        player_1_name = self.app.dao_game.player_1.name
        # get the colors of the players in the game
        player_0_color = self.app.dao_game.player_0.color
        player_1_color = self.app.dao_game.player_1.color
        # set the text on the gui to the names and colors of the players
        #self.player_0_text.config(text=player_0_name, highlightthickness=4, highlightcolor=player_0_color)
        #self.player_1_text.config(text=player_1_name, highlightthickness=4, highlightcolor=player_1_color)
        self.player_0_text.config(text=player_0_name, highlightthickness=2, highlightbackground=player_0_color)
        self.player_1_text.config(text=player_1_name, highlightthickness=2, highlightbackground=player_1_color)


    # function to draw a dao board on the canvas
    def draw_dao_board(self):
        # iterate through every board position
        for x in range(4):
            for y in range(4):
                # determine where to draw the tile
                center_coords = self.tile_positions[(x, y)]
                corner_0_coords = center_coords[0] - self.tile_size * 0.5, center_coords[1] - self.tile_size * 0.5
                corner_1_coords = center_coords[0] + self.tile_size * 0.5, center_coords[1] + self.tile_size * 0.5
                # alternate the colors of the tile
                if (x + y) % 2 == 0:
                    color = self.tile_color_0
                else:
                    color = self.tile_color_1
                # draw the tile onto the canvas
                tile = self.game_canvas.create_rectangle(corner_0_coords, corner_1_coords, fill=color, outline=color)
                self.board_tiles.append(tile)
                self.game_tile_map[tile] = (x,y)


    # function to draw the game pieces onto the canvas
    def draw_game_pieces(self):
        pieces = self.app.dao_game.get_dao_pieces()
        # create pieces
        for piece in pieces:
            # draw a piece on the board
            init_x = 100
            init_y = 100
            oval_coords = init_x - self.piece_radius, init_y - self.piece_radius, init_x + self.piece_radius, init_y + self.piece_radius
            drawn_piece = self.game_canvas.create_oval(oval_coords, fill=piece.color, outline='#303030', width=1)
            # move the piece to the right tile to match it's position in the dao game
            self.adjust_piece_position(drawn_piece, piece.position)
            # map the drawn piece to the piece in the dao game
            self.game_pieces.append(drawn_piece)
            self.game_pieces_map[drawn_piece] = piece
            self.game_drawn_pieces_map[piece] = drawn_piece


    # function to put a piece onto a specific tile
    def adjust_piece_position(self, drawn_piece, board_pos):
        # get the coordinates of the tile from the board position
        coords = self.tile_positions[board_pos]
        # move the piece, adjusting for left corner placement
        self.game_canvas.moveto(drawn_piece, coords[0]-self.piece_radius, coords[1]-self.piece_radius)
        pass


    # function to move a piece to the cursor
    def move_piece_to_cursor(self, drawn_piece, event):
        # move the piece, adjusting for left corner placement
        self.game_canvas.moveto(drawn_piece, event.x-self.selected_offset_pos[0], event.y-self.selected_offset_pos[1])
        self.game_canvas.tag_raise(drawn_piece)
        pass


    # function to select a piece at the mouse cursor position
    def select_piece_at_cursor(self, event : EventType.ButtonPress):
        # TODO: Prevent selecting when it is not the local players turn, + error message
        # see if the cursor is on a piece
        for piece in self.game_pieces:
            # get the coordinates of the piece
            x1, y1, x2, y2 = self.game_canvas.coords(piece)
            center_x = x1 + self.piece_radius
            center_y = y1 + self.piece_radius
            # determine if the cursor is less than a radius away from the center of the piece
            dist = ((center_x - event.x)**2 + (center_y - event.y)**2)**0.5
            if dist <= self.piece_radius:
                # we can pickup this piece! 
                team_turn = self.app.dao_game.active_player.team
                dao_piece = self.game_pieces_map[piece]
                # TODO: implement check on local player so that they cannot pickup the other players piece, + error message
                # check to see if it's this players turn to move this piece
                if team_turn == dao_piece.team:
                    # it is this players turn!  select the piece
                    self.selected_piece = piece
                    self.selected_offset_pos = (event.x-x1, event.y-y1)
                    self.move_piece_to_cursor(piece, event)
                    self.show_legal_moves(piece)
                else:
                    # it is NOT this players turn! Don't allow the piece to be selected
                    self.update_notification_text("Hey mister, that's not your piece!")
                break


    # function to drop a selected piece onto the board and attempt to move it there
    def drop_piece_at_cursor(self, event : EventType.ButtonRelease):
        # ensure we actually have a selected piece, this runs on any button release on the game canvas
        if self.selected_piece != None:
            # determine where we should drop the piece
            target_tile = None
            for tile in self.board_tiles:
                x1, y1, x2, y2 = self.game_canvas.coords(tile)
                # check to see if the mouse cursor is above this tile
                if (event.x > x1) and (event.x < x2) and (event.y > y1) and (event.y < y2):
                    target_tile = tile
                    break
            # if we found a target tile, attempt the same move within the dao game object
            if target_tile != None:
                new_position = self.game_tile_map[target_tile]
                dao_piece = self.game_pieces_map[self.selected_piece]
                move_status, end_status = self.app.dao_game.move_dao_piece(dao_piece, new_position)
                # if the move was valid, update the gui
                if move_status:
                    self.update_player_turn_text()
                    self.generate_good_move_notification()
                    self.adjust_piece_position(self.selected_piece, new_position)
                    # if this move caused the game to end, display the result
                    if end_status:
                        self.report_game_over()
                        pass
                # if the move was not valid, reset the piece to the position it has in the game
                else:
                    old_position = dao_piece.position
                    self.adjust_piece_position(self.selected_piece, old_position)
                    # don't yell at the player if they dropped the piece on the same tile it started on
                    if new_position != old_position:
                        self.update_notification_text("That move isn't allowed")
            # if we didn't find a tile, reset the piece to the position it has in the game
            else:
                dao_piece = self.game_pieces_map[self.selected_piece]
                old_position = dao_piece.position
                self.adjust_piece_position(self.selected_piece, old_position)
                self.update_notification_text("You gotta put the piece on a tile dude!")
                pass
        # unselect the piece
        self.selected_piece = None
        # clear any shown legal moves
        self.hide_legal_moves()
    

    # function to modify the notification text
    def update_notification_text(self, new_text : str):
        # change the notification text to be the new text
        self.notification_text.config(text=new_text)
        pass


    # function to highlight the legal moves a piece has
    def show_legal_moves(self, drawn_piece):
        # get the set of legal moves for the piece
        dao_piece = self.game_pieces_map[drawn_piece]
        legal_moves = self.app.dao_game.find_legal_moves(dao_piece)
        # draw a rectangle at each tile that is a legal move
        for move in legal_moves:
            center_coords = self.tile_positions[move]
            corner_0_coords = center_coords[0] - self.legal_tile_size * 0.5, center_coords[1] - self.legal_tile_size * 0.5
            corner_1_coords = center_coords[0] + self.legal_tile_size * 0.5, center_coords[1] + self.legal_tile_size * 0.5
            highlighted_tile = self.game_canvas.create_rectangle(corner_0_coords, corner_1_coords, outline=self.legal_tile_color, width=6)
            self.highlighted_tiles.append(highlighted_tile)
        

    # function to remove the legal moves
    def hide_legal_moves(self):
        # delete each legal move object from the canvas and the list of highlighted tiles
        for highlight in self.highlighted_tiles:
            self.game_canvas.delete(highlight)
        self.highlighted_tiles = []
        
        
    # function to report the end of the game after a successful move in the notification text
    def report_game_over(self):
        # extract info from the dao game object
        last_log = self.app.dao_game.game_log.event_log[-1]
        player_0 = self.app.dao_game.player_0.name
        player_1 = self.app.dao_game.player_1.name
        result_code = last_log[0]
        method_code = last_log[1]
        # get the name of the winning player
        if result_code == DaoGameEventCode_e.player_0_win:
            winner = player_0
            loser = player_1
        else:
            winner = player_1
            loser = player_0
        # generate a text string based on how the winner won the game
        if method_code == DaoGameEventCode_e.four_in_a_row:
            game_over_text = winner + " played connect 4 and won the game!"
        elif method_code == DaoGameEventCode_e.four_in_a_box:
            game_over_text = winner + " just out boxed " + loser + "!"
        elif method_code == DaoGameEventCode_e.four_in_corners:
            game_over_text = winner + " won by corner camping!"
        elif method_code == DaoGameEventCode_e.trapped_piece:
            game_over_text = loser + " just handed " + winner + " the win by trapping their piece!"
        # update the notification text
        self.update_notification_text(game_over_text)

    

    # function to update the player turn text
    def update_player_turn_text(self):
        # get the name of the player who's turn it is from the game object
        player_name = self.app.dao_game.active_player.name
        player_team = self.app.dao_game.active_player.team
        new_text = "It's " + player_name + "'s turn!"
        # set message text to reflect the current players turn
        self.player_turn_text.config(text=new_text)
        # make current player's name black if it's their turn and fadded out if it's not their turn
        if player_team == 0:
            self.player_0_text.config(fg='black')
            self.player_1_text.config(fg='#303030')
        else:
            self.player_0_text.config(fg='#303030')
            self.player_1_text.config(fg='black')


    # this function will update the notification text with a randomly selected string
    def generate_good_move_notification(self):
        good_move_text = [
            "Woah!  What a power move!",
            "Hmmm, are you sure about that one?",
            "Now that's how you move a piece!",
            "Ok, ok, not bad!",
            "Look at you go!",
            "You've got 'em on the ropes!",
            "Oh no....",
            "Dude, you're crushing this!",
            "Huh!?  How is that even a legal move!?",
            "POGGERS",
            "What is this, Hot Soup?",
            "That was fantastic!",
            "Wait, the game's still going?",
            "<Insert Funny Joke Here>",
            "Another day, another move",
            "Hahahahhahahahaha!",
            "Dude, that was INSANE!",
            "I need to see that one in slow-mo!",
            "Ref?  Is that cheating?",
            "Pi pi pi pi pi!",
            "You activated my trap card!",
            "Heh",
            "Nice!  That was a good move!",
            "Really?  You went there?",
            "Are you even trying to win?",
            "You came, you saw, you moved a Dao piece",
            "I like that one!",
            "You actually moved there AGAIN?!?!?",
            "That move's a doozy"
        ]
        # choose a random thing to say
        move_text = good_move_text[random.randint(0, len(good_move_text)-1)]
        # say the thing
        self.update_notification_text(move_text)




















