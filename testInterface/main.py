from tkinter import *
from tortue import Tortue
from interface import Interface

interface = Interface()

tortue = Tortue()
tortue.image(interface.dessin)

interface.boutons(tortue)

interface.fenetre.mainloop()