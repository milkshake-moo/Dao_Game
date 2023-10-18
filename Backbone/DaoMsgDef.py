
"""
This file contains the message definitions for the way in which two Dao programs
will interact with each other.

This is desinged to be modular so that new messages can be easily added or old
messages modified

Everything defined in this file should be heavily commented, that way this can also
serve as a form of documentation or used for reference later

NOTE:  Many of the payloads of these messages are not yet defined.  The way Dao game
information is stored and tracked has not yet been defined.  These placeholders
should be replaced once these have been defined


Message structure:
===============================================================================
| 4 bytes msg_code | 4 bytes payload_length | payload_length bytes of payload |
===============================================================================
    - msg_code:  Identifies the message and the intent
    - payload_length:  tells us how much payload data to expect (some messages may need a variable amount)
    - payload:  Any extra data that needs to be sent for the msg_code
            - Variables within paylaods will be seperated by a constant delimiter

    
Python sockets send / receive data in byte form. 
NOTE:  current byte conversions feel messy and there may be some room for improvement
"""


# Imported things!
from enum import IntEnum


# constants and configurable values
HEADER_LENGTH = 8                           # This is the length in bytes of a StandardDaoMsg header
PAYLOAD_DELIMITER = "-&&&-".encode()        # These bytes will seperate data in payloads containing multiple variables



# ========================  MSG CODE AND MSG STRUCTURE DEFINITIONS =========================


# Dao Message Codes
class DaoMsgCode_e(IntEnum):
    """
    This enumeration keeps track of what msg_code number is assosiated with what msg
    NOTE:  Current numbers and msg_codes are placeholders and can change
    """
    # invlaid message
    invalid                 = 0x0000

    # requests and responses
    challenge_to_game       = 0x0100
    challenge_response      = 0x0101
    request_draw            = 0x0102
    draw_response           = 0x0103
    resign                  = 0x0104

    # Dao Game event messages
    legal_move              = 0x0200
    end_of_game             = 0x0201
    
    # Not Yet Implemented
    request_game_state      = 0x0300
    game_state              = 0x0301





# class to represent a standard Dao message
class StandardDaoMsg():
    """
    Each Dao Message needs to have three crucial parts:
    - A message code to identify what message it is
    - A payload length to know how long the payload is
    - A payload, this will contain any information the msg needs to deliver
    - This class has functions to convert into a byte string or from a byte string
    (sockets require data in byte form in order to send. They also receive stuff in this form)
    """
    
    # configure initial values for the message object
    def __init__(self):
        self.msg_code = DaoMsgCode_e.invalid
        self.payload_length = 0
        self.header_length = 8  # This value should remain constant
        self.header = None
        self.payload = None


    # configure the message (combines two other functions)
    def configMsg(self, msg_code : DaoMsgCode_e, payload : bytes):
        self.populateHeader(msg_code, len(payload))
        self.addPayload(payload)


    # add a message code and payload length to the the message object
    def populateHeader(self, msg_code : DaoMsgCode_e, payload_length : int):
        # save the msg_code and paylaod_length 
        self.msg_code = msg_code
        self.payload_length = payload_length
        # build and save a set of header bytes out of the same info
        code_bytes = msg_code.to_bytes(4)
        len_bytes = payload_length.to_bytes(4)
        self.header = combineBytes(code_bytes, len_bytes)
    

    # extract and populate the header information from some given bytes
    def extractHeaderFromBytes(self, header_bytes : bytes):
        self.header = header_bytes
        msg_bytes, len_bytes = splitBytes(header_bytes, 4)
        self.msg_code = DaoMsgCode_e(int.from_bytes(msg_bytes))
        self.payload_length = int.from_bytes(len_bytes)
    

    # add the payload (in bytes) to the message oject
    def addPayload(self, payload : bytes):
        self.payload = payload
    

    # get the bytes assosiated with this message
    def getBytes(self):
        # simply return the combined header and payload objects
        raw_bytes = combineBytes(self.header, self.payload)
        return raw_bytes
    

    # populate the fields of the message object from a raw string of bytes
    def buildFromBytes(self, raw_bytes):
        # split the raw bytes into the header and any payload
        header_bytes, payload_bytes = splitBytes(raw_bytes, self.header_length)
        # save the payload 
        self.payload = payload_bytes
        # extract and save the header bytes
        self.extractHeaderFromBytes(header_bytes)





