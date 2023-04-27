from tkinter import *


class TextualVisualizer:
    """Class that represent the textual visualizer"""

    def __init__(self, master: Toplevel) -> None:
        self.master = master
        self.master.geometry("500x250")
        master.title("Visualiseur textuel")

    def afficheCommande(self, commande):
        text = Label(self.master, text=commande, font=("Constantia", 14))
        text.pack()

    def processIncoming(self, msg):
        self.afficheCommande(msg)

    def stop(self):
        pass
