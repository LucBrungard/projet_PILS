from tkinter import *
from graphicalVisualizer.tortue import *
from PIL import EpsImagePlugin


class GraphicalVisualizer:
    """Class that represent the graphical visualizer"""

    def __init__(self, master: Toplevel) -> None:
        self.master = master
        self.master.geometry("500x250")
        master.title("Visualiseur graphique")

        self.canvasTurtle = Canvas(master, width=600, height=600)
        self.canvasTurtle.grid(row=1, column=1, columnspan=3)

        save_btn = Button(master, text="Save", command=self.saveCanvas)
        save_btn.grid(column=1, row=2)

        self.turtle = Tortue()
        self.turtle.image(self.canvasTurtle)

    def saveCanvas(self):
        self.turtle.canvas.delete(self.turtle.dessinImage)
        self.canvasTurtle.postscript(file="image.eps", colormode="color")

        # EpsImagePlugin.gs_windows_binary = r'C:\Program Files\gs\gs10.01.1\bin\gswin64c'

        # epsimage = Image.open('image.eps')
        # epsimage.show()
        # epsimage.save('image.png', quality=99)

        self.turtle.dessinImage = self.turtle.canvas.create_image(
            self.turtle.coord[0],
            self.turtle.coord[1],
            anchor=NW,
            image=self.turtle.imageFin,
        )

    def processIncoming(self, msg):
        x = msg.split()

        self.turtle.running = True

        if x[0] == "AVANCE":
            self.turtle.avancer(
                0,
                int(x[1]),
                [
                    (self.turtle.coord[0] + (self.turtle.coord[0] + 30)) / 2,
                    (self.turtle.coord[1] + (self.turtle.coord[1] + 30)) / 2,
                ],
            )
        elif x[0] == "RECULE":
            self.turtle.reculer(
                0,
                int(x[1]),
                [
                    (self.turtle.coord[0] + (self.turtle.coord[0] + 30)) / 2,
                    (self.turtle.coord[1] + (self.turtle.coord[1] + 30)) / 2,
                ],
            )
        elif x[0] == "TOURNEGAUCHE":
            self.turtle.tourner(-int(x[1]))
        elif x[0] == "TOURNEDROITE":
            self.turtle.tourner(int(x[1]))
        elif x[0] == "LEVECRAYON":
            self.turtle.leverCrayon()
        elif x[0] == "BAISSECRAYON":
            self.turtle.baisserCrayon()
        elif x[0] == "ORIGINE":
            self.turtle.origine()
        elif x[0] == "NETTOIE":
            self.turtle.nettoyer()
        elif x[0] == "RESTAURE":
            self.turtle.restaurer()
        elif x[0] == "FPOS":
            self.turtle.fixerPos([int(x[1]), int(x[2])])
        elif x[0] == "FCC":
            self.turtle.changerCouleur([int(x[1]), int(x[2]), int(x[3])])
        elif x[0] == "FCAP":
            self.turtle.fixerCap(int(x[1]))

        self.turtle.running = False

    def stop(self):
        pass
