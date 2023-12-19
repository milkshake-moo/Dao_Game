
"""
This file contains the code used to represent a DaoGame Object
A DaoGame Object will keep track of a game of Dao and all related info
This includes:
    - Dao board state / where pieces are
    - Players and their colors
    - Player turn
    - Checking for win conditions
    - A game log 
    - Functions to alter the game state that can be called from a parent object
    - Any other game meta data that we want to add (special positions, etc)

This file also contains other objects related to organizing information involved in a Dao Game

Notable behavior:
    - Position (0,0) is the top left square of the dao board
    - Dao Pieces are identified by the player number and the piece number
        - ex: '0_2' refers to player 0 and piece number 2
    - A game log is a byte array of game information
        - Dao log version
        - player 0 info
        - player 1 info
        - A list of game events
        - A game result
"""


import sys
# set sys path to allow imports from the parent directory
sys.path.append('../Dao_Game')

# general import stuffs
from enum import IntEnum




# Dao Game Event Codes class
class DaoGameEventCode_e(IntEnum):
    """
    This class translates various events into a 2 byte code
    This will be used to log things that happen during a Dao Game
    Some of these event codes may currently be unnused or unimplemented
    """
    # invalid event
    invalid                 = 0x0000

    # legal move
    legal_move              = 0x1001
    
    # offer draw events
    player_0_offer_draw     = 0x0100
    player_1_offer_draw     = 0x0101

    # connection events
    player_0_disconnect     = 0x0200
    player_1_disconnect     = 0x0201
    player_0_reconnect      = 0x0202
    player_1_reconnect      = 0x0203

    # game ending events
    player_0_win            = 0x0300
    player_1_win            = 0x0301
    draw_accepted           = 0x0302
    inconclusive_game       = 0x0303

    # victory types
    four_in_a_row           = 0x0400
    four_in_a_box           = 0x0401
    four_in_corners         = 0x0402
    trapped_piece           = 0x0403
    conceede                = 0x0404




# Dao Piece class
class DaoPiece():
    """
    A Dao Piece stores all info to identify itself within a Dao Game
    """

    # configure initial values of the Dao piece
    def __init__(self, piece_num : int, team_num : int, color : str, position : tuple):
        self.color = color          # identifies what color this piece is
        self.team = team_num        # identifies what team this piece belongs to (0 or 1)
        self.position = position    # identifies the x, y coordinates of the piece on the board
        self.id = str(team_num) + "_" + str(piece_num) # identifies this specific Dao piece

    # move the Dao Piece to a different position, this does not do any legal move checking
    def move(self, new_position : tuple):
        self.position = new_position


# Dao Player class
class DaoPlayer():
    """
    A Dao Player stores all info related to a player in a Dao game
    This could later be expanded to store player meta data, a bet or wager, win streak, etc.
    """

    # initialization function for a DaoPlayer
    def __init__(self, player_name : str, player_color : str, player_team : int =0):
        self.name = player_name     # name of this player
        self.color = player_color   # color of this players pieces
        self.team = player_team     # a number (0 or 1) to refer to which team this player is on




class DaoGameLog():
    """
    This class stores information about a dao game for future review
    TODO:  Implement conversion to and from an array of bytes
    TODO:  Implement Restoring / running a game object using a log (without a result)
    TODO:  Implement saving a log to a file and loading a log from a file
    """
    # This identifies the format and info the game log uses from potential (but unlikely) future versions
    DAOGAMELOG_VERSION = 1
    # This delimiter will seperate certain parts of log entries in byte form so they can be parsed later
    DAOGAMELOG_DELIMITER = '*.'

    # initialization function for a DaoGameLog
    def __init__(self, player_0 : DaoPlayer = None, player_1 : DaoPlayer = None):
        self.player_0 = player_0
        self.player_1 = player_1
        self.event_log = []         # stores a list of events and any assosiated data
        self.game_log_bytes = bytearray()
    
    
    # This function adds a legal move to the log
    def log_move(self, piece : DaoPiece):
        self.event_log.append((DaoGameEventCode_e.legal_move, piece.id, piece.position))
    
    
    # This function logs a standalone event with no associated data
    def log_event(self, event : DaoGameEventCode_e):
        self.event_log.append((event))


    # This function logs the result of a dao game
    def log_result(self, result : DaoGameEventCode_e, victory_by : DaoGameEventCode_e = None):
        self.event_log.append((result, victory_by))

    
    # This function converts the game information into byte form
    def get_log_bytes(self):
        # Add log version
        # Add player 0 info
        # Add player 1 info
        # Add series of game events
        pass

    
    # This function creates a DaoGameLog object from a set of byte stream
    def build_log_from_bytes(self, log_bytes : bytes):
        # Extract log version / compare to self version, fail if not same
        # Extract player 0 info
        # Extract player 1 info
        # Extract series of game events
        # Extract game result
        pass






