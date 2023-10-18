#
# CS 177 - project3.py
# Nicolas Miller: 0029780020
# Following Coding Standards and Guidelines
# This program creates a version of the game 'Tic-Tac-Toe' playable by
#   the user using a graphics interface and inputs from the mouse.
#   The program displays two graphics windows, a "Control" window and
#   a "Game Board" window. The game is playable by either zero, one or two
#   players and has implemented AI.
#   The game also implements added features such as customizable
#   usernames, games played, and option to play again without ending
#   the program.
#
# Import Libraries
from graphics import *
from random import choice
# define main() function
def main():
    # initialize variables
    IsEXIT = False
    IsGAME = False
    IsWinner = False
    IsPlayAgain = False
    CurrentTurn = 0
    ControlWin, P1button, P2button, ZPbutton, EXITbutton = ControlPanel()
    # loop until click on EXIT
    while (IsEXIT != True):
        # checkmouse() in control panel window
        CWclick = ControlWin.checkMouse()
        # was there a click?
        if (CWclick != None):
            # was 1Player clicked?
            Is1player = clickedOval(CWclick,P1button)
            if Is1player == True:
                # is game currently active?
                if IsGAME == True:
                    # close current game board window
                    GameWin.close()
                # initialize 1Player variables
                playernum = 1
                # randomize the starting player
                turnset = [1,3]
                CurrentTurn = choice(turnset)
                # open game board window for 1Player
                GameWin, TopText, BotText, IsGAME, gamegrid, Xmarker, Omarker = GameBoard(playernum)
            # was 2player clicked?
            Is2player = clickedOval(CWclick,P2button)
            if Is2player == True:
                # is game already active?
                if IsGAME == True:
                    # close current game board window
                    GameWin.close()
                # initialize 2Player variables
                playernum = 2
                # open game board window for 2Player
                GameWin, TopText, BotText, IsGAME, gamegrid, Xmarker, Omarker = GameBoard(playernum)
            # was Zero-player clicked?
            IsZplayer = clickedOval(CWclick,ZPbutton)
            if IsZplayer == True:
                # is the game currently active?
                if IsGAME == True:
                    # close the current game board
                    GameWin.close()
                # initializa Zeroplayer variables
                playernum = 0
                # randomize the starting AI
                turnset = [3,4]
                CurrentTurn = choice(turnset)
                # open game board window for zero players
                GameWin, TopText, BotText, IsGAME, gamegrid, Xmarker, Omarker = GameBoard(playernum)
            # was EXIT clicked?
            IsEXIT = clickedRect(CWclick,EXITbutton)
        # is game in progress?
        if (IsGAME == True) and (IsEXIT == False):
            # give current player chance to take turn
            GameWin,gamegrid = PlayTurn(playernum,GameWin,gamegrid,CurrentTurn,TopText,BotText,Xmarker,Omarker)
            # is there a winner?
            IsWinner, winningplayer, GameWin, gamegrid, CurrentTurn = CheckWinner(gamegrid,GameWin,CurrentTurn,playernum)
            if (IsWinner == True) or (IsWinner == 'Tie'):
                if IsWinner == True:
                    # display winner text
                    TopText.undraw()
                    BotText.undraw()
                    # if 2 player
                    if playernum == 2:
                        TopText.setText("Player "+str(winningplayer)+" wins!")
                    # if 1 player
                    if (playernum == 1) and (winningplayer == 1):
                        TopText.setText("Player "+str(winningplayer)+" wins!")
                    if (playernum == 1) and (winningplayer == 3):
                        TopText.setText("I win!")
                if IsWinner == "Tie":
                    TopText.undraw()
                    BotText.undraw()
                    TopText.setText("It's a tie...")
                BotText.setText("Click to close")
                TopText.draw(GameWin)
                BotText.draw(GameWin)
                # display the number of games played
                # open the file to get the previous games played
                gamefile = open('gamecount.txt','r')
                filelist = gamefile.readlines()
                gamefile.close()
                # change the amount of games played
                gamefile2 = open('gamecount.txt','w')
                for line in filelist:
                    gamenum = int(line)
                    gamenum += 1
                    gamefile2.write(str(gamenum))
                gamefile2.close()
                gamenum = 1
                # display the games played
                GamesPlayed = Text(Point(200,50),"Games Played: "+str(gamenum))
                gamenum += 1
                GamesPlayed.draw(GameWin)
                # ask for play again
                # draw the objects
                Playagain = Rectangle(Point(250,100),Point(350,150))
                Playagaintxt = Text(Point(300,125),"PLAY AGAIN?")
                Playagain.setFill('green')
                Playagain.draw(GameWin)
                Playagaintxt.draw(GameWin)
                # wait for click
                GWclick = GameWin.getMouse()
                # check for a click in play again
                IsPlayAgain = clickedRect(GWclick,Playagain)
                if IsPlayAgain == True:
                    IsEXIT = False
                # close game board window
                GamesPlayed.undraw()
                GameWin.close()
                # reset variables
                IsGAME = False
                IsWinner = False
                CurrentTurn = 1
    # close the program after the while loop terminates
    ControlWin.close()
    GameWin.close()

