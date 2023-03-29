from tkinter import *
# from commands import *
from parts.editor import *
from parts.graphicalVisualizer import *
from parts.textualVisualizer import *


class Main:
   def __init__(self) -> None:
      # La fenêtre de gestion des différentes parties du logiciel
      self.master = Tk()

      # La fenêtre de l'éditeur
      self.editorWindow = None

      # La fenêtre du visualiseur graphique
      self.gvWindow = None

      # La fenêtre du visualiseur textuel
      self.tvWindow = None

      # Le bouton pour gérer la fenêtre de l'éditeur
      self.btnEditor = Button(
          self.master,
          text="Editeur",
          background="green",
          command=lambda: self.createWindow("editorWindow", "btnEditor", Editor))
      self.btnEditor.grid(row=0, column=0)

      # Le bouton pour gérer la visualiseur graphique
      self.btnGV = Button(
          self.master,
          text="Visualiseur Graphique",
          background="green",
          command=lambda: self.createWindow("gvWindow", "btnGV", GraphicalVisualizer))
      self.btnGV.grid(row=0, column=1)

      # Le bouton pour gérer la visualiseur textuel
      self.btnTV = Button(
          self.master,
          text="Visualiseur textuel",
          background="green",
          command=lambda: self.createWindow("tvWindow", "btnTV", TextualVisualizer))
      self.btnTV.grid(row=0, column=2)

      # Création des fenêtres initiales
      self.btnEditor.invoke()
      self.btnGV.invoke()
      self.btnTV.invoke()

      mainloop()

   def closeWindow(self, btnName: str, windowName: str):
      """Ferme une fenêtre et met à jour le bouton qui gère cette fenêtre

      Args:
          btnName (str): Le nom du bouton qui gère la fenêtre
          windowName (str): Le nom de la fenêtre
      """
      btn = getattr(self, btnName)
      window = getattr(self, windowName)

      btn.configure(bg="red")
      window.destroy()

   def createWindow(self, windowName: str, btnName: str, constructor: Editor | GraphicalVisualizer | TextualVisualizer):
      """Créer une fenêtre si elle n'existe pas encore

      Args:
          windowName (str): Le nom de la fenêtre a créer
          btnName (str): Le nom du bouton qui est associé à la fenêtre
          constructor (Editor | GraphicalVisualizer | TextualVisualizer): Le constructeur du contenu de la fenêtre
      """
      window = getattr(self, windowName)
      btn = getattr(self, btnName)

      if (window == None) or (not Toplevel.winfo_exists(window)):
         window = Toplevel(self.master)
         setattr(self, windowName, window)
         window.protocol("WM_DELETE_WINDOW",
                         lambda: self.closeWindow(btnName, windowName))
         constructor(window)
         btn.configure(background='green')


Main()
