# version 0.2

# This is a full re-implementation of the webserver using the twisted web
# libraries to drastically simplify things.

# this code will run a webserver that will allow users to play games of Dao




# Basic Functionality:
# We will implement a basic webservice through twisted.web that will talk
# between users and the various aspects of the dao site
#
# Name Page:
# upon a persons first interaction with the server, they should be prompted
# to choose a name.  Afterwards they should be redirected to the main page.
# returning users should be redirected immedietly to the main page, not to here
#
# Main Page:
# this will serve to allow users to access all the features of the site. You
# should be able to see active users/game requests, start a game of dao, change
# your name, access recrods of previous dao games, and see some site info
#
# Game Page:
# this is the page a user will see when playing a game of dao.  this page
# should let the user move pieces of their color on their turn and show any
# moves made by the other player. There should be a way to time out of a game,
# a way to offer a draw, a way to resign, and a way to request a rematch once
# a game has concluded.  There should also be a way back to the main page from
# here.
#
# Record Page:
# this page should let the user see a list of all the previous games played
# which includes; the date/time, the users that played, the victor, and the
# victory condition if applicable.  There should be a way back to the main
# page and a way to view enter a replay page for any game in the list.
#
# Replay Page:
# this page should let a user walk back and forth through a record of a dao
# game.  It should include a full board, turn numbers/time taken on that move,
# a way to cycle through moves (forwards and backwards), clearly show the win
# condition, and have a way back to the record page.





# Game Functionality:
# Everything about the actual dao game will be processed and rendered client
# side via javascript.
# This server will need to keep track of active games and update users when
# their opponent make a move in their game.  




# imports
from twisted.web import server
from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints


# global variable constants
serverPort = 8080
serverAddress = 'localhost'
mainPageFile = "MainPage.html"
gamePageFile = "DaoGame.html"
namePageFile = "NamePage.html"



# global variables
knownUsers = {}  # dictionary object, session uid = key, user object = value


# user class
# this is the object the service will use to represent an active user
# this will store the uid from the users specific session object as well
class User():
    name = ""
    uid = 0
    def init(self, name, uid):
        self.name = name
        self.uid = uid

    def updateUid(self, uid):
        self.uid = uid

    def updateName(self, name):
        self.name = name
    

# game class
# this is the object the service will use to represent an active game
class DaoGame():
    gameID = 0



# game manager class
# This is the object that will keep track of all of the game objects, make new
# ones, etc.
class GameManager():
    activeGames = {} # game int id = key, game object = value
    
    




# webserver implementation class

class MainServer(Resource):
    isLeaf = True
    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)



    # handle get requests
    def render_GET(self, request):
        session = request.getSession()
        user = knownUsers[session.uid]
        if user==None:
            # if user is new, redirect to name page regardless of request
            return readHTML(namePageFile)
        # determine the path of the request
        path = ''
        for i in request.path:
            path = path + chr(i)
            print(i)
        output = "Hello, world!\nThis is located at: " + path
        return output.encode("utf8")



    # handle POST requests
    def render_POST(self, request):
        yolo = "new"




# Helper methods

# Load Html Page
# Will return the data of an html page in a format to send to the client
def readHTML(file):
    page = open(file, 'r')
    text = ""
    lines = page.read()
    # piece the file together into a string object
    for i in lines:
        text = text + i
    # encode and return the object
    return text.encode("utf8")



# main instantiation

serverResource = MainServer()

def main():
    website = server.Site(MainServer())
    endpoint = endpoints.TCP4ServerEndpoint(reactor, serverPort)
    endpoint.listen(website)
    try:
        reactor.run()
    except KeyboardInterrupt:
        pass
    




if __name__ == "__main__":
    main()


