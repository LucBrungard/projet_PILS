from tkinter import *
from tkinter import filedialog
import commands as commands
import os


class Editor:
   def saveFocused(self, item):
      if (self.focused != None):
         self.focused.configure(relief=RAISED)
      self.focused = item
      self.focused.configure(relief=SUNKEN)

   def copyCommand(self, event):
      master = event.widget.master
      for commandType in self.commands:
         if (master == self.commands[commandType]):
            command = None
            # If this command has parameter
            if (len(master.winfo_children()) > 1):
               parameter = None
               try:
                  parameter = int(master.winfo_children()[1].get())
               except ValueError:
                  parameter = 0
               command = commandType(parameter)
            else:
               command = commandType()

            # Create graphical representation
            widget = command.visualize(self.visitorHistoricField)
            widget.pack(expand=True, fill=BOTH)

            # Bind the event to children
            for child in widget.winfo_children():
               if (not isinstance(child, Entry)):
                  child.bind(
                      "<Button-1>", lambda event: self.saveFocused(widget))

            # Save the view
            self.historicCommandsView.append(widget)
            # Save the model
            self.historicCommands.append(command)

            break

   def removeElement(self):
      if (self.focused != None):
         self.focused.pack_forget()
         idx = self.historicCommandsView.index(self.focused)
         del self.historicCommandsView[idx]
         del self.historicCommands[idx]
         self.focused = None

   def moveUp(self):
      if (self.focused != None):
         for widget in self.historicCommandsView:
            widget.pack_forget()

         i = self.historicCommandsView.index(self.focused)

         # Swap values
         if (i > 0):
            self.historicCommandsView[i -
                                      1], self.historicCommandsView[i] = self.historicCommandsView[i], self.historicCommandsView[i-1]

            self.historicCommands[i -
                                  1], self.historicCommands[i] = self.historicCommands[i], self.historicCommands[i-1]

      # Repaint all items
      for widget in self.historicCommandsView:
         widget.pack(expand=True, fill=BOTH)

   def moveDown(self):
      if (self.focused != None):
         for widget in self.historicCommandsView:
            widget.pack_forget()

         i = self.historicCommandsView.index(self.focused)

         # Swap values
         if (i != len(self.historicCommandsView)-1):
            self.historicCommandsView[i], self.historicCommandsView[i +
                                                                    1] = self.historicCommandsView[i+1], self.historicCommandsView[i]

            self.historicCommands[i], self.historicCommands[i +
                                                            1] = self.historicCommands[i+1], self.historicCommands[i]

      # Repaint all items
      for widget in self.historicCommandsView:
         widget.pack(expand=True, fill=BOTH)

   def save(self):
      self.visitorSaveXML = commands.VisitorSaveXML()
      initialDir = os.getcwd() if (self.lastSelectedFolder ==
                                   None) else self.lastSelectedFolder
      file = filedialog.asksaveasfile(initialdir=initialDir)

      self.lastSelectedFolder = os.path.dirname(file.name)

      for command in self.historicCommands:
         file.write(command.save(self.visitorSaveXML)+"\n")
      file.close()

   def load(self):
      for widget in self.historicCommandsView:
         widget.pack_forget()
      self.historicCommandsView.clear()
      self.historicCommands.clear()

      initialDir = os.getcwd() if (self.lastSelectedFolder ==
                                   None) else self.lastSelectedFolder

      file = filedialog.askopenfile(
          initialdir=initialDir,
          title="Select a File",
          filetypes=[("XML Files", "*.xml*")])

      for line in file.readlines():
         # Remove <, >
         line = line[1:len(line)-2]
         lines = line.split()
         if lines[0] == "avancer":
            value = lines[1][5:]
            command = commands.Forward(value)
         elif lines[0] == "reculer":
            value = lines[1][5:]
            command = commands.Backward(value)
         elif lines[0] == "droite":
            value = lines[1][6:]
            command = commands.TurnRight(value)
         elif lines[0] == "gauche":
            value = lines[1][6:]
            command = commands.TurnLeft(value)
         elif lines[0] == "lever":
            command = commands.LiftPencil()
         elif lines[0] == "baisser":
            command = commands.LowerPencil()
         elif lines[0] == "origine":
            command = commands.Origin()
         elif lines[0] == "nettoyer":
            command = commands.Clean()
         elif lines[0] == "restaurer":
            command = commands.Restore()

         widget = command.visualize(self.visitorHistoricField)
         widget.pack(expand=True, fill=BOTH)

         self.historicCommandsView.append(widget)
         self.historicCommands.append(command)

         for child in widget.winfo_children():
            if (not isinstance(child, Entry)):
               child.bind(
                   "<Button-1>", lambda event, widget=widget: self.saveFocused(widget))

   def play(self):
      for command in self.historicCommands:
         print(command.toLogo())

   def __init__(self, master: Toplevel) -> None:
      self.master = master
      master.geometry("500x250")
      master.title("Editeur")

      self.focused = None
      self.historicCommandsView = []
      self.historicCommands = []

      self.lastSelectedFolder = None

      # Liste des commandes disponibles dans la zone de saisie
      self.commands = {
          commands.Forward: None,
          commands.Backward: None,
          commands.TurnLeft: None,
          commands.TurnRight: None,
          commands.LiftPencil: None,
          commands.LowerPencil: None,
          commands.Origin: None,
          commands.Restore: None,
          commands.Clean: None
      }

      # Creation de la zone de saisie
      self.inputField = LabelFrame(
          self.master, text="Zone de saisie", padx=20, pady=20, labelanchor="n")
      self.inputField.grid(row=0, column=0)

      # Création du visiteur qui permet de créer le rendu graphique des commandes
      self.visitorInputField = commands.VisitorEditorVisualiser(
          self.inputField)

      # Creation de la zone d'historique
      self.historicField = LabelFrame(
          self.master, text="Historique des commandes")
      self.historicField.grid(row=0, column=1)

      self.panelControlBtn = Frame(self.historicField)
      self.panelControlBtn.pack(side=RIGHT)
      self.btnDelete = Button(
          self.panelControlBtn, text="Delete", command=self.removeElement)
      self.btnDelete.pack()
      self.btnMoveUp = Button(self.panelControlBtn,
                              text="⬆", command=self.moveUp)
      self.btnMoveUp.pack()
      self.btnMoveDown = Button(
          self.panelControlBtn, text="⬇", command=self.moveDown)
      self.btnMoveDown.pack()

      self.panelHistoricCommands = Frame(self.historicField)
      self.panelHistoricCommands.pack(side=RIGHT)

      # Création du visiteur qui permet de créer le rendu graphique des commandes
      self.visitorHistoricField = commands.VisitorEditorVisualiser(
          self.panelHistoricCommands)

      # Creation du panel de boutons
      self.panelBtn = Frame(self.master)
      self.panelBtn.grid(row=1, column=0, columnspan=2)

      self.btnSave = Button(self.panelBtn, text="Save", command=self.save)
      self.btnSave.pack(side=LEFT)
      self.btnLoad = Button(self.panelBtn, text="Load", command=self.load)
      self.btnLoad.pack(side=LEFT)
      self.btnExec = Button(self.panelBtn, text="Play", command=self.play)
      self.btnExec.pack(side=LEFT)

      for command in self.commands:
         # On récupère la représentation graphique de la commande
         item = command().visualize(self.visitorInputField)
         # A une commande est associée une représentation graphique
         self.commands[command] = item
         item.pack(expand=True, fill=BOTH)

         for child in item.winfo_children():
            if (not isinstance(child, Entry)):
               child.bind(
                   "<Button-1>", lambda event: self.copyCommand(event))
