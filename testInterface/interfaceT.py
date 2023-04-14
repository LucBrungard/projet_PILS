from tkinter import *
from ivy.std_api import *

class InterfaceT :
    def __init__(self) :
        self.fenetre = Tk()
        self.fenetre.title("LOGO Texte")
        self.fenetre.geometry("300x300")

        """save_btn = Button(self.fenetre, text = 'QUITTER', command=self.fermer)
        save_btn.pack()"""

    def afficheCommande(self, commande) :
        text = Label(self.fenetre, text = commande, font=("Constantia", 14))
        text.pack()
    
    """def fermer(self) :
        self.fenetre.destroy()
        self.ivybus.stop()"""