# ========================  HELPER CLASSES AND FUNCTIONS =========================


# this is a placeholder class that holds garbage data
class tempData():
    """
    This class is used to take the place of data we have not yet defined
    This allows us to send / receive some bogus data as a placeholder while testing the transport layer
    """
    temp_int = 0
    temp_char = ''
    temp_string = ""

    # initializing bogus parameters with bogus data
    def __init__(self):
        self.temp_int = 80085
        self.temp_char = 'z'
        self.temp_string = "hi mom"

    # actual structures should have a way of converting into a byte string
    # the way this happens is not important as long as it is reversable
    def getBytes(self):
        raw_bytes = bytearray(4 + 1 + len(self.temp_string))
        int_bytes = self.temp_int.to_bytes(4)
        chr_bytes = self.temp_char.encode()
        str_bytes = self.temp_string.encode()
        raw_bytes[0] = int_bytes[0]
        raw_bytes[1] = int_bytes[1]
        raw_bytes[2] = int_bytes[2]
        raw_bytes[3] = int_bytes[3]
        raw_bytes[4] = chr_bytes[0]
        for i in range(len(str_bytes)):
            raw_bytes[i + 5] = str_bytes[i]
        return raw_bytes
    


# This function takes two byte array objects and combines them into a larger one
def combineBytes(object_1 : bytes, object_2 : bytes):
    combined_bytes = bytearray(len(object_1) + len(object_2))
    # add the bytes from the first array
    combined_bytes[0 : len(object_1)] = object_1[0 :]
    # add the bytes from the second array
    combined_bytes[len(object_1) :] = object_2[0 :]
    # return the new set of bytes
    return combined_bytes


# This function takes a single array of bytes and splits it into two
def splitBytes(total_bytes : bytes, len_first_array : int):
    # the length_at_split should also be the length of the first byte object
    object_1 = bytearray(len_first_array)
    object_2 = bytearray(len(total_bytes) - len_first_array)
    # extract the first set of bytes
    object_1[0 :] = total_bytes[0 : len_first_array]
    # extract the second set of bytes
    object_2[0 :] = total_bytes[len_first_array :]
    # return both of the resulting arrays
    return object_1, object_2


# This function will take a single array of bytes and split it into two after encountering a delimiter
def splitBytesOnDelimiter(total_bytes : bytes):
    delim_size = len(PAYLOAD_DELIMITER)
    found = False 
    delim_index = 1
    scanned_bytes = bytearray(delim_size)
    # start by scanning for the delimiter
    scanned_bytes[0 : delim_size] = total_bytes[0 : delim_size]
    for single_byte in total_bytes[delim_size : len(total_bytes)]:
        scanned_bytes = shiftBytes(scanned_bytes)
        scanned_bytes[delim_size - 1] = single_byte
        if bytes(scanned_bytes) == bytes(PAYLOAD_DELIMITER):
            # we have found where the delimiter is, exit the loop
            found = True
            break
        else:
            # we need to keep searching for the delmiter, increment the index we are checking
            delim_index = delim_index + 1
    # confirm that we have found the delimiter
    assert found, "Err, no delimiter was found within the bytestring"
    # extract the byte array from either side of the delimiter as two new byte objects
    object_1 = bytearray(delim_index)
    object_2 = bytearray(len(total_bytes) - delim_index - delim_size)
    object_1[0 :] = total_bytes[0 : delim_index]
    object_2[0 :] = total_bytes[delim_index + delim_size :]
    # return the individual byte arrays without the delimiter
    return object_1, object_2



# This function will shift all of the bytes in a byte array down by one index
def shiftBytes(bytes_to_shift):
    shifted_bytes = bytearray(len(bytes_to_shift))
    # copy everything but the fist byte into the new array
    # This will leave the last byte in the new array empty
    shifted_bytes[0 : len(bytes_to_shift) - 1] = bytes_to_shift[1 : len(bytes_to_shift)]
    return shifted_bytes





# ========================  MESSAGE CONSTRUCTORS =========================
"""
Each msg_code should have it's own constructor function to put data into a StandardDaoMsg object
NOTE:  These can be implemented later, whenever msg_codes are better implemented / defined
"""


