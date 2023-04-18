
from tkinter import *
import threading
from queue import *
from interfaceT import InterfaceT
from interfaceV import InterfaceV
from ivybus import MyAgent

class GuiPart:
    def __init__(self, master, tortue, queue, endCommand):
        self.queue = queue
        # Set up the GUI

        self.master = master
        self.tortue = tortue

        self.end = endCommand

        self.interfaceV = InterfaceV(master, tortue)
        self.interfaceT = InterfaceT()

        self.bind_commands()

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                print(msg)
                x = msg.split()
                if x[0] == "AVANCE" :
                    self.tortue.avancer(0, int(x[1]), 
                        [(self.tortue.coord[0] + (self.tortue.coord[0] + 30)) / 2, 
                        (self.tortue.coord[1] + (self.tortue.coord[1] + 30)) / 2])
                    self.interfaceT.afficheCommande(msg)
                elif x[0] == "RECULE" :
                    self.tortue.reculer(0, int(x[1]),
                        [(self.tortue.coord[0] + (self.tortue.coord[0] + 30)) / 2, 
                        (self.tortue.coord[1] + (self.tortue.coord[1] + 30)) / 2])
                    self.interfaceT.afficheCommande(msg)
                elif x[0] == "TOURNEGAUCHE" :
                    self.tortue.tourner(-int(x[1]))
                    self.interfaceT.afficheCommande(msg)
                elif x[0] == "TOURNEDROITE" :
                    self.tortue.tourner(int(x[1]))
                    self.interfaceT.afficheCommande(msg)
                elif x[0] == "LEVECRAYON" :
                    self.tortue.leverCrayon()
                    self.interfaceT.afficheCommande(msg)
                elif x[0] == "BAISSECRAYON" :
                    self.tortue.baisserCrayon()
                    self.interfaceT.afficheCommande(msg)
                elif x[0] == "ORIGINE" :
                    self.tortue.origine()
                    self.interfaceT.afficheCommande(msg)
                elif x[0] == "NETTOIE" :
                    self.tortue.nettoyer()
                    self.interfaceT.afficheCommande(msg)
                elif x[0] == "RESTAURE" :
                    self.tortue.restaurer()
                    self.interfaceT.afficheCommande(msg)
                elif x[0] == "FPOS" :
                    self.tortue.fixerPos([int(x[1]), int(x[2])])
                    self.interfaceT.afficheCommande(msg)
                elif x[0] == "FCC" :
                    self.tortue.changerCouleur([int(x[1]), int(x[2]), int(x[3])])
                    self.interfaceT.afficheCommande(msg)
                elif x[0] == "FCAP" :
                    self.tortue.fixerCap(int(x[1]))
                elif x[0] == "QUITTER" :
                    self.end()
                    self.interfaceV.ivybus.stop()
                
            except Empty:
                pass

    def bind_commands(self) :
        self.interfaceV.bind_command(self.avance, "AVANCE (.*)")
        self.interfaceV.bind_command(self.recule, "RECULE (.*)")
        self.interfaceV.bind_command(self.tourneDroite, "TOURNEDROITE (.*)")
        self.interfaceV.bind_command(self.tourneGauche, "TOURNEGAUCHE (.*)")
        self.interfaceV.bind_command(self.leveCrayon, "LEVECRAYON")
        self.interfaceV.bind_command(self.baisseCrayon, "BAISSECRAYON")
        self.interfaceV.bind_command(self.restaure, "RESTAURE")
        self.interfaceV.bind_command(self.nettoie, "NETTOIE")
        self.interfaceV.bind_command(self.origine, "ORIGINE")
        self.interfaceV.bind_command(self.fpos, "FPOS (.*) (.*)")
        self.interfaceV.bind_command(self.fcc, "FCC (.*) (.*) (.*)")
        self.interfaceV.bind_command(self.fcap, "FCAP (.*)")

        self.interfaceV.bind_command(self.quitte, "QUITTER")

    def avance(self, agent, n) :
        print("Received from ", agent, " : ", "AVANCE " + n)
        self.queue.put("AVANCE " + n)

    def recule(self, agent, n) :
        print("Received from ", agent, " : ", "RECULE " + n)
        self.queue.put("RECULE " + n)
    
    def restaure(self, agent) :
        print("Received from ", agent, " : ", "RESTAURE")
        self.queue.put("RESTAURE")

    def nettoie(self, agent) :
        print("Received from ", agent, " : ", "NETTOIE")
        self.queue.put("NETTOIE")

    def origine(self, agent) :
        print("Received from ", agent, " : ", "ORIGINE")
        self.queue.put("ORIGINE")

    def tourneDroite(self, agent, n) :
        print("Received from ", agent, "TOURNEDROITE " + n)
        self.queue.put("TOURNEDROITE " + n)

    def tourneGauche(self, agent, n) :
        print("Received from ", agent, "TOURNEGAUCHE " + n)
        self.queue.put("TOURNEGAUCHE " + n)

    def leveCrayon(self, agent) :
        print("Received from ", agent, "LEVECRAYON")
        self.queue.put("LEVECRAYON")
    
    def baisseCrayon(self, agent) :
        print("Received from ", agent, "BAISSECRAYON")
        self.queue.put("BAISSECRAYON")
    
    def fcc(self, agent, r, g, b) :
        print("Received from ", agent, "FCC " + r + " " + g + " " + b)
        self.queue.put("FCC " + r + " " + g + " " + b)
    
    def fpos(self, agent, x, y) :
        print("Received from ", agent, "FPOS " + x + " " + y)
        self.queue.put("FPOS " + x + " " + y)

    def fcap(self, agent, n) :
        print("Received from ", agent, "FCAP" + n)
        self.queue.put("FCAP " + n)
    
    def quitte(self, agent) :
        print("Received from ", agent, "QUITTER")
        self.queue.put("QUITTER")

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master, tortue):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        self.tortue = tortue

        # Create the queue
        self.queue = Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, tortue, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            """import sys
            sys.exit(1)"""
            self.master.destroy()
            self.gui.interfaceT.fenetre.destroy()
        self.master.after(100, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """

        """while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following 2 lines with the real
            # thing.
            time.sleep(rand.random() * 0.3)
            msg = rand.random()
            self.queue.put(msg)"""

    def endApplication(self):
        self.running = 0