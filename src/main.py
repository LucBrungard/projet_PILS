from tkinter import *
# from commands import *
from editor.editor import *
from graphicalVisualizer.graphicalVisualizer import *
from textualVisualizer.textualVisualizer import *
from queue import *


class Main:
   def __init__(self) -> None:
      # Set up the thread to do asynchronous I/O
      # More can be made if necessary
      self.running = 1

      # La fenêtre de gestion des différentes parties du logiciel
      self.master = Tk()

      self.queue = Queue()

      self.ivybus = MyAgent("main")

      self.createEditor()
      self.createGV()
      self.createTV()

      self.registerBindings()

      self.periodicCall()

      mainloop()

   def periodicCall(self):
      """
      Check every 100 ms if there is something new in the queue.
      """
      while self.queue.qsize():
         try:
            msg = self.queue.get(0)

            if (self.textualVisualizer != None):
               self.textualVisualizer.processIncoming(msg)
            if (self.graphicalVisualizer != None):
               self.graphicalVisualizer.processIncoming(msg)
         except Empty:
            pass

      if not self.running:
         import sys
         sys.exit(1)
      self.master.after(100, self.periodicCall)

   def createGV(self):
      self.graphicalVisualizer = None

      # Le bouton pour gérer la visualiseur graphique
      self.btnGV = Button(
          self.master,
          text="Visualiseur Graphique",
          background="green",
          command=lambda: self.createItem("graphicalVisualizer", "btnGV", GraphicalVisualizer))
      self.btnGV.grid(row=0, column=1)

      self.btnGV.invoke()

   def createTV(self):
      # La fenêtre du visualiseur textuel
      self.textualVisualizer = None

      # Le bouton pour gérer la visualiseur textuel
      self.btnTV = Button(
          self.master,
          text="Visualiseur textuel",
          background="green",
          command=lambda: self.createItem("textualVisualizer", "btnTV", TextualVisualizer))
      self.btnTV.grid(row=0, column=2)

      self.btnTV.invoke()

   def createEditor(self):
      # La fenêtre de l'éditeur
      self.editor = None

      # Le bouton pour gérer la fenêtre de l'éditeur
      self.btnEditor = Button(
          self.master,
          text="Editeur",
          background="green",
          command=lambda: self.createItem("editor", "btnEditor", Editor))
      self.btnEditor.grid(row=0, column=0)

      self.btnEditor.invoke()

   def closeWindow(self, btn: Button, window: Toplevel, itemName):
      btn.configure(bg="red")
      setattr(self, itemName, None)
      window.destroy()

   def createItem(self, itemName: str, btnName: str, constructor: Editor | GraphicalVisualizer | TextualVisualizer):
      """Créer une fenêtre si elle n'existe pas encore

      Args:
          windowName (str): Le nom de la fenêtre a créer
          btnName (str): Le nom du bouton qui est associé à la fenêtre
          constructor (Editor | GraphicalVisualizer | TextualVisualizer): Le constructeur du contenu de la fenêtre
      """
      item = getattr(self, itemName)
      btn = getattr(self, btnName)

      if item == None:
         window = Toplevel(self.master)
         window.protocol("WM_DELETE_WINDOW",
                         lambda btn=btn, window=window: self.closeWindow(btn, window, itemName))

         if (constructor == GraphicalVisualizer or constructor == TextualVisualizer):
            item = constructor(
                window, self.queue, self.ivybus, self.endApplication)
         else:
            item = constructor(window)
         setattr(self, itemName, item)
         btn.configure(background='green')

   def endApplication(self):
      self.running = 0

   def registerBindings(self):
      self.ivybus.bind_msg(
          lambda agent, n: self.queue.put("AVANCE " + n), "AVANCE (.*)")
      self.ivybus.bind_msg(
          lambda agent, n: self.queue.put("RECULE " + n), "RECULE (.*)")
      self.ivybus.bind_msg(
          lambda agent, n: self.queue.put("TOURNEDROITE " + n), "TOURNEDROITE (.*)")
      self.ivybus.bind_msg(
          lambda agent, n: self.queue.put("TOURNEGAUCHE " + n), "TOURNEGAUCHE (.*)")
      self.ivybus.bind_msg(
          lambda agent: self.queue.put("LEVECRAYON"), "LEVECRAYON")
      self.ivybus.bind_msg(
          lambda agent: self.queue.put("BAISSECRAYON"), "BAISSECRAYON")
      self.ivybus.bind_msg(
          lambda agent: self.queue.put("RESTAURE"), "RESTAURE")
      self.ivybus.bind_msg(
          lambda agent: self.queue.put("NETTOIE"), "NETTOIE")
      self.ivybus.bind_msg(
          lambda agent: self.queue.put("ORIGINE"), "ORIGINE")
      self.ivybus.bind_msg(
          lambda agent, x, y: self.queue.put(f"FPOS {x} {y}"), "FPOS (.*) (.*)")
      self.ivybus.bind_msg(
          lambda agent, r, g, b: self.queue.put(f"FCC {r} {g} {b}"), "FCC (.*) (.*) (.*)")
      self.ivybus.bind_msg(
          lambda agent: self.queue.put("QUITTER"), "QUITTER")


Main()