# This function creates a StandardDaoMsg using the challenge_to_game msg
def build_challenge_to_game_msg(player_name : str, player_color : str):
    """
    This creates a challenge_to_game Dao message.
        - player_name:   The name of the player sending the challenge request
        - player_color:  The color this player would like to play as
    """
    msg = StandardDaoMsg()
    name_bytes = player_name.encode()
    color_bytes = combineBytes(PAYLOAD_DELIMITER, player_color.encode())
    payload = combineBytes(name_bytes, color_bytes)
    msg.configMsg(DaoMsgCode_e.challenge_to_game, payload)
    return msg
    

# This function creates a StandardDaoMsg using the challenge_response msg
def build_challenge_response_msg(player_name : str, accepted_status : bool):
    """
    This creates a challenge_response Dao message.
        - player_name:      The name of the player responding to a challenge
        - accepted_status:  True if the player is accepting the challenge, false if rejecting
    """
    msg = StandardDaoMsg()
    name_bytes = player_name.encode()
    accepted_btyes = combineBytes(PAYLOAD_DELIMITER, accepted_status.to_bytes(1))
    payload = combineBytes(name_bytes, accepted_btyes)
    msg.configMsg(DaoMsgCode_e.challenge_response, payload)
    return msg


# This function creates a StandardDaoMsg using the request_draw msg
def build_request_draw_msg():
    """
    This creates a request_draw Dao message.
    """
    msg = StandardDaoMsg()
    payload = bytes(0)
    msg.configMsg(DaoMsgCode_e.request_draw, payload)
    return msg


# This function creates a StandardDaoMsg using the draw_response msg
def build_draw_response_msg(accepted_status : bool):
    """
    This creates a draw_resonse Dao message.
        - accepted_status:  True if the player is accepting the draw, false if rejecting
    """
    msg = StandardDaoMsg()
    payload = accepted_status.to_bytes(1)
    msg.configMsg(DaoMsgCode_e.draw_response, payload)
    return msg


# This function creates a StandardDaoMsg using the resign msg
def build_resign_msg():
    """
    This creates a resign Dao message.
    """
    msg = StandardDaoMsg()
    payload = bytes(0)
    msg.configMsg(DaoMsgCode_e.resign, payload)
    return msg


# This function creates a StandardDaoMsg using the legal_move msg
def build_legal_move_msg(dao_piece : tempData, new_position : tempData):
    """
    This creates a legal_move Dao message.
    - dao_piece:    An identifier to know what piece is moving
    - new_position: The board position to move the piece to
    """
    msg = StandardDaoMsg()
    piece_bytes = dao_piece.getBytes()
    posit_bytes = combineBytes(PAYLOAD_DELIMITER, new_position.getBytes())
    payload = combineBytes(piece_bytes, posit_bytes)
    msg.configMsg(DaoMsgCode_e.legal_move, payload)
    return msg


# This function creates a StandardDaoMsg using the end_of_game msg
def build_end_of_game_mgs(end_status : str, win_player : str, win_method : str):
    """
    This creates an end_of_game Dao message.
        - end_status:  Describes the reason the game is ending
        - win_player:  Contains the name of the winning player if there is one
        - win_method:  Describes how the player won if there is a winning player
    """
    msg = StandardDaoMsg()
    end_bytes = end_status.encode()
    player_bytes = combineBytes(PAYLOAD_DELIMITER, win_player.encode())
    win_bytes = combineBytes(PAYLOAD_DELIMITER, win_method.encode())
    temp_payload = combineBytes(end_bytes, player_bytes)
    payload = combineBytes(temp_payload, win_bytes)
    msg.configMsg(DaoMsgCode_e.challenge_to_game, payload)
    return msg






# ========================  MESSAGE EXTRACTORS =========================
"""
These functions take a StandardDaoMsg object as input and extract relevant payload data
Only msg_codes that carry a payload need one of these
"""


# This function extracts payload data for the challenge_to_game msg
def extract_challenge_to_game_msg(msg : StandardDaoMsg):
    """
    This extracts data from a challenge_to_game Dao message.
        - player_name:   The name of the player sending the challenge request
        - player_color:  The color this player would like to play as
    """
    # get the bytes for each variable in the payload
    name_bytes, color_bytes = splitBytesOnDelimiter(msg.payload)
    # convert the bytes back into useable variables / structures
    player_name = name_bytes.decode()
    player_color = color_bytes.decode()
    return player_name, player_color