# define ControlPanel() function
def ControlPanel():
    # define 400x400 graphics window with light grey background
    ControlWin = GraphWin('Control Panel',400,400)
    ControlWin.setBackground("light grey")
    # draw 2 image GIFs using files provided
    image1 = Image(Point(200,55),'TicTacToe-Title.gif')
    image1.draw(ControlWin)
    image2 = Image(Point(200,260),'TicTacToe-Board.gif')
    image2.draw(ControlWin)
    # draw "v2.0" text object
    image3 = Text(Point(260,110),'v3.0')
    image3.setStyle('italic')
    image3.draw(ControlWin)
    # wait 3 seconds to continue
    time.sleep(3)
    # remove the lower GIF object
    image2.undraw()
    # draw 4 controls: 1-PLAYER, 2-PLAYER, Zero-player and EXIT
    # buttons
    P1button = Oval(Point(20,170),Point(130,230))
    P1button.setFill('blue')
    P1button.draw(ControlWin)
    P2button = Oval(Point(260,170),Point(150,230))
    P2button.setFill('yellow')
    P2button.draw(ControlWin)
    ZPbutton = Oval(Point(280,170),Point(390,230))
    ZPbutton.setFill('green')
    ZPbutton.draw(ControlWin)
    EXITbutton = Rectangle(Point(150,325),Point(250,375))
    EXITbutton.setFill('red')
    EXITbutton.draw(ControlWin)
    # text
    P1text = Text(Point(75,200),'1 - PLAYER')
    P1text.setFill('white')
    P1text.setSize(10)
    P1text.setStyle('bold')
    P1text.draw(ControlWin)
    P2text = Text(Point(205,200),'2 - PLAYER')
    P2text.setFill('black')
    P2text.setSize(10)
    P2text.setStyle('bold')
    P2text.draw(ControlWin)
    ZPtext = Text(Point(335,200),'Zero-PLAYER')
    ZPtext.setFill('black')
    ZPtext.setSize(10)
    ZPtext.setStyle('bold')
    ZPtext.draw(ControlWin)
    EXITtext = Text(Point(200,350),'EXIT')
    EXITtext.setFill('white')
    EXITtext.setSize(20)
    EXITtext.setStyle('bold')
    EXITtext.draw(ControlWin)
    # return the graphics window and three control objects
    return ControlWin, P1button, P2button, ZPbutton, EXITbutton

# define clickedOval() function
def clickedOval(point,oval):
    # find if a clicked point is in an oval
    # get the radii of the oval
    radx = abs(oval.getP1().getX() - oval.getP2().getX())/2
    rady = abs(oval.getP1().getY() - oval.getP2().getY())/2
    # get the center of the oval
    cenx = oval.getCenter().getX()
    ceny = oval.getCenter().getY()
    # coordinates of the point
    x = point.getX()
    y = point.getY()
    # return True if the point is in the oval
    return (x-cenx)**2/radx**2 + (y-ceny)**2/rady**2 <= 1

