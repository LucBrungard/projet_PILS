import threading
from commandParser import parseCommandCLI
from ivybus import *


class CLI(threading.Thread):
    """Class to handle inputs in cmd"""

    def __init__(self) -> None:
        threading.Thread.__init__(self, target=self.readInputs)
        self.daemon = True
        self.ivybus = MyAgent("cli")
        self.stop_event = threading.Event()

    def stop(self):
        self.ivybus.stop()
        self.stop_event.set()

    def readInputs(self):
        while not self.stop_event.is_set():
            user_input = input()
            command = parseCommandCLI(user_input)
            if command != None:
                self.ivybus.send_msg(command.toLogo())
            else:
                print("Commande incorrecte")
                    
