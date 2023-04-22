from tkinter import *
from tkinter import filedialog
import commands as commands
import os
from commandParser import parseXML
from ivybus import MyAgent


class Editor:
    def saveFocused(self, item):
        if self.focused != None:
            self.focused.configure(relief=RAISED)
        self.focused = item
        self.focused.configure(relief=SUNKEN)

    def clone_widget(self, widget, master=None):
        """
        Create a cloned version o a widget

        Parameters
        ----------
        widget : tkinter widget
            tkinter widget that shall be cloned.
        master : tkinter widget, optional
            Master widget onto which cloned widget shall be placed. If None, same master of input widget will be used. The
            default is None.

        Returns
        -------
        cloned : tkinter widget
            Clone of input widget onto master widget.

        """
        # Get main info
        parent = master if master else widget.master
        cls = widget.__class__

        # Clone the widget configuration
        cfg = {key: widget.cget(key) for key in widget.configure()}
        cloned = cls(parent, **cfg)

        # Clone the widget's children
        for child in widget.winfo_children():
            child_cloned = self.clone_widget(child, master=cloned)
            if child.grid_info():
                grid_info = {
                    k: v for k, v in child.grid_info().items() if k not in {"in"}
                }
                child_cloned.grid(**grid_info)
            elif child.place_info():
                place_info = {
                    k: v for k, v in child.place_info().items() if k not in {"in"}
                }
                child_cloned.place(**place_info)
            else:
                pack_info = {
                    k: v for k, v in child.pack_info().items() if k not in {"in"}
                }
                child_cloned.pack(**pack_info)

        return cloned

    def copyCommand(self, master, visitorEditor: commands.VisitorEditorVisualiser):
        for commandType in self.commands:
            if master == self.commands[commandType]:
                command = None
                # If this command has parameter
                if len(master.winfo_children()) > 1:
                    parameter = None
                    if commandType is commands.FCC:
                        try:
                            parameter = [
                                int(master.winfo_children()[1].get()),
                                int(master.winfo_children()[2].get()),
                                int(master.winfo_children()[3].get()),
                            ]
                        except ValueError:
                            parameter = [0, 0, 0]
                    elif commandType is commands.FPOS:
                        try:
                            parameter = [
                                int(master.winfo_children()[1].get()),
                                int(master.winfo_children()[2].get()),
                            ]
                        except ValueError:
                            parameter = [0, 0]
                    elif commandType is commands.Repeat:
                        try:
                            parameter = int(
                                master.winfo_children()[1].winfo_children()[1].get()
                            )
                        except ValueError:
                            parameter = 0
                    else:
                        try:
                            parameter = int(master.winfo_children()[1].get())
                        except ValueError:
                            parameter = 0
                    command = commandType(parameter)
                else:
                    command = commandType()

                # Create graphical representation
                widget = command.visualize(visitorEditor)
                widget.pack(expand=True, fill=BOTH)

                # Bind the event to children
                for child in widget.winfo_children():
                    if not isinstance(child, Entry):
                        child.bind("<Button-1>", lambda event: self.saveFocused(widget))

                # Save the view
                self.historicCommandsView.append(widget)
                # Save the model
                self.historicCommands.append(command)

                break

    def removeElement(self):
        if self.focused != None:
            self.focused.pack_forget()
            idx = self.historicCommandsView.index(self.focused)

            item = self.historicCommandsView[idx]

            del self.historicCommandsView[idx]
            del self.historicCommands[idx]

            if isinstance(item, LabelFrame):
                print("children : ", item.winfo_children())
                for i in range(len(item.winfo_children()) - 2):
                    self.focused = self.historicCommandsView[idx]
                    self.removeElement()

            self.focused = None

            print(self.historicCommands)
            print(self.historicCommandsView)

    def redrawCommand(self, i: int, visitor: commands.VisitorEditorVisualiser):
        # Recreate graphical element
        self.historicCommandsView[i] = self.historicCommands[i].visualize(visitor)

        if isinstance(self.historicCommands[i], commands.Repeat):
            for command in self.historicCommands[i].commands:
                j = self.historicCommands.index(command, i)
                self.historicCommandsView[j] = self.historicCommands[j].visualize(
                    self.historicCommands[i].visitorDrawEditor
                )

        # Bind the event to children
        for child in self.historicCommandsView[i].winfo_children():
            if not isinstance(child, Entry):
                child.bind(
                    "<Button-1>",
                    lambda event, item=self.historicCommandsView[i]: self.saveFocused(
                        item
                    ),
                )

        self.saveFocused(self.historicCommandsView[i])

    def swapElements(self, i: int, j: int):
        if (
            isinstance(self.historicCommands[i], commands.Repeat)
            and j > i
            and len(self.historicCommands[i].commands) > 0
        ):
            for k in reversed(
                range(
                    i,
                    self.historicCommands.index(self.historicCommands[i].commands[-1])
                    + 1,
                )
            ):
                (
                    self.historicCommandsView[k + 1],
                    self.historicCommandsView[k],
                ) = (
                    self.historicCommandsView[k],
                    self.historicCommandsView[k + 1],
                )

                (
                    self.historicCommands[k + 1],
                    self.historicCommands[k],
                ) = (
                    self.historicCommands[k],
                    self.historicCommands[k + 1],
                )
            return

        (
            self.historicCommandsView[j],
            self.historicCommandsView[i],
        ) = (
            self.historicCommandsView[i],
            self.historicCommandsView[j],
        )

        (
            self.historicCommands[j],
            self.historicCommands[i],
        ) = (
            self.historicCommands[i],
            self.historicCommands[j],
        )

        if isinstance(self.historicCommands[j], commands.Repeat) and j < i:
            for command in self.historicCommands[j].commands:
                i += 1
                j += 1

                self.swapElements(i, j)

    def moveUp(self):
        if self.focused != None:
            i = self.historicCommandsView.index(self.focused)

            if i == 0:
                return

            # Eraise all widgets
            for widget in self.historicCommandsView:
                widget.pack_forget()

            # Make the movement
            if isinstance(self.focused.master, LabelFrame):
                # If element is in a repeat command
                if isinstance(self.historicCommandsView[i - 1], LabelFrame):
                    # If above element is a repeat command
                    j = self.historicCommandsView.index(self.focused.master)

                    if self.focused.master != self.historicCommandsView[i - 1]:
                        # if the repeat command above is different from parent

                        # Remove the command from parent
                        self.historicCommands[j].commands.remove(
                            self.historicCommands[i]
                        )

                        # Add command to the new parent
                        self.historicCommands[i - 1].commands.append(
                            self.historicCommands[i]
                        )

                        self.redrawCommand(
                            i,
                            commands.VisitorEditorVisualiser(
                                self.historicCommandsView[i - 1]
                            ),
                        )
                    else:
                        # if the repeat command above is the parent

                        # Remove command from parent
                        self.historicCommands[i - 1].commands.pop(0)

                        if isinstance(
                            self.historicCommandsView[i - 1].master, LabelFrame
                        ):
                            k = self.historicCommandsView.index(
                                self.historicCommandsView[i - 1].master
                            )

                            self.historicCommands[k].commands.insert(
                                self.historicCommands[k].commands.index(
                                    self.historicCommands[i - 1]
                                ),
                                self.historicCommands[i],
                            )

                        # Recreate element
                        self.redrawCommand(
                            i,
                            commands.VisitorEditorVisualiser(
                                self.historicCommandsView[i - 1].master
                            ),
                        )

                        self.swapElements(i=i, j=(i - 1))

                else:
                    # if above element is not a repeat command
                    j = self.historicCommandsView.index(self.focused.master)
                    for k in range(len(self.historicCommands[j].commands)):
                        if (
                            self.historicCommands[j].commands[k]
                            == self.historicCommands[i]
                        ):
                            (
                                self.historicCommands[j].commands[k - 1],
                                self.historicCommands[j].commands[k],
                            ) = (
                                self.historicCommands[j].commands[k],
                                self.historicCommands[j].commands[k - 1],
                            )
                            break

                    self.swapElements(i=i, j=(i - 1))
            else:
                # If element is not in a repeat command
                if isinstance(
                    self.historicCommandsView[i - 1], LabelFrame
                ) or isinstance(self.historicCommandsView[i - 1].master, LabelFrame):
                    # If above element or his master is repeat command

                    # Get the first repeat element
                    widget = self.historicCommandsView[i - 1]
                    while True:
                        if isinstance(widget.master, LabelFrame):
                            widget = widget.master
                        else:
                            break

                    j = self.historicCommandsView.index(widget)
                    self.historicCommands[j].commands.append(self.historicCommands[i])

                    # Recreate element
                    self.redrawCommand(i, self.historicCommands[j].visitorDrawEditor)
                else:
                    self.swapElements(i=i, j=(i - 1))

            print("\nMOVE UP")
            for command in self.historicCommands:
                print(command)
                if isinstance(command, commands.Repeat):
                    print("commands : ")
                    for command2 in command.commands:
                        print(f"\t{command2}")

            # Repaint all items
            for widget in self.historicCommandsView:
                widget.pack(expand=True, fill=BOTH)

    def checkIfLast(self, i):
        if isinstance(self.historicCommandsView[i].master, LabelFrame):
            return False

        if not isinstance(self.historicCommands[i], commands.Repeat):
            return i == len(self.historicCommands) - 1

        if len(self.historicCommands[i].commands) == 0:
            return i == len(self.historicCommands) - 1

        return self.checkIfLast(
            self.historicCommands.index(self.historicCommands[i].commands[-1])
        )

    def getElementAfter(self, i: int):
        initial = self.historicCommandsView[i]
        for j in range(i + 1, len(self.historicCommandsView)):
            if self.historicCommandsView[j].master == initial.master:
                return j
        return -1

    def moveDown(self):
        if self.focused != None:
            i = self.historicCommandsView.index(self.focused)

            if isinstance(
                self.historicCommands[i], commands.Repeat
            ) and self.checkIfLast(i):
                return

            for widget in self.historicCommandsView:
                widget.pack_forget()

            next = self.getElementAfter(i)
            if next == -1 or i == len(self.historicCommandsView) - 1:
                if isinstance(self.focused.master, LabelFrame):
                    j = self.historicCommandsView.index(self.focused.master)
                    self.historicCommands[j].commands.pop()

                    if isinstance(self.focused.master.master, LabelFrame):
                        k = self.historicCommandsView.index(self.focused.master.master)

                        for v in range(len(self.historicCommands[k].commands)):
                            if (
                                self.historicCommands[k].commands[v]
                                == self.historicCommands[j]
                            ):
                                self.historicCommands[k].commands.insert(
                                    v + 1, self.historicCommands[i]
                                )
                                break

                    # recreate the graphical element
                    self.redrawCommand(
                        i, commands.VisitorEditorVisualiser(self.focused.master.master)
                    )
            else:
                # If not the last element
                if isinstance(self.historicCommandsView[next], LabelFrame):
                    # If below element is a repeat command
                    if isinstance(self.focused.master, LabelFrame):
                        # If master is a repeat command

                        # Remove the command from parent
                        j = self.historicCommandsView.index(self.focused.master)
                        self.historicCommands[j].remove(self.historicCommands[i])

                        if (
                            self.focused.master
                            != self.historicCommandsView[next].master
                        ):
                            # If self.focused and below element are in the same repeat command

                            # recreate the graphical element
                            self.redrawCommand(
                                i,
                                commands.VisitorEditorVisualiser(
                                    self.historicCommands[next].master
                                ),
                            )
                        else:
                            # If self.focused and below element are in different repeat command

                            # Add command to repeat
                            self.historicCommands[next].commands.insert(
                                0, self.historicCommands[i]
                            )

                            # recreate the graphical element
                            self.redrawCommand(
                                i, self.historicCommands[next].visitorDrawEditor
                            )

                            self.swapElements(i=i, j=(i + 1))
                    else:
                        # If master is not a repeat command

                        # Add command to repeat
                        self.historicCommands[next].commands.insert(
                            0, self.historicCommands[i]
                        )

                        # recreate the graphical element
                        self.redrawCommand(
                            i, self.historicCommands[next].visitorDrawEditor
                        )

                        self.swapElements(i=i, j=(i + 1))
                else:
                    # If below element is not a repeat command
                    if isinstance(self.focused.master, LabelFrame):
                        # If master is repeat command
                        if (
                            self.focused.master
                            == self.historicCommandsView[next].master
                        ):
                            # If focused and below are in same repeat command
                            j = self.historicCommandsView.index(self.focused.master)
                            for k in range(len(self.historicCommands[j].commands)):
                                if (
                                    self.historicCommands[j].commands[k]
                                    == self.historicCommands[i]
                                ):
                                    (
                                        self.historicCommands[j].commands[k],
                                        self.historicCommands[j].commands[k + 1],
                                    ) = (
                                        self.historicCommands[j].commands[k + 1],
                                        self.historicCommands[j].commands[k],
                                    )
                                    break

                            self.swapElements(i=i, j=(i + 1))
                        else:
                            # If focused and below are not in same repeat command
                            j = self.historicCommandsView.index(self.focused.master)
                            self.historicCommands[j].commands.pop()

                            # recreate the graphical element
                            self.redrawCommand(
                                i,
                                commands.VisitorEditorVisualiser(
                                    self.historicCommandsView[next].master
                                ),
                            )
                    else:
                        # If master is not repeat command
                        self.swapElements(i=i, j=(i + 1))

            print("\nMOVE DOWN")
            for command in self.historicCommands:
                print(command)
                if isinstance(command, commands.Repeat):
                    print("commands : ")
                    for command2 in command.commands:
                        print(f"\t{command2}")

            # Repaint all items
            for widget in self.historicCommandsView:
                widget.pack(expand=True, fill=BOTH)

    def save(self):
        self.visitorSaveXML = commands.VisitorSaveXML()
        initialDir = (
            os.getcwd()
            if (self.lastSelectedFolder == None)
            else self.lastSelectedFolder
        )
        file = filedialog.asksaveasfile(initialdir=initialDir)

        if file != None:
            self.lastSelectedFolder = os.path.dirname(file.name)

            self.saveCommands(self.panelHistoricCommands, 0, file)
            file.close()

    def saveCommands(self, master, i: int, file):
        while i < len(self.historicCommandsView):
            if self.historicCommandsView[i].master != master:
                return i
            if isinstance(self.historicCommandsView[i], LabelFrame):
                file.write(f"<repeter fois={self.historicCommands[i].n}>\n")
                i = self.saveCommands(self.historicCommandsView[i], i + 1, file)
                file.write("</repeter>\n")
            else:
                file.write(self.historicCommands[i].save(self.visitorSaveXML) + "\n")
                i += 1
        return i

    def load(self):
        for widget in self.historicCommandsView:
            widget.pack_forget()
        self.historicCommandsView.clear()
        self.historicCommands.clear()

        initialDir = (
            os.getcwd()
            if (self.lastSelectedFolder == None)
            else self.lastSelectedFolder
        )

        file = filedialog.askopenfile(
            initialdir=initialDir,
            title="Select a File",
            filetypes=[("XML Files", "*.xml*")],
        )

        if file == None:
            return

        self.historicCommands = parseXML(file)

        for command in self.historicCommands:
            parent = (
                self.visitorHistoricField
                if command.parentRepeat == None
                else command.parentRepeat.visitorDrawEditor
            )
            widget = command.visualize(parent)
            widget.pack(expand=True, fill=BOTH)

            self.historicCommandsView.append(widget)

            for child in widget.winfo_children():
                if not isinstance(child, Entry):
                    child.bind(
                        "<Button-1>",
                        lambda event, widget=widget: self.saveFocused(widget),
                    )

    def play(self, master, i):
        while i < len(self.historicCommandsView):
            if self.historicCommandsView[i].master != master:
                return i
            if isinstance(self.historicCommandsView[i], LabelFrame):
                for j in range(self.historicCommands[i].n):
                    tmpI = self.play(self.historicCommandsView[i], i + 1)
                i = tmpI
            else:
                self.ivybus.send_msg(self.historicCommands[i].toLogo())
                i += 1
        return i

    def __init__(self, master: Toplevel) -> None:
        self.master = master
        master.geometry("500x250")
        master.title("Editeur")

        self.focused = None
        self.historicCommandsView = []
        self.historicCommands = []

        self.ivybus = MyAgent("Editor")

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
            commands.Clean: None,
            commands.FCC: None,
            commands.FCAP: None,
            commands.FPOS: None,
            commands.Repeat: None,
        }

        # Creation de la zone de saisie
        self.inputField = LabelFrame(
            self.master, text="Zone de saisie", padx=20, pady=20, labelanchor="n"
        )
        self.inputField.grid(row=0, column=0)

        # Création du visiteur qui permet de créer le rendu graphique des commandes
        self.visitorInputField = commands.VisitorEditorVisualiser(self.inputField)

        # Creation de la zone d'historique
        self.historicField = LabelFrame(self.master, text="Historique des commandes")
        self.historicField.grid(row=0, column=1)

        self.panelControlBtn = Frame(self.historicField)
        self.panelControlBtn.pack(side=RIGHT)
        self.btnDelete = Button(
            self.panelControlBtn, text="Delete", command=self.removeElement
        )
        self.btnDelete.pack()
        self.btnMoveUp = Button(self.panelControlBtn, text="⬆", command=self.moveUp)
        self.btnMoveUp.pack()
        self.btnMoveDown = Button(self.panelControlBtn, text="⬇", command=self.moveDown)
        self.btnMoveDown.pack()

        self.panelHistoricCommands = Frame(self.historicField)
        self.panelHistoricCommands.pack(side=RIGHT)

        # Création du visiteur qui permet de créer le rendu graphique des commandes
        self.visitorHistoricField = commands.VisitorEditorVisualiser(
            self.panelHistoricCommands
        )

        # Creation du panel de boutons
        self.panelBtn = Frame(self.master)
        self.panelBtn.grid(row=1, column=0, columnspan=2)

        self.btnSave = Button(self.panelBtn, text="Save", command=self.save)
        self.btnSave.pack(side=LEFT)
        self.btnLoad = Button(self.panelBtn, text="Load", command=self.load)
        self.btnLoad.pack(side=LEFT)
        self.btnExec = Button(
            self.panelBtn,
            text="Play",
            command=lambda: self.play(self.panelHistoricCommands, 0),
        )
        self.btnExec.pack(side=LEFT)

        for command in self.commands:
            # On récupère la représentation graphique de la commande
            item = command().visualize(self.visitorInputField)
            # A une commande est associée une représentation graphique
            self.commands[command] = item
            item.pack(expand=True, fill=BOTH)

            for child in item.winfo_children():
                if not isinstance(child, Entry):
                    child.bind(
                        "<Button-1>",
                        lambda event: self.copyCommand(
                            event.widget.master, self.visitorHistoricField
                        ),
                    )
