
"""
This file tests aspects of tkinter so TJ can figure out what the heck he's doing

Things here will be random but hopefully well commented so this can be used as future reference
"""


import sys
# set sys path to allow imports from the parent directory
sys.path.append('../Dao_Game')


# imports n stuff
from tkinter import *



# Testing Tkinter class
class TestTkinterClass():
    """
    This class will store and initailze some widgets to test tkinter stuff
    """

    def __init__(self):
        app = Tk()
        self.canvas_height = 500
        self.canvas_width = 500
        self.canvas = Canvas(app, bg="grey", height=self.canvas_height, width=self.canvas_width)
        self.rect_1 = self.canvas.create_rectangle(10, 10, 100, 100, fill="blue")
        self.canvas.pack()
        self.debug_msg = Message(app, text="testing text!", width=400)
        self.debug_msg.config(bg = 'lightblue', font=('times', 24))
        #self.debug_msg.bind('<Motion>', self.mouse_motion)
        self.canvas.bind('<Motion>', self.update_canvas)
        self.canvas.bind('<Button-1>', self.draw_rect_at_click)
        self.canvas.bind('<Button-3>', self.move_rect_to_click)
        self.canvas.bind('<ButtonRelease-3>', self.release_selected_on_release)
        self.debug_msg.pack(side='bottom')
        self.objects = []
        self.objects.append(self.rect_1)
        self.selected = None
        app.mainloop()
    

    # update function to peridocially update things as needed
    def update_canvas(self, event : EventType.Motion):
        if self.selected != None:
            self.move_selected_to_cursor(event)
        self.mouse_motion(event)


    # function to bring the selected object to the mouse cursor 
    def move_selected_to_cursor(self, event : EventType.Motion):
        x1, y1, x2, y2 = self.canvas.coords(self.selected)
        offset_x = (x2 - x1) / 2
        offset_y = (y2 - y1) / 2

        # keep the selected object within the bounds of the canvas
        if event.x > offset_x:
            x_pos = min((event.x - offset_x), self.canvas_width - (offset_x*2))
        else:
            x_pos = 0
        if event.y > offset_y:
            y_pos = min((event.y - offset_y), self.canvas_height - (offset_y*2))
        else:
            y_pos = 0

        # raise the selected object above other objects
        self.canvas.tag_raise(self.selected)
        # move the selected object to the new position
        self.canvas.moveto(self.selected, x_pos, y_pos)


    # print the position of the mouse when motion is detected
    def mouse_motion(self, event : EventType.Motion):
        new_text = "Mouse Position: " + str(event.x) + ", " + str(event.y)
        self.debug_msg.config(text=new_text)
        return
    

    # draw on the canvas when clicking on it
    def draw_rect_at_click(self, event : EventType.ButtonPress):
        width = 50
        height = 50
        corner_1 = (event.x - width/2), (event.y - height/2)
        corner_2 = (event.x + width/2), (event.y + height/2)
        new_rect = self.canvas.create_rectangle(corner_1, corner_2, fill="red")
        self.objects.append(new_rect)
        #self.canvas.pack()


    # attempt to un-select an object on button release
    def release_selected_on_release(self, event : EventType.ButtonRelease):
        self.selected = None

    
    # attempt to select an object on a button click
    def move_rect_to_click(self, event : EventType.ButtonPress):
        # get the object that was clicked on
        for i in self.objects:
            x1, y1, x2, y2 = self.canvas.coords(i)
            if (event.x > x1) and (event.y > y1) and (event.x < x2) and (event.y < y2):
                self.selected = i

        #self.canvas.moveto(self.rect_1, event.x, event.y)








# main function to initaite the test scripts and guis
def main():
    hello = TestTkinterClass()
    pass




# init main when this is run
if __name__ == "__main__":
    main()