# This function extracts payload data for the challenge_response msg
def extract_challenge_response_msg(msg : StandardDaoMsg):
    """
    This extracts data from a challenge_response Dao message.
        - player_name:      The name of the player responding to a challenge
        - accepted_status:  True if the player is accepting the challenge, false if rejecting
    """
    # get the bytes for each variable in the payload
    name_bytes, accepted_btyes = splitBytesOnDelimiter(msg.payload)
    # convert the bytes back into useable variables / structures
    player_name = name_bytes.decode()
    accepted_status = bool.from_bytes(accepted_btyes)
    return player_name, accepted_status


# This function extracts payload data for the draw_response msg
def extract_draw_response_msg(msg : StandardDaoMsg):
    """
    This extracts data from a draw_resonse Dao message.
        - accepted_status:  True if the player is accepting the draw, false if rejecting
    """
    # convert the payload back into useable variables / structures
    accepted_status = bool.from_bytes(msg.payload)
    return accepted_status


# This function extracts payload data for the legal_move msg
def extract_legal_move_msg(msg : StandardDaoMsg):
    """
    This extracts data from a legal_move Dao message.
    - dao_piece:    An identifier to know what piece is moving
    - new_position: The board position to move the piece to
    """
    # get the bytes for each variable in the payload
    piece_bytes, posit_bytes = splitBytesOnDelimiter(msg.payload)
    # convert the bytes back into useable variables / structures
    # TODO: implement the reverse byte conversion once no longer using tempData structures
    dao_piece = tempData()
    new_position = tempData()
    return dao_piece, new_position


# This function extracts payload data for the end_of_game msg
def extract_end_of_game_mgs(msg : StandardDaoMsg):
    """
    This extracts data from an end_of_game Dao message.
        - end_status:  Describes the reason the game is ending
        - win_player:  Contains the name of the winning player if there is one
        - win_method:  Describes how the player won if there is a winning player
    """
    # get the bytes for each variable in the payload
    end_bytes, temp_bytes = splitBytesOnDelimiter(msg.payload)
    player_bytes, win_bytes = splitBytesOnDelimiter(temp_bytes)
    # convert the bytes back into useable variables / structures
    end_status = end_bytes.decode()
    win_player = player_bytes.decode()
    win_method = win_bytes.decode()
    return end_status, win_player, win_method






# ========================= TEMP TEST CODE PLZ IGNORE ==============================

# DO NOT INCLUDE WITH FINAL DAOMSGDEF FILE
# this is for testing functions within this file to make sure they work as intended
# This should be removed after some kind of communication interface is created


def main():
    # testing building a StandDaoMsg with a function and getting the bytes
    data1 = tempData()
    data2 = tempData()
    test = build_legal_move_msg(data1, data2)
    test_bytes = test.getBytes()
    test2 = StandardDaoMsg()

    # testing that we can convert the bytes from the first msg into a new msg structure
    test2.buildFromBytes(test_bytes)
    print("initial bytes")
    print(test_bytes)
    print("new msg structure bytes")
    # test2's bytes should match the initial test_bytes perfectly
    print(test2.getBytes())
    # all of the below should match data related to the legal_move function
    print(test2.msg_code)
    print(test2.payload_length)
    print(test2.payload)
    print()

    # Testing a different message function with a boolean and string input
    print("TESTING CHALLENGE RSP MESSAGE")
    name = "The Wolfzer"
    accepted = True
    test3 = build_challenge_response_msg(name, accepted)
    test3_bytes = test3.getBytes()
    print(test3_bytes)
    print()

    # Testing extracting the above data using the msg extractor
    print("TESTING EXTRACT ON CHALLENGE RESPONSE")
    rsp_msg = StandardDaoMsg()
    rsp_msg.buildFromBytes(test3.getBytes())
    name, accepted = extract_challenge_response_msg(rsp_msg)
    print(name, accepted)
    print()

    # Testing helper functions that help create or extract information from byte arrays
    print("TESTING BYTE MANIPULATION HELPER FUNCTIONS")
    bytes1 = "Hello World! ".encode()
    bytes2 = "Yo Mamma so fat".encode()
    bytes3 = combineBytes(bytes1, bytes2)
    print(bytes3)
    bytes4, bytes5 = splitBytes(bytes3, len(bytes1))
    print(bytes4)
    print(bytes5)
    print()
    bytes6 = combineBytes(bytes1, combineBytes(PAYLOAD_DELIMITER, bytes2))
    print(bytes6)
    bytes7, bytes8 = splitBytesOnDelimiter(bytes6)
    print(bytes7)
    print(bytes8)


if __name__ == "__main__":
    main()