# define clickedRect() function
def clickedRect(point,rectangle):
    # find if a clicked point is in a rectangle
    # get the coordinates of the rectangle corner points
    corner1 = rectangle.getP1()
    corner2 = rectangle.getP2()
    # return true if the click was in the rectangle
    if (point.getX() >= corner1.getX()) and (point.getX() <= corner2.getX()):
        if (point.getY() >= corner1.getY()) and (point.getY() <= corner2.getY()):
            return True
        else:
            return False
    else:
        return False

# define GameBoard() function
def GameBoard(playernum):
    # a game has started
    IsGAME = True
    # create the graphics window
    GameWin = GraphWin('Game Board',600,600)
    # draw the grid of lines
    line1 = Line(Point(150,250),Point(450,250))
    line2 = Line(Point(150,350),Point(450,350))
    line3 = Line(Point(250,150),Point(250,450))
    line4 = Line(Point(350,150),Point(350,450))
    line1.draw(GameWin)
    line2.draw(GameWin)
    line3.draw(GameWin)
    line4.draw(GameWin)
    # create the text objects
    if (playernum == 1) or (playernum == 2):
        TopText = Text(Point(300,75),"Your Turn Player 1")
        TopText.draw(GameWin)
        BotText = Text(Point(300,525),"Click to place a marker")
        BotText.draw(GameWin)
    if playernum == 0:
        TopText = Text(Point(300,75),"My Turn")
        TopText.draw(GameWin)
        BotText = Text(Point(300,525),"Thinking...")
        BotText.draw(GameWin)
    # create the initial game grid
    gamegrid = [" "," "," "," "," "," "," "," "," "]
    # create marker objects
    Xmarker = Text(Point(300,300),"X")
    Xmarker.setStyle('bold')
    Xmarker.setSize(30)
    Omarker = Text(Point(300,300),"O")
    Omarker.setStyle('bold')
    Omarker.setSize(30)
    # return the game board window, text objects, updated game status, grid, and markers
    return GameWin, TopText, BotText, IsGAME, gamegrid, Xmarker, Omarker