# Dao Game Object class
class DaoGameObject():
    """
    This object tracks the state of a dao game and stores any related information
    This is the object that checks move legality, for win conditions, and tracks player turns
    """

    # initialization function for the DaoGameFunction
    def __init__(self, player_0 : DaoPlayer, player_1 : DaoPlayer):
        # store and initialze the player objects
        self.player_0 = player_0
        self.player_0.team = 0
        self.player_1 = player_1
        self.player_1.team = 1
        # create the sets of Dao pieces for each player
        self.pieces_0, self.pieces_1 = self.build_board()
        # initialze other variables
        self.active_player = player_0   # this tracks who's turn it is / who's allowed to move
        self.pending_draw_request = None # this var stores a player who is actively requesting a draw
        self.game_over = False          # this var tracks whether or not the game is over
        self.game_log = DaoGameLog(self.player_0, self.player_1)


    # function to build a set of Dao pieces for each player in the game
    def build_board(self):
        pieces_0 = []
        pieces_1 = []
        # set up the pieces for player_0, team 0
        pieces_0.append(DaoPiece(0, 0, self.player_0.color, (0,0)))
        pieces_0.append(DaoPiece(1, 0, self.player_0.color, (1,1)))
        pieces_0.append(DaoPiece(2, 0, self.player_0.color, (2,2)))
        pieces_0.append(DaoPiece(3, 0, self.player_0.color, (3,3)))
        # set up the pieces for player_1, team 1
        pieces_1.append(DaoPiece(0, 1, self.player_1.color, (3,0)))
        pieces_1.append(DaoPiece(1, 1, self.player_1.color, (2,1)))
        pieces_1.append(DaoPiece(2, 1, self.player_1.color, (1,2)))
        pieces_1.append(DaoPiece(3, 1, self.player_1.color, (0,3)))
        # return the arrays of pieces
        return pieces_0, pieces_1


    # function to return a list of all dao pieces in the game
    def get_dao_pieces(self):
        dao_pieces = []
        for piece in self.pieces_0:
            dao_pieces.append(piece)
        for piece in self.pieces_1:
            dao_pieces.append(piece)
        return dao_pieces
    
    
    # function to handle requesting a draw
    def request_draw(self, player : DaoPlayer):
        # the player provided to this func is requesting a draw

        # if there is a pending draw request from the other player already, accept the draw request, ending the game
        if (self.pending_draw_request != None) and (player != self.pending_draw_request):
            self.game_over = True
            # log that a draw caused the game to conclude
            self.game_log.log_event(DaoGameEventCode_e.draw_accepted)
        else:
            # either the same player requested a draw or there wasn't a pending draw request
            # store this request in the game state and log the event
            self.pending_draw_request = player
            if player == self.player_0:
                self.game_log.log_event(DaoGameEventCode_e.player_0_offer_draw)
            else:
                self.game_log.log_event(DaoGameEventCode_e.player_1_offer_draw)


    # function to handle conceeding a game
    def conceede_game(self, player : DaoPlayer):
        # the player in the arguments is conceeding the game
        self.game_over = True
        # record that the other player won the game because of the concession
        if player == self.player_0:
            self.game_log.log_result(DaoGameEventCode_e.player_1_win, DaoGameEventCode_e.conceede)
        else:
            self.game_log.log_result(DaoGameEventCode_e.player_0_win, DaoGameEventCode_e.conceede)


    # function to abruptly end the game without declaring a winner
    def end_game_abruptly(self):
        self.game_over = True
        self.game_log.log_event(DaoGameEventCode_e.inconclusive_game)


    # function to move a dao piece on the board
    def move_dao_piece(self, piece : DaoPiece, new_position : tuple):
        movement_status = True

        # check who's turn it is and that the piece is allowed to move
        if piece.team != self.active_player.team:
            movement_status = False
        
        # check if move is legal
        if movement_status:
            # the new position must exist within the set of legal moves to be allowed
            legal_moves = self.find_legal_moves(piece)
            movement_status = False
            for move in legal_moves:
                if move == new_position:
                    movement_status = True
                    break
        
        # actually move the piece to the new position
        if movement_status:
            piece.position = new_position
            # add this to the game log
            self.game_log.log_move(piece)
            # if there is a pending draw request, cancel it if the opposing player just made a move
            if (self.pending_draw_request != None) and (self.pending_draw_request.team != piece.team):
                self.pending_draw_request = None
        else:
            # the move wasn't leagal, no need to do other checks
            # return status: no piece moved, the game has not ended
            return False, False

        # check if this move ends the game
        end_of_game, winning_player, victory_method = self.check_for_victory(piece)
        if end_of_game:
            self.game_over = True
            # log the result of the game
            self.game_log.log_result(winning_player, victory_method)
            # return status: a piece moved, and it caused the end of the game
            return True, True
            
        # increment player turn 
        if self.active_player == self.player_0:
            self.active_player = self.player_1
        else:
            self.active_player = self.player_0
        
        # return status: a piece moved, but the game hasn't ended yet
        return True, False

    
    # function that returns an array of positions a piece can legally move to
    def find_legal_moves(self, piece : DaoPiece):
        legal_moves = []
        x_pos = piece.position[0]
        y_pos = piece.position[1]

        # create an array of all existing piece positions
        obstructed_positions = []
        for p in (self.pieces_0, self.pieces_1):
            for i in p:
            # add the position of any piece except the piece we're trying to move
                if i.id != piece.id:
                    obstructed_positions.append(i.position)
        
        # Look for any legal moves along each of the 8 possible vectors the piece can move along
        # (_x,-y) check the UP direction
        new_position = self.find_legal_movement_along_vector((x_pos, y_pos), (0, -1), obstructed_positions)
        if new_position != None:
            legal_moves.append(new_position)
        # (+x,-y) check the UP-RIGHT direction
        new_position = self.find_legal_movement_along_vector((x_pos, y_pos), (1, -1), obstructed_positions)
        if new_position != None:
            legal_moves.append(new_position)
        # (+x,_y) check the RIGHT direction
        new_position = self.find_legal_movement_along_vector((x_pos, y_pos), (1, 0), obstructed_positions)
        if new_position != None:
            legal_moves.append(new_position)
        # (+x,+y) check the DOWN-RIGHT direction
        new_position = self.find_legal_movement_along_vector((x_pos, y_pos), (1, 1), obstructed_positions)
        if new_position != None:
            legal_moves.append(new_position)
        # (_x,+y) check the DOWN direction
        new_position = self.find_legal_movement_along_vector((x_pos, y_pos), (0, 1), obstructed_positions)
        if new_position != None:
            legal_moves.append(new_position)
        # (-x,+y) check the DOWN-LEFT direction
        new_position = self.find_legal_movement_along_vector((x_pos, y_pos), (-1, 1), obstructed_positions)
        if new_position != None:
            legal_moves.append(new_position)
        # (-x,_y) check the LEFT direction
        new_position = self.find_legal_movement_along_vector((x_pos, y_pos), (-1, 0), obstructed_positions)
        if new_position != None:
            legal_moves.append(new_position)
        # (-x,-y) check the UP-LEFT direction
        new_position = self.find_legal_movement_along_vector((x_pos, y_pos), (-1, -1), obstructed_positions)
        if new_position != None:
            legal_moves.append(new_position)

        # return the list of legal moves for the selected piece
        return legal_moves
    

    # a helper function that returns a legal position along a movement vector
    def find_legal_movement_along_vector(self, position : tuple, vector : tuple, obstructed_positions : list):
        delta_x = vector[0]
        delta_y = vector[1]
        valid_position = None
        can_continue_moving = True
        # start by checking the first positon along the movement vector
        x = position[0] + delta_x
        y = position[1] + delta_y

        # continue searching along the vector as long as it is still within the Dao Grid
        while ((x<=3) and (x>=0) and (y<=3) and (y>=0)):
            # check to see if another piece is already in this new position
            for obstruction in obstructed_positions:
                if (x, y) == obstruction:
                    # another piece is already here, we can move no further along this vector
                    can_continue_moving = False
                    break   # exit for loop
            
            # see if we ran into something or if the next position was empty
            if can_continue_moving:
                # The new position is ok to move to / through
                valid_position = (x, y)
            else:
                # there is a piece obstructing any further movement
                break   # exit while loop

            # increment the new position along the vector for the next check
            x = x + delta_x
            y = y + delta_y
        
        # return the valid position along this vector (returns 'None' if there was no movement in this direction)
        return valid_position
        


    # check to see if the new position of a given piece causes the game to end
    def check_for_victory(self, piece : DaoPiece):
        end_of_game = False
        winning_player = None
        victory_method = None

        # determine who would win if the game ends
        if self.active_player.team == 0:
            active_player_win = DaoGameEventCode_e.player_0_win
            other_player_win = DaoGameEventCode_e.player_1_win
        else:
            active_player_win = DaoGameEventCode_e.player_1_win
            other_player_win = DaoGameEventCode_e.player_0_win
        
        # check for a four in a row victory
        if self.check_four_in_row_victory(piece):
            end_of_game = True
            winning_player = active_player_win
            victory_method = DaoGameEventCode_e.four_in_a_row

        # look for four corners victory
        if self.check_four_corners_victory(piece):
            end_of_game = True
            winning_player = active_player_win
            victory_method = DaoGameEventCode_e.four_in_corners

        # look for a box victory
        if self.check_box_victory(piece):
            end_of_game = True
            winning_player = active_player_win
            victory_method = DaoGameEventCode_e.four_in_a_box

        # make sure pieces on the opposite team are not trapped
        if self.check_trapped_victory(piece):
            end_of_game = True
            winning_player = other_player_win
            victory_method = DaoGameEventCode_e.trapped_piece

        # return positive victory status and a victory method if applicable
        return end_of_game, winning_player, victory_method



    # look for 4 in a row victory
    def check_four_in_row_victory(self, piece : DaoPiece):
        if piece.team == 0:
            team_pieces = self.pieces_0
        else:
            team_pieces = self.pieces_1
        
        # check to see if all pieces have the same x or the same y value
        v_line_count = 0
        h_line_count = 0
        for p in team_pieces:
            # check for a horizontal line
            if p.position[1] == piece.position[1]:
                h_line_count = h_line_count + 1
            # check for a vertical line
            if p.position[0] == piece.position[0]:
                v_line_count = v_line_count + 1
        
        # if all the pieces are in a line, that's a win!
        if (v_line_count == 4) or (h_line_count == 4):
            return True


    # look for 4 corners victory for the selected piece
    def check_four_corners_victory(self, piece : DaoPiece):
        victory_status = True
        if piece.team == 0:
            team_pieces = self.pieces_0
        else:
            team_pieces = self.pieces_1
        
        # The player needs a piece in each of these positions in order to win by 4 corners
        winning_position = [(0, 0), (3, 0), (0, 3), (3, 3)]

        # go through each piece and see if it is in one of the winning positions
        for p in team_pieces:
            valid = False
            for i in winning_position:
                # if the piece is in a winning position, it is valid for 4 corners
                if p.position == i:
                    valid = True
                    winning_position.remove(i) # no reason to re-check a position already occupied by another piece
                    break
            # if the piece was not in a winning position, the player did not get a 4 corners victory
            if not valid:
                victory_status = False
                break
        
        # return the victory status
        return victory_status
            

    # look for a box victory for the selected piece
    def check_box_victory(self, piece : DaoPiece):
        if piece.team == 0:
            team_pieces = self.pieces_0
        else:
            team_pieces = self.pieces_1

        # There are four orientations the box can be in relative to the selected piece
        # the sets of winning positions will be relative to that position
        # (delta sets have relative coords with the selected piece as 0,0 going clockwise around a valid box positon)   
        # (there is one delta set for each possible position of the selected piece in a winning box position)
        pos = piece.position
        # TOP RIGHT CORNER
        delta_pos_0 = [(0, 0), (0, 1), (-1, 1), (-1, 0)]
        # BOT RIGHT CORNER
        delta_pos_1 = [(0, 0), (-1, 0), (-1, -1), (0, -1)]
        # BOT LEFT CORNER
        delta_pos_2 = [(0, 0), (0, -1), (1, -1), (1, 0)]
        # TOP LEFT CORNER
        delta_pos_3 = [(0, 0), (1, 0), (1, 1), (0, 1)]

        # calculate the actual winning position values for each of these relative positon sets
        for delta_pos in (delta_pos_0, delta_pos_1, delta_pos_2, delta_pos_3):
            winning_position = [(delta_pos[0][0] + pos[0], delta_pos[0][1] + pos[1]), 
                                (delta_pos[1][0] + pos[0], delta_pos[1][1] + pos[1]), 
                                (delta_pos[2][0] + pos[0], delta_pos[2][1] + pos[1]), 
                                (delta_pos[3][0] + pos[0], delta_pos[3][1] + pos[1])]
            victory_status = True

            # for a player to win via box victory, all of their pieces must match a winnging position
            for p in team_pieces:
                valid = False
                for i in winning_position:
                    # if the piece matches part of a winning position, then it is valid
                    if p.position == i:
                        valid = True
                        winning_position.remove(i) # no reason to re-check a position already occupied by another piece
                        break
                # if this piece was not valid, this set of winning positions won't work
                if not valid:
                    victory_status = False
                    break

            # check to see if all the pieces matched the winning position
            if victory_status:
                # the player won a box victory!
                return True
        
        # if none of the winning positions were valid, we will return False
        return False

            
        
    # this function will check for a trapped victory
    def check_trapped_victory(self, piece :DaoPiece):
        trapped_victory = False
        if piece.team == 0:
            team_pieces = self.pieces_0
            opp_team_pieces = self.pieces_1
        else:
            team_pieces = self.pieces_1
            opp_team_pieces = self.pieces_0
        # the provided piece has just successfully moved
        # if any pieces on the opposing team are boxed into a corner because of this, they win
        
        # determine what corner to check
        x = piece.position[0]
        y = piece.position[1]
        # TOP RIGHT CORNER
        if (x>=2) and (y<=1):
            corner = (3, 0)
            trap_pos = [(2, 0), (2, 1), (3, 1)]
        # BOT RIGHT CORNER
        elif (x>=2) and (y>=2):
            corner = (3, 3)
            trap_pos = [(3, 2), (2, 2), (2, 3)]
        # BOT LEFT CORNER
        elif (x<=1) and (y>=2):
            corner = (0,3)
            trap_pos = [(0, 2), (1, 2), (1, 3)]
        # TOP LEFT CORNER
        elif (x<=1) and (y<=1):
            corner = (0,0)
            trap_pos = [(1, 0), (1, 1), (0, 1)]

        # if there is an opposing piece in that corner we need to check for a trapped victory
        at_risk = False
        for p in opp_team_pieces:
            if p.position == corner:
                at_risk = True
                break
        
        # if we are at risk, see if our pieces occupy all of the spaces adjacent to the corner
        adjacent_pieces = 0
        if at_risk:
            for p in team_pieces:
                for i in trap_pos:
                    # determine if the piece is adjacent to the opposing piece in the corner
                    if p.position == i:
                        adjacent_pieces = adjacent_pieces + 1
                        trap_pos.remove(i) # no reason to re-check a position already occupied by another piece
                        break
            # if there were 3 adjacent pieces, we have triggered a trap victory for the opponent
            if adjacent_pieces == 3:
                trapped_victory = True
        
        # return the trapped victory status
        return trapped_victory















