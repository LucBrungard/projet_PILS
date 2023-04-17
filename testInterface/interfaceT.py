from tkinter import *
from ivy.std_api import *


class InterfaceT:
   def __init__(self):
      self.fenetre = Tk()
      self.fenetre.title("LOGO Texte")
      self.fenetre.geometry("300x300")

   def afficheCommande(self, commande):
      text = Label(self.fenetre, text=commande, font=("Constantia", 14))
      text.pack()
