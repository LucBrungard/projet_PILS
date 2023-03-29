from tkinter import *

class TextualVisualizer:
   """Class that represent the textual visualizer"""

   def __init__(self, master: Toplevel) -> None:
      self.master = master
      self.master.geometry("500x250")
      master.title("Visualiseur textuel")