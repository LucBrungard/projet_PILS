from tkinter import *

# from commands import *
from editor.editor import *
from graphicalVisualizer.graphicalVisualizer import *
from textualVisualizer.textualVisualizer import *
from queue import *
from cli.cli import *


class Main:
    def __init__(self) -> None:
        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1

        # La fenêtre de gestion des différentes parties du logiciel
        self.master = Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.endApplication)

        self.queue = Queue()

        self.ivybus = MyAgent("main")
        self.registerBindings()

        self.createEditor()
        self.createGV()
        self.createTV()
        self.cli = CLI()
        self.cli.start()

        self.periodicCall()

        mainloop()

    def registerBindings(self):
        self.ivybus.bind_msg(
            lambda agent, n: self.queue.put("AVANCE " + n), "AVANCE (.*)"
        )
        self.ivybus.bind_msg(
            lambda agent, n: self.queue.put("RECULE " + n), "RECULE (.*)"
        )
        self.ivybus.bind_msg(
            lambda agent, n: self.queue.put("TOURNEDROITE " + n), "TOURNEDROITE (.*)"
        )
        self.ivybus.bind_msg(
            lambda agent, n: self.queue.put("TOURNEGAUCHE " + n), "TOURNEGAUCHE (.*)"
        )
        self.ivybus.bind_msg(lambda agent: self.queue.put("LEVECRAYON"), "LEVECRAYON")
        self.ivybus.bind_msg(
            lambda agent: self.queue.put("BAISSECRAYON"), "BAISSECRAYON"
        )
        self.ivybus.bind_msg(lambda agent: self.queue.put("RESTAURE"), "RESTAURE")
        self.ivybus.bind_msg(lambda agent: self.queue.put("NETTOIE"), "NETTOIE")
        self.ivybus.bind_msg(lambda agent: self.queue.put("ORIGINE"), "ORIGINE")
        self.ivybus.bind_msg(
            lambda agent, x, y: self.queue.put(f"FPOS {x} {y}"), "FPOS (.*) (.*)"
        )
        self.ivybus.bind_msg(
            lambda agent, r, g, b: self.queue.put(f"FCC {r} {g} {b}"),
            "FCC (.*) (.*) (.*)",
        )
        self.ivybus.bind_msg(lambda agent, n: self.queue.put("FCAP " + n), "FCAP (.*)")

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        if self.queue.qsize():
            try:
                if self.graphicalVisualizer != None:
                    if not self.graphicalVisualizer.turtle.running:
                        msg = self.queue.get(0)

                        if self.textualVisualizer != None:
                            self.textualVisualizer.processIncoming(msg)
                        self.graphicalVisualizer.processIncoming(msg)
                else:
                    if self.textualVisualizer != None:
                        msg = self.queue.get(0)
                        self.textualVisualizer.processIncoming(msg)
            except Empty:
                pass

        if not self.running:
            import sys

            self.master.destroy()
            sys.exit(1)
        self.after = self.master.after(100, self.periodicCall)

    def createGV(self):
        self.graphicalVisualizer = None

        # Le bouton pour gérer la visualiseur graphique
        self.btnGV = Button(
            self.master,
            text="Visualiseur Graphique",
            background="green",
            command=lambda: self.createItem(
                "graphicalVisualizer", "btnGV", GraphicalVisualizer
            ),
        )
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
            command=lambda: self.createItem(
                "textualVisualizer", "btnTV", TextualVisualizer
            ),
        )
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
            command=lambda: self.createItem("editor", "btnEditor", Editor),
        )
        self.btnEditor.grid(row=0, column=0)

        self.btnEditor.invoke()

    def closeWindow(self, btn: Button, window: Toplevel, itemName):
        item = getattr(self, itemName)
        item.stop()
        item = None

        btn.configure(bg="red")
        setattr(self, itemName, item)

        window.destroy()

    def createItem(
        self,
        itemName: str,
        btnName: str,
        constructor: Editor or GraphicalVisualizer or TextualVisualizer,
    ):
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
            window.protocol(
                "WM_DELETE_WINDOW",
                lambda btn=btn, window=window: self.closeWindow(btn, window, itemName),
            )

            item = constructor(window)
            setattr(self, itemName, item)

            btn.configure(background="green")

    def endApplication(self):
        self.ivybus.stop()

        if self.editor != None:
            self.editor.stop()

        if self.textualVisualizer != None:
            self.textualVisualizer.stop()

        if self.graphicalVisualizer != None:
            self.graphicalVisualizer.stop()

        if self.cli != None:
            self.cli.stop()

        self.running = 0


Main()
