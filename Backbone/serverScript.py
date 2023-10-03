# verison 0.1

# This code will run the backend of the Dao/Game server


# Server Features To Implement:
#
# Choose a name page;
#       Each user can choose a name when they connect to the server
#       This name will be used for all recordkeeping
#       Once a name is chosen, the user gets redirected to the main page
# Main Page;
#       Users can see other online users here
#       Users can access the records page here
#       Users see a MOTD or random messages
#       Users can challenge other users to a game of Dao here
#       Users can accept challenges from other users here;
#           This redirects both users into a game page
#       Users can return to the choose a name page from here
# Game Page;
#       Users in a game page are not visible to users on the main page
#       Each user can see / interact with a live version of the game
#       Every move / interaction with the game will interact with the server
#           The server will mediate the game and determine win conditions
#       Users can request/agree to draw or concede during the game
#       On game conclusion, users can play again or return to the main Page
# Record Page;
#       Users can view / search through all previously played Dao Games here
#       Users can enter a replay page by interacting with a record here
#       Users can view statistics about themselves / other users here
#       Users can return to the main page from here
# Replay Page;
#       Users can increment through each turn of a dao game here
#       Users see the board positions on each turn
#       Users can return to the Recpord Page from here





# imports
from http.server import BaseHTTPRequestHandler, HTTPServer
import time



# global variables
# addresses, pages, and connection information
hostName = "localhost"
serverPort = 8080
gamePage = "/DaoGame"
namePage = "/NamePage"
mainPage = "/MainPage"
gamePageFile = "DaoGame.html"
namePageFile = "NamePage.html"
mainPageFile = "MainPage.html"
nameUpdate = "/NamePage/update"

# global objects for storing information
activeUsers = []




# User Object class
class User:
    def __init__(self, name, address, page, intTime):
        
        # store the chosen name of this user
        self.name = name
        # store the address the user connected from
        self.address  = address
        # store the current page (place) of the active user
        self.page = page
        # store the last time this user interacted with the server
        self.interactionTime = intTime




# Main server class
class DaoServer(BaseHTTPRequestHandler):
    
    # handeling Get requests
    def do_GET(self):
        # parse the get request
        if(self.path == "/example"):
            self.exampleGet()
        elif(self.path == namePage):
            self.defaultPage()
        elif(self.path == gamePage):
            self.launchDaoGame()
        else:
            self.defaultPage()



    # handeling post requests
    def do_POST(self):
        print("recieved a post request")
        ioStream = self.rfile
        self.params, self.values = parseStream(ioStream)
        if(self.path == nameUpdate):
            # create an object for this user, store, load main page
            print("nameUpdate request recieved")
            name = self.values[0]
            self.createUser(name)
            self.mainPageGet()
            


    # function to create and add a new user to our array of users
    def createUser(self, name):
        newUser = User(name, self.client_address, mainPage, time.gmtime())
        activeUsers.append(newUser)

    def mainPageGet(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        page = open(mainPageFile, 'r')
        lines = page.read()
        for i in lines:
            self.wfile.write(bytes(i, "utf-8"))

    # Command to return an example page to the requester
    def exampleGet(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print(self.date_time_string())
        print(self.address_string())
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>You requested the Example Page!</p>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    # function to return the Dao Game Page to the requester
    def launchDaoGame(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        page = open(gamePageFile, 'r')
        lines = page.read()
        for i in lines:
            self.wfile.write(bytes(i, "utf-8"))


    # function to return the default page (the namePage) to the requester
    def defaultPage(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        page = open(namePageFile, 'r')
        lines = page.read()
        for i in lines:
            self.wfile.write(bytes(i, "utf-8"))




# function to parse and return objects from a buffered IO stream into two arrays
# the first array is the parameters/names of the values for the second array
# all elements in both arrays will be saved as lists of characters (strings) for simplicity sake
def parseStream(ioStream):
    temp = ""
    variables = []
    values = []
    selector = 0
    # read in one char at a time
    chars = ascii(ioStream.peek())
    chars = chars[2:-1]
    for nextByte in chars:
        print(nextByte)
        # upon receiving the '=' or ',' operator, store the operator and prepare to save the selector
        if(nextByte == '=' or nextByte == '&'):
            if(selector == 0):
                variables.append(temp)
                selector = 1
                temp = ""
            else:
                values.append(temp)
                selector = 0
                temp = ""
        # otherwise, add the next character to the temp var
        else:
            if(nextByte == '+'):
                nextByte = ' '
            temp = temp + nextByte
    # after the while loop, save the value stored in temp to the correct array
    if(selector == 1):
        values.append(temp)
    else:
        variables.append(temp)
    # finally return both arrays
    return variables, values



# Figure out a way to check active connections to the webserver.  When a connection is lost, that user
#   should be removed from our list of active users.  This is so users can see and interact with other
#   active users, and not be bogged down with anyone not currently online / active



# code to launch the application
if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), DaoServer)
    print("Server started http://%s:%s" %(hostName, serverPort))

    # initialize array of user objects
    
    # stop the server on keyboard interupt (ctrl + C)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server Stopped.")











