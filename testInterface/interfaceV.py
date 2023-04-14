from tkinter import *
from ivybus import *
from PIL import Image
from PIL import EpsImagePlugin
from PIL import ImageGrab

class InterfaceV :
    def __init__(self, master, tortue) :
        """self.fenetre = Tk()
        self.fenetre.title("LOGO Visu")"""

        self.fenetre = master

        self.dessin = Canvas(master, width=600, height=600)
        self.dessin.grid(row=1, column = 1, columnspan= 3)

        self.ivybus = MyAgent("VisuLOGO")

        self.tortue = tortue

        self.option()
        
    def bind_command(self, action, command) :
        self.ivybus.bind_msg(action, command)

    def option(self) :
        save_btn = Button(self.fenetre, text = 'SAUVEGARDER IMAGE', command=self.sauvegarderCanvas)
        save_btn.grid(column=1, row=2)

        """save_btn = Button(self.fenetre, text = 'QUITTER', command=self.fermer)
        save_btn.grid(column=3, row=2)"""

    """def fermer(self) :
        self.fenetre.destroy()
        self.ivybus.stop()"""

    def sauvegarderCanvas(self) :
        self.tortue.canvas.delete(self.tortue.dessinImage)
        self.dessin.postscript(file="image.eps", colormode='color')

        EpsImagePlugin.gs_windows_binary =  r'C:\Program Files\gs\gs10.01.1\bin\gswin64c'

        epsimage=Image.open('image.eps')
        epsimage.show()
        epsimage.save('image.png', quality=99)

        self.tortue.dessinImage = self.tortue.canvas.create_image(self.tortue.coord[0],self.tortue.coord[1], 
                                                                  anchor=NW, image=self.tortue.imageFin)
        #self.getter(self.dessin)

    """def getter(self):
        self.fenetre.update()
        x0 = self.dessin.winfo_rootx()
        y0 = self.dessin.winfo_rooty()
        x1 = x0 + self.dessin.winfo_width()
        y1 = y0 + self.dessin.winfo_height()
        
        im = ImageGrab.grab((x0, y0, x1, y1))
        im.show()
        #im.save('mypic.png') # Can also say im.show() to display it"""