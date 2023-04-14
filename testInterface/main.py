from tkinter import *
from thread import ThreadedClient
from tortue import Tortue
from interfaceC import InterfaceC

tortue = Tortue()
fenetreVisu = Tk()
fenetreVisu.title("VisuLOGO")

client = ThreadedClient(fenetreVisu, tortue)

tortue.image(client.gui.interfaceV.dessin)

interfaceCommand = InterfaceC()

fenetreVisu.mainloop()
client.gui.interfaceT.mainloop()
interfaceCommand.fenetre.mainloop()