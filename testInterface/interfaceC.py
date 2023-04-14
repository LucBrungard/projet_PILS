from tkinter import *
from ivy.std_api import *

from ivybus import MyAgent

class InterfaceC :
    def __init__(self) :
        self.fenetre = Tk()
        self.fenetre.title("LOGO")

        self.ivybus = MyAgent("CommandeLOGO") 

        self.boutons()
        
    def boutons(self) :

        saisi = Entry(self.fenetre)
        saisi.grid(column=2, row = 2)

        abtn = Button(self.fenetre, text = 'Avancer', command=lambda:self.ivybus.send_msg("AVANCE " + saisi.get()))
        abtn.grid(column=2, row=3)

        rbtn = Button(self.fenetre, text = 'Reculer', command=lambda:self.ivybus.send_msg("RECULE " + saisi.get()))
        rbtn.grid(column=2, row=5)

        gbtn = Button(self.fenetre, text = 'RotationGauche', command=lambda:self.ivybus.send_msg("TOURNEGAUCHE " + saisi.get()))
        gbtn.grid(column=1, row=4)

        dbtn = Button(self.fenetre, text = 'RotationDroite', command=lambda:self.ivybus.send_msg("TOURNEDROITE " + saisi.get()))
        dbtn.grid(column=3, row=4)

        res_btn = Button(self.fenetre, text = 'Origine', command=lambda:self.ivybus.send_msg("ORIGINE " + saisi.get()))
        res_btn.grid(column=2, row=4)

        cood_btn = Button(self.fenetre, text = 'Nettoie', command=lambda:self.ivybus.send_msg("NETTOIE " + saisi.get()))
        cood_btn.grid(column=1, row=2)

        nbtn = Button(self.fenetre, text = 'Restaure', command=lambda:self.ivybus.send_msg("RESTAURE " + saisi.get()))
        nbtn.grid(column=3, row=2)

        lc_btn = Button(self.fenetre, text = 'LeverCrayon', command=lambda:self.ivybus.send_msg("LEVECRAYON " + saisi.get()))
        lc_btn.grid(column=1, row=3)

        bc_btn = Button(self.fenetre, text = 'BaisserCrayon', command=lambda:self.ivybus.send_msg("BAISSECRAYON " + saisi.get()))
        bc_btn.grid(column=3, row=3)

        fp_btn = Button(self.fenetre, text = 'FPOS', command=lambda:self.ivybus.send_msg("FPOS " + saisi.get()))
        fp_btn.grid(column=1, row=5)

        fp_btn = Button(self.fenetre, text = 'FCC', command=lambda:self.ivybus.send_msg("FCC " + saisi.get()))
        fp_btn.grid(column=3, row=5)



        act_btn = Button(self.fenetre, text = 'ACTION', command=lambda:self.ivybus.send_msg("ACTION"))
        act_btn.grid(column=2, row=6)

        quit_btn = Button(self.fenetre, text = 'QUITTER', command=self.quitter)
        quit_btn.grid(column=2, row=7)

    def quitter(self) :
        self.fenetre.destroy()
        self.ivybus.send_msg("QUITTER")
        self.ivybus.stop()