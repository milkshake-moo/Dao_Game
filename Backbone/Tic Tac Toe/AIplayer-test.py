# test the AI player for project 2
# open the AI file
AIfile = open("AIPlayer.txt",'r')
gamegrid = ["O"," ","O","X","X","X"," "," "," "]
gridSTR = ""
# check the game grid for the matching scenario
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
for n in gamegrid:
    gridSTR += str(n)
# compare the strings of possible moves to the current game grid
for i in range(len(PossibleList)):
    # find the scenario that matches
    if PossibleList[i] == gridSTR:
        # find where the AI will place marker
        placespot = int(AImovelist[i])
        MarkerPlaced = True
        # update game grid
        gamegrid[placespot] = "O"
# close the AI file
AIfile.close()

print(placespot)
print(gridSTR)
print(gamegrid)
