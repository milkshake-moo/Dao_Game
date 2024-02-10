
"""
This is for testing random things during the development of the gui interface and Dao App
"""


import sys
# set sys path to allow imports from the parent directory
sys.path.append('../Dao_Game')

# imports and things
from Backbone.DaoMsgDef import StandardDaoMsg
#from Backbone.DaoTransport import *
from Backbone.DaoApp import DaoApp, InitialAppGui
from Backbone.DaoGameObject import DaoPlayer



# main method for running stuffs
def main():
    # create the dao application instance
    main_app = DaoApp()

    # create an instance of the initial app gui
    init_gui = InitialAppGui(main_app)





# init main when this is run
if __name__ == "__main__":
    main()