# define PlayTurn() function
def PlayTurn(playernum,GameWin,gamegrid,CurrentTurn,TopText,BotText,Xmarker,Omarker):
    # initialize variables
    IsTurn = True
    placespot = 10
    MarkerPlaced = False
    # set the text
    TopText.undraw()
    BotText.undraw()
    if (CurrentTurn == 1) or (CurrentTurn == 2):
        # update text
        TopText.setText("Your Turn Player "+str(CurrentTurn))
        BotText.setText("Click to place a marker")
    if (CurrentTurn == 3) or (CurrentTurn == 4):
        # set text to AI player thinking
        TopText.setText("My Turn")
        BotText.setText("Thinking...")
    TopText.draw(GameWin)
    BotText.draw(GameWin)
    # setup a loop for the player's turn
    while IsTurn == True:
        # if player's turn, check for a mouse click in the game window
        if (CurrentTurn == 1) or (CurrentTurn ==2):
            GWclick = GameWin.checkMouse()
            # was there a click?
            if GWclick != None:
                # check the click for each grid slot
                if (150<GWclick.getX()<250) and (150<GWclick.getY()<250):
                    placespot = 0
                if (250<GWclick.getX()<350) and (150<GWclick.getY()<250):
                    placespot = 1
                if (350<GWclick.getX()<450) and (150<GWclick.getY()<250):
                    placespot = 2
                if (150<GWclick.getX()<250) and (250<GWclick.getY()<350):
                    placespot = 3
                if (250<GWclick.getX()<350) and (250<GWclick.getY()<350):
                    placespot = 4
                if (350<GWclick.getX()<450) and (250<GWclick.getY()<350):
                    placespot = 5
                if (150<GWclick.getX()<250) and (350<GWclick.getY()<450):
                    placespot = 6
                if (250<GWclick.getX()<350) and (350<GWclick.getY()<450):
                    placespot = 7
                if (350<GWclick.getX()<450) and (350<GWclick.getY()<450):
                    placespot = 8
                # if clicked, check for empty spot
                if placespot != 10:
                    # if empty, place correct player marker
                    if gamegrid[placespot] == " ":
                        if CurrentTurn == 1:
                            gamegrid[placespot] = "X"
                        if CurrentTurn == 2:
                            gamegrid[placespot] = "O"
                        MarkerPlaced = True
        # if AI player 1's turn, choose location from AI file
        if CurrentTurn == 3:
            # think for 2 seconds
            time.sleep(2)
            # open the AI file
            AIfile = open("AIPlayer2.txt",'r')
            # initialize variables
            placespot = 10
            PossibleList = []
            AImovelist = []
            # read the AI file
            for line in AIfile.readlines():
                lineList = line.split(":")
                # clean the text
                for x in lineList:
                    x = x.strip("\n")
                    # separate the grid scenarios from the integer
                    if len(x) > 1:
                        PossibleList.append(x)
                    if len(x) == 1:
                        AImovelist.append(x)
            # make the current grid into a string
            gridSTR = ""
            for n in gamegrid:
                gridSTR += str(n)
            # compare the strings of possible moves to the current game grid
            for i in range(len(PossibleList)):
                # find the scenario that matches
                if "".join(PossibleList[i]) == gridSTR:
                    # find where the AI will place marker
                    placespot = int(AImovelist[i])
                    # update game grid
                    if gamegrid[placespot] == " ":
                        gamegrid[placespot] = "O"
                        MarkerPlaced = True
            # close the AI file
            AIfile.close()
        # if AI player 2's turn, choose location from AI file
        if CurrentTurn == 4:
            # think for 2 seconds
            time.sleep(2)
            # open the AI file
            AIfile2 = open("AIPlayer2.txt",'r')
            # initialize variables
            placespot = 10
            PossibleList2 = []
            AImovelist2 = []
            # read the AI file
            for line in AIfile2.readlines():
                lineList = line.split(":")
                # clean the text
                for x in lineList:
                    x = x.strip("\n")
                    # separate the grid scenarios from the integer
                    if len(x) > 1:
                        PossibleList2.append(x)
                    if len(x) == 1:
                        AImovelist2.append(x)
            # make the current grid into a string
            gridSTR = ""
            for n in gamegrid:
                gridSTR += str(n)
            # compare the strings of possible moves to the current game grid
            for i in range(len(PossibleList2)):
                # find the scenario that matches
                if "".join(PossibleList2[i]) == gridSTR:
                    # find where the AI will place marker
                    placespot = int(AImovelist2[i])
                    # update game grid
                    if gamegrid[placespot] == " ":
                        gamegrid[placespot] = "O"
                        MarkerPlaced = True
            # close the AI file
            AIfile2.close()
        # update the game window
        # if the marker is placed
        if MarkerPlaced == True:
            # copy the marker objects
            Xcopy = Xmarker.clone()
            Ocopy = Omarker.clone()
            # find where to move the marker to
            if placespot == 0:
                dx,dy = -100,-100
            if placespot == 1:
                dx,dy = 0,-100
            if placespot == 2:
                dx,dy = 100,-100
            if placespot == 3:
                dx,dy = -100,0
            if placespot == 4:
                dx,dy = 0,0
            if placespot == 5:
                dx,dy = 100,0
            if placespot == 6:
                dx,dy = -100,100
            if placespot == 7:
                dx,dy = 0,100
            if placespot == 8:
                dx,dy = 100,100
            # move the correct marker and draw it
            if (CurrentTurn == 1) or (CurrentTurn == 4):
                Xcopy.move(dx,dy)
                Xcopy.draw(GameWin)
            if (CurrentTurn == 2) or (CurrentTurn == 3):
                Ocopy.move(dx,dy)
                Ocopy.draw(GameWin)
        # if the marker is placed
        if MarkerPlaced == True:
            # update the turn status
            IsTurn = False
    # return the updated game window and game grid
    return GameWin, gamegrid

