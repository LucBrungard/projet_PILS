from tkinter import *
import commands as commands


class Editor:
   def __init__(self, master: Toplevel) -> None:
      self.master = master
      master.geometry("500x250")
      master.title("Editeur")
      # itemWidth = master.winfo_screenwidth() / 4
      # itemHeight = master.winfo_screenheight() / 2

      # self.master = Frame(master,
      #                   width=itemWidth * 2,
      #                   height=itemHeight,
      #                   highlightbackground="black",
      #                   highlightthickness=1)
      # self.master.grid_propagate(0)

      # Label(self.master, text="Editeur").grid(
      #     row=0,
      #     column=0,
      #     columnspan=2
      # )

      # # Créer la zone pour dessiner les commandes autorisées
      # self.listCommandsZone = Frame(self.master,
      #                               width=itemWidth - 20,
      #                               height=itemHeight - 60)
      # self.listCommandsZone.pack_propagate(0)
      # self.listCommandsZone.grid(row=1, column=0, padx=10, pady=10)

      # # Créer la zone contenant l'historique des commandes
      # self.editorZone = Frame(self.master,
      #                         width=itemWidth - 20,
      #                         height=itemHeight - 60)
      # self.editorZone.pack_propagate(0)
      # self.editorZone.grid(row=1, column=1, padx=10, pady=10)

      # # Create a visitor to draw commands on zones
      # self.visitor = commands.VisitorEditor(self.listCommandsZone)

      # # Create the authorized commands
      # self.listCommands = [
      #     commands.Forward(50),
      #     commands.Backward(50),
      #     commands.TurnLeft(90),
      #     commands.TurnRight(90),
      #     commands.LiftPencil(),
      #     commands.LowerPencil(),
      #     commands.Origin(),
      #     commands.Restore(),
      #     commands.Clean()]

      # # Draw each commands authorized
      # for command in self.listCommands:
      #    command.toLOGOEditor(self.visitor).pack(expand=1, fill=BOTH)

      # Label(self.editorZone, text="Ecrirer son code ici ...").pack(
      #     side=TOP)