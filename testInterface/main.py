from tkinter import *
from thread import ThreadedClient
from tortue import Tortue
from interfaceC import InterfaceC

tortue = Tortue()
fenetreVisu = Tk()

client = ThreadedClient(fenetreVisu, tortue)

tortue.image(client.gui.interface.dessin)

interfaceCommand = InterfaceC()

fenetreVisu.mainloop()
interfaceCommand.fenetre.mainloop()