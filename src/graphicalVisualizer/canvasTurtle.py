from tkinter import *
from ivybus import *
from PIL import Image


class CanvasTurtle:
    def __init__(self, master, tortue):
        self.fenetre = master

        self.option()

    def option(self):
        save_btn = Button(
            self.fenetre, text="SAUVEGARDER IMAGE", command=self.sauvegarderCanvas
        )
        save_btn.grid(column=1, row=2)

    def sauvegarderCanvas(self):
        self.tortue.canvas.delete(self.tortue.dessinImage)
        self.dessin.postscript(file="image.eps", colormode="color")

        epsimage = Image.open("image.eps")
        epsimage.show()
        epsimage.save("image.png", quality=99)

        self.tortue.dessinImage = self.tortue.canvas.create_image(
            self.tortue.coord[0],
            self.tortue.coord[1],
            anchor=NW,
            image=self.tortue.imageFin,
        )
