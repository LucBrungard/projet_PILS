from tkinter import *
from ivybus import *

class InterfaceV :
    def __init__(self, master, tortue) :
        """self.fenetre = Tk()
        self.fenetre.title("LOGO Visu")"""

        self.dessin = Canvas(master, width=400, height=400)
        self.dessin.grid(row=1, column = 1, columnspan= 3)

        self.ivybus = MyAgent("VisuLOGO")

        self.tortue = tortue

        #self.bind_commands()
        
    def bind_command(self, action, command) :
        self.ivybus.bind_msg(action, command)