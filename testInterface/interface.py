from tkinter import *

class Interface :
    def __init__(self) :
        self.fenetre = Tk()
        self.fenetre.title("LOGO")
        
        self.dessin = Canvas(self.fenetre, width=400, height=400)
        self.dessin.grid(row=1, column = 1, columnspan= 3)
        
    def boutons(self, tortue) :

        saisi = Entry(self.fenetre)
        saisi.grid(column=2, row = 2)

        abtn = Button(self.fenetre, text = 'Avancer', command=lambda:tortue.avancer(0, int(saisi.get()), 
                    [(tortue.coord[0] + (tortue.coord[0] + 30)) / 2, (tortue.coord[1] + (tortue.coord[1] + 30)) / 2]))
        abtn.grid(column=2, row=3)

        rbtn = Button(self.fenetre, text = 'Reculer', command=lambda:tortue.reculer(0, int(saisi.get()),
                    [(tortue.coord[0] + (tortue.coord[0] + 30)) / 2, (tortue.coord[1] + (tortue.coord[1] + 30)) / 2]))
        rbtn.grid(column=2, row=5)

        gbtn = Button(self.fenetre, text = 'RotationGauche', command=lambda:tortue.tourner(- int(saisi.get())))
        gbtn.grid(column=1, row=4)

        dbtn = Button(self.fenetre, text = 'RotationDroite', command=lambda:tortue.tourner(int(saisi.get())))
        dbtn.grid(column=3, row=4)

        res_btn = Button(self.fenetre, text = 'Origine', command=tortue.origine)
        res_btn.grid(column=2, row=4)

        cood_btn = Button(self.fenetre, text = 'Nettoie', command=tortue.nettoyer)
        cood_btn.grid(column=1, row=2)

        nbtn = Button(self.fenetre, text = 'Restaure', command=tortue.restaurer)
        nbtn.grid(column=3, row=2)

        lc_btn = Button(self.fenetre, text = 'LeverCrayon', command=tortue.leverCrayon)
        lc_btn.grid(column=1, row=3)

        bc_btn = Button(self.fenetre, text = 'BaisserCrayon', command=tortue.baisserCrayon)
        bc_btn.grid(column=3, row=3)

        fp_btn = Button(self.fenetre, text = 'FPOS', command=lambda:tortue.fixerPos(saisi.get()))
        fp_btn.grid(column=1, row=5)

        fp_btn = Button(self.fenetre, text = 'FCC', command=lambda:tortue.changerCouleur(saisi.get()))
        fp_btn.grid(column=3, row=5)

