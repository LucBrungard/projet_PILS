from tkinter import *

class GraphicalVisualizer:
   """Class that represent the graphical visualizer"""

   def __init__(self, master: Toplevel) -> None:
      self.master = master
      self.master.geometry("500x250")
      master.title("Visualiseur graphique")