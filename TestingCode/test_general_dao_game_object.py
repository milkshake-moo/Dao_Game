
"""
This file exists to test the DaoGameObject python class.

These tests look at the object itself and do not try to instantiate or do anything weird with them
"""



import sys
# set sys path to allow imports from the parent directory
sys.path.append('../Dao_Game')

# imports dimports
from Backbone.DaoGameObject import DaoGameObject as dgo
from Backbone.DaoGameObject import DaoPlayer as dp
from Backbone.DaoGameObject import DaoGameLog as dgl








# TESTING FUNCTIONS


# prints the id and position of each dao piece in a game object
def test_print_dao_piece_info(game : dgo):
    print("\n")
    print("Dao Piece status:")
    pieces = game.get_dao_pieces()
    for piece in pieces:
        print(piece.id, ":  position:", piece.position, " team:",piece.team, " color:", piece.color)



# prints the id of each dao piece from the game in a formatted way
def test_print_ascii_board(game : dgo):
    print("/n/n")
    print("Displaying Dao Game State...")
    empty = "   "
    
    # these are all the ascii tiles on a dao board
    # they are in a dictionary so that we can look up a specific space using the coordinates
    tile_dict = {
        (0, 0): empty, (1, 0): empty, (2, 0): empty, (3, 0): empty,
        (0, 1): empty, (1, 1): empty, (2, 1): empty, (3, 1): empty,
        (0, 2): empty, (1, 2): empty, (2, 2): empty, (3, 2): empty,
        (0, 3): empty, (1, 3): empty, (2, 3): empty, (3, 3): empty,
    }

    # here we add the ID of each piece to the tile dictionary to represent each piece
    for piece in game.get_dao_pieces():
        tile_dict[piece.position] = piece.id
    
    # now we need to print everything
    # each piece should be represented by it's id on this ascii board
    print("="*17)
    print("|"+tile_dict[(0,0)]+"|"+tile_dict[(1,0)]+"|"+tile_dict[(2,0)]+"|"+tile_dict[(3,0)]+"|")
    print("="*17)
    print("|"+tile_dict[(0,1)]+"|"+tile_dict[(1,1)]+"|"+tile_dict[(2,1)]+"|"+tile_dict[(3,1)]+"|")
    print("="*17)
    print("|"+tile_dict[(0,2)]+"|"+tile_dict[(1,2)]+"|"+tile_dict[(2,2)]+"|"+tile_dict[(3,2)]+"|")
    print("="*17)
    print("|"+tile_dict[(0,3)]+"|"+tile_dict[(1,3)]+"|"+tile_dict[(2,3)]+"|"+tile_dict[(3,3)]+"|")
    print("="*17)
    



# this test function will create a visual aid of the dao game using an ascii representation
# this can be used to manually move pieces around from any game state
def run_ascii_debugger(game : dgo):
        move_status = False
        end_status = False
        # Run a debug ascii gui to represent the game
        while True:
            # display the ascii board
            test_print_ascii_board(game)
            # display the event log
            print("\nGame Event Log:")
            print(game.game_log.event_log)
            # display the last move statuses
            print(f"\nMove Status: {move_status}, End Status: {end_status}")

            # exit the loop if the game has ended
            if end_status:
                break

            # get input and attempt to move a dao piece
            piece_id = input("\nSelect a piece to move: ")
            new_pos = input("Enter a new position (seperate x and y with a space): ").split()
            position = (int(new_pos[0]), int(new_pos[1]))
            pieces = game.get_dao_pieces()
            selected = None
            for p in pieces:
                if p.id == piece_id:
                    selected = p
            move_status, end_status = game.move_dao_piece(selected, position)





# main method for testing dao game related things
def main():
    print("\nTesting Dao Game Object Creation")
    # create two player objects
    player_1 = dp("donny", "black")
    player_2 = dp("MilkShakeMoo", "white")

    # create a Dao game object
    game = dgo(player_1, player_2)
    print("DaoGameObject created")

    # list the starting piece setup
    pieces = game.get_dao_pieces()
    test_print_dao_piece_info(game)
    print("\n\n")

    # configure the locations of the pieces within the game to a preset value
    print("Loading Test postion 1...")
    game.pieces_0[0].position = (0,0)
    game.pieces_0[1].position = (1,1)
    game.pieces_0[2].position = (1,0)
    game.pieces_0[3].position = (0,2)
    game.pieces_1[0].position = (3,0)
    game.pieces_1[1].position = (3,1)
    game.pieces_1[2].position = (3,2)
    game.pieces_1[3].position = (2,3)
    print("Test position 1 loaded: ")
    #run_ascii_debugger(game)

    # configure the locations of the pieces within the game to a preset value
    print("Loading Test postion 1...")
    game.pieces_0[0].position = (3,3)
    game.pieces_0[1].position = (1,1)
    game.pieces_0[2].position = (1,0)
    game.pieces_0[3].position = (0,2)
    game.pieces_1[0].position = (0,0)
    game.pieces_1[1].position = (3,1)
    game.pieces_1[2].position = (3,2)
    game.pieces_1[3].position = (2,3)
    print("Test position 1 loaded: ")
    run_ascii_debugger(game)

    pass


if __name__ == "__main__":
    main()