# define the CheckWinner() function
def CheckWinner(gamegrid,GameWin,CurrentTurn,playernum):
    # initialize
    WinMark = "NOT"
    IsWinner = False
    winningplayer = 10
    # check the current game grid for a 3-in-a-row win
    # check columns
    if gamegrid[0]==gamegrid[3]==gamegrid[6]!=" ":
        lineX1,lineX2,lineY1,lineY2 = 200,200,175,425
        if gamegrid[0]=='X':
            WinMark = 'X'
        if gamegrid[0]=='O':
            WinMark = 'O'
    if gamegrid[1]==gamegrid[4]==gamegrid[7]!=" ":
        lineX1,lineX2,lineY1,lineY2 = 300,300,175,425
        if gamegrid[1]=='X':
            WinMark = 'X'
        if gamegrid[1]=='O':
            WinMark = 'O'
    if gamegrid[2]==gamegrid[5]==gamegrid[8]!=" ":
        lineX1,lineX2,lineY1,lineY2 = 400,400,175,425
        if gamegrid[2]=='X':
            WinMark = 'X'
        if gamegrid[2]=='O':
            WinMark = 'O'
    # check rows
    if gamegrid[0]==gamegrid[1]==gamegrid[2]!=" ":
        lineX1,lineX2,lineY1,lineY2 = 175,425,200,200
        if gamegrid[0]=='X':
            WinMark = 'X'
        if gamegrid[0]=='O':
            WinMark = 'O'
    if gamegrid[3]==gamegrid[4]==gamegrid[5]!=" ":
        lineX1,lineX2,lineY1,lineY2 = 175,425,300,300
        if gamegrid[3]=='X':
            WinMark = 'X'
        if gamegrid[3]=='O':
            WinMark = 'O'
    if gamegrid[6]==gamegrid[7]==gamegrid[8]!=" ":
        lineX1,lineX2,lineY1,lineY2 = 175,425,400,400
        if gamegrid[6]=='X':
            WinMark = 'X'
        if gamegrid[6]=='O':
            WinMark = 'O'
    # check diagonals
    if gamegrid[0]==gamegrid[4]==gamegrid[8]!=" ":
        lineX1,lineX2,lineY1,lineY2 = 175,425,175,425
        if gamegrid[0]=='X':
            WinMark = 'X'
        if gamegrid[0]=='O':
            WinMark = 'O'
    if gamegrid[2]==gamegrid[4]==gamegrid[6]!=" ":
        lineX1,lineX2,lineY1,lineY2 = 425,175,175,425
        if gamegrid[2]=='X':
            WinMark = 'X'
        if gamegrid[2]=='O':
            WinMark = 'O'
    # if there is a winner
    if (WinMark=='X') or (WinMark=='O'):
        # draw the line in the correct winning pattern
        WinLine = Line(Point(lineX1,lineY1),Point(lineX2,lineY2))
        WinLine.setFill('red')
        WinLine.setWidth(4)
        WinLine.draw(GameWin)
        # assign winningplayer to the player who's turn it was
        if CurrentTurn == 1:
            winningplayer = 1
        if CurrentTurn == 2:
            winningplayer = 2
        if CurrentTurn == 3:
            winningplayer = 3
        if CurrentTurn == 4:
            winningplayer = 4
        # update IsWinner
        IsWinner = True
    # check for tie
    if (gamegrid[0]!=" ") and (gamegrid[1]!=" ") and (gamegrid[2]!=" ") and (gamegrid[3]!=" ") and (gamegrid[4]!=" ") and (gamegrid[5]!=" ") and (gamegrid[6]!=" ") and (gamegrid[7]!=" ") and (gamegrid[8]!=" ") and (IsWinner==False):
        IsWinner = "Tie"                                                      
    # update the current turn
    if (playernum == 1) and (CurrentTurn == 1):
        # AI1 turn is 3
        NextTurn = 3
    if (playernum == 1) and (CurrentTurn == 3):
        NextTurn = 1
    if (playernum == 2) and (CurrentTurn == 1):
        NextTurn = 2
    if (playernum == 2) and (CurrentTurn == 2):
        NextTurn = 1
    if (playernum == 0) and (CurrentTurn == 3):
        # AI2 turn is 4
        NextTurn = 4
    if (playernum == 0) and (CurrentTurn == 4):
        NextTurn = 3
    CurrentTurn = NextTurn
    # return IsWinner, winning player, game window, game grid, and current turn
    return IsWinner, winningplayer, GameWin, gamegrid, CurrentTurn
    
# Run the program
main()