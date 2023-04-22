from __future__ import annotations
from abc import ABC, abstractmethod
import collections.abc
from tkinter import *

##################################################
############ COMMAND WITHOUT PARAMETER ###########
##################################################


class Command(ABC):
    """Abstract class to describe a command"""

    def __init__(self) -> None:
        super().__init__()
        self.name = self.__class__.__name__
        self.parentRepeat = None

    @abstractmethod
    def save(self, visitor: VisitorSave) -> str:
        """Return the textual representation of the command to be saved

        Args:
            visitor (VisitorSave): A visitor

        Raises:
            TypeError: If the visitor is not a subtype of VisitorSave
        """
        if not isinstance(visitor, VisitorSave):
            raise TypeError()

    @abstractmethod
    def visualize(self, visitor: VisitorVisualize) -> None | Frame:
        """Draw the graphical representation of a command

        Args:
            visitor (VisitorVisualize): A visitor

        Raises:
            TypeError: If the visitor is not a subtype of VisitorVisualize
        """
        if not isinstance(visitor, VisitorVisualize):
            raise TypeError()

    @abstractmethod
    def toLogo(self) -> str:
        """Return the textual representation of the command to be sent on ivy bus"""
        pass


class LiftPencil(Command):
    def save(self, visitor):
        super().save(visitor)
        return visitor.visitLiftPencil(self)

    def visualize(self, visitor):
        super().visualize(visitor)
        return visitor.visitLiftPencil(self)

    def toLogo(self):
        return "LEVECRAYON"


class LowerPencil(Command):
    def save(self, visitor):
        super().save(visitor)
        return visitor.visitLowerPencil(self)

    def visualize(self, visitor):
        super().visualize(visitor)
        return visitor.visitLowerPencil(self)

    def toLogo(self):
        return "BAISSECRAYON"


class Origin(Command):
    def save(self, visitor):
        super().save(visitor)
        return visitor.visitOrigin(self)

    def visualize(self, visitor):
        super().visualize(visitor)
        return visitor.visitOrigin(self)

    def toLogo(self):
        return "ORIGINE"


class Restore(Command):
    def save(self, visitor):
        super().save(visitor)
        return visitor.visitRestore(self)

    def visualize(self, visitor):
        super().visualize(visitor)
        return visitor.visitRestore(self)

    def toLogo(self):
        return "RESTAURE"


class Clean(Command):
    def save(self, visitor):
        super().save(visitor)
        return visitor.visitClean(self)

    def visualize(self, visitor):
        super().visualize(visitor)
        return visitor.visitClean(self)

    def toLogo(self) -> str:
        return "NETTOIE"


##################################################
############   COMMAND WITH PARAMETER  ###########
##################################################


class CommandWithParameter(Command):
    """Abstract class. Represent the commands with a parameter"""

    def __init__(self, n) -> None:
        super().__init__()
        self.n = n


class Forward(CommandWithParameter):
    def __init__(self, n=50) -> None:
        super().__init__(n)

    def visualize(self, visitor):
        super().visualize(visitor)
        return visitor.visitForward(self)

    def save(self, visitor):
        super().save(visitor)
        return visitor.visitForward(self)

    def toLogo(self) -> str:
        return f"AVANCE {self.n}"


class Backward(CommandWithParameter):
    def __init__(self, n=50) -> None:
        super().__init__(n)

    def visualize(self, visitor):
        super().visualize(visitor)
        return visitor.visitBackward(self)

    def save(self, visitor):
        super().save(visitor)
        return visitor.visitBackward(self)

    def toLogo(self) -> str:
        return f"RECULE {self.n}"


class TurnLeft(CommandWithParameter):
    def __init__(self, n=90) -> None:
        super().__init__(n)

    def visualize(self, visitor):
        super().visualize(visitor)
        return visitor.visitTurnLeft(self)

    def save(self, visitor):
        super().save(visitor)
        return visitor.visitTurnLeft(self)

    def toLogo(self) -> str:
        return f"TOURNEGAUCHE {self.n}"


class TurnRight(CommandWithParameter):
    def __init__(self, n=90) -> None:
        super().__init__(n)

    def visualize(self, visitor):
        super().visualize(visitor)
        return visitor.visitTurnRight(self)

    def save(self, visitor):
        super().save(visitor)
        return visitor.visitTurnRight(self)

    def toLogo(self) -> str:
        return f"TOURNEDROITE {self.n}"


class FCC(CommandWithParameter):
    def __init__(self, n=[0, 0, 0]) -> None:
        super().__init__(n)
        if not isinstance(n, collections.abc.Sequence):
            raise ValueError()

    def visualize(self, visitor):
        super().visualize(visitor)
        return visitor.visitFCC(self)

    def save(self, visitor):
        super().save(visitor)
        return visitor.visitFCC(self)

    def toLogo(self) -> str:
        return f"FCC {self.n[0]} {self.n[1]} {self.n[2]}"


class FCAP(CommandWithParameter):
    def __init__(self, n=90) -> None:
        super().__init__(n)

    def visualize(self, visitor):
        super().visualize(visitor)
        return visitor.visitFCAP(self)

    def save(self, visitor):
        super().save(visitor)
        return visitor.visitFCAP(self)

    def toLogo(self) -> str:
        return f"FCAP {self.n}"


class FPOS(CommandWithParameter):
    def __init__(self, n=[0, 0]) -> None:
        super().__init__(n)
        if not isinstance(n, collections.abc.Sequence):
            raise ValueError()

    def visualize(self, visitor):
        super().visualize(visitor)
        return visitor.visitFPOS(self)

    def save(self, visitor):
        super().save(visitor)
        return visitor.visitFPOS(self)

    def toLogo(self) -> str:
        return f"FPOS {self.n[0]} {self.n[1]}"


class Repeat(CommandWithParameter):
    def __init__(self, n=5) -> None:
        super().__init__(n)
        self.commands = []
        self.visitorDrawEditor = None

    def visualize(self, visitor):
        super().visualize(visitor)
        return visitor.visitRepeat(self)

    def save(self, visitor):
        super().save(visitor)
        return visitor.visitRepeat(self)

    def toLogo(self) -> str:
        res = f"REPETE {self.n} [\n\t"
        for command in self.commands:
            res += f"{command.toLogo()}\n\t"
        return res + "]"


##################################################
############        VISITORS           ###########
##################################################


class VisitorCommands(ABC):
    """Abstract class. A visitor to handle each command interaction"""

    @abstractmethod
    def visitForward(self, command: Forward):
        if not isinstance(command, Forward):
            raise TypeError()

    @abstractmethod
    def visitBackward(self, command: Backward):
        if not isinstance(command, Backward):
            raise TypeError()

    @abstractmethod
    def visitTurnLeft(self, command: TurnLeft):
        if not isinstance(command, TurnLeft):
            raise TypeError()

    @abstractmethod
    def visitTurnRight(self, command: TurnRight):
        if not isinstance(command, TurnRight):
            raise TypeError()

    @abstractmethod
    def visitLiftPencil(self, command: LiftPencil):
        if not isinstance(command, LiftPencil):
            raise TypeError()

    @abstractmethod
    def visitLowerPencil(self, command: LowerPencil):
        if not isinstance(command, LowerPencil):
            raise TypeError()

    @abstractmethod
    def visitOrigin(self, command: Origin):
        if not isinstance(command, Origin):
            raise TypeError()

    @abstractmethod
    def visitRestore(self, command: Restore):
        if not isinstance(command, Restore):
            raise TypeError()

    @abstractmethod
    def visitClean(self, command: Clean):
        if not isinstance(command, Clean):
            raise TypeError()

    @abstractmethod
    def visitFCC(self, command: FCC):
        if not isinstance(command, FCC):
            raise TypeError()

    @abstractmethod
    def visitFCAP(self, command: FCAP):
        if not isinstance(command, FCAP):
            raise TypeError()

    @abstractmethod
    def visitFPOS(self, command: FPOS):
        if not isinstance(command, FPOS):
            raise TypeError()

    @abstractmethod
    def visitRepeat(self, command: Repeat):
        if not isinstance(command, Repeat):
            raise TypeError()


##################################################
############      VISITORS  SAVE       ###########
##################################################
class VisitorSave(VisitorCommands):
    """Abstract class. A visitor to save commands as text."""

    pass


class VisitorSaveXML(VisitorSave):
    """Concrete class. A visitor to save commands as XML text."""

    def visitForward(self, command):
        super().visitForward(command)
        return f"<avancer dist={command.n}>"

    def visitBackward(self, command):
        super().visitBackward(command)
        return f"<reculer dist={command.n}>"

    def visitTurnLeft(self, command):
        super().visitTurnLeft(command)
        return f"<gauche angle={command.n}>"

    def visitTurnRight(self, command):
        super().visitTurnRight(command)
        return f"<droite angle={command.n}>"

    def visitLiftPencil(self, command):
        super().visitLiftPencil(command)
        return "<lever>"

    def visitLowerPencil(self, command):
        super().visitLowerPencil(command)
        return "<baisser>"

    def visitOrigin(self, command):
        super().visitOrigin(command)
        return "<origine>"

    def visitRestore(self, command):
        super().visitRestore(command)
        return "<restaurer>"

    def visitClean(self, command):
        super().visitClean(command)
        return "<nettoyer>"

    def visitFCC(self, command):
        super().visitFCC(command)
        return f"<crayon rouge={command.n[0]} vert={command.n[1]} bleu={command.n[2]}>"

    def visitFCAP(self, command):
        super().visitFCAP(command)
        return f"<cap angle={command.n}>"

    def visitFPOS(self, command):
        super().visitFPOS(command)
        return f"<position x={command.n[0]} y={command.n[1]}>"

    def visitRepeat(self, command):
        super().visitRepeat(command)
        # res = f"<repeter fois={command.n}>\n"

        # for command in command.commands:
        #     res += f"{command.save(self)}\n"

        # res += "</repeter>"

        return ""


##################################################
############    VISITORS VISUALIZER    ###########
##################################################


class VisitorVisualize(VisitorCommands):
    """Abstract class. A visitor to draw commands"""

    def __init__(self, parent: Toplevel) -> None:
        """Constructor

        Args:
            parent (TopLevel): The main window
        """
        super().__init__()
        self.parent = parent


class VisitorEditorVisualiser(VisitorVisualize):
    """Concrete class. A visitor to draw graphical commands' representation on user's editor"""

    def __init__(self, parent: Toplevel) -> None:
        """Constructor

        Args:
            parent (TopLevel): The main window
        """
        super().__init__(parent)

    def updateValue(self, command: CommandWithParameter, stringVar: StringVar):
        try:
            command.n = int(stringVar.get())
        except ValueError:
            command.n = 0

    def visitForward(self, command: Forward):
        super().visitForward(command)
        frame = Frame(self.parent, bd=2, relief=RAISED, cursor="hand2")
        frame.columnconfigure((0, 1, 2), weight=1)

        label = Label(frame, text="Avancer de ")
        label.grid(row=0, column=0, sticky="nswe")

        stringVar = StringVar()
        stringVar.trace(
            "w", lambda a, b, c, sv=stringVar: self.updateValue(command, sv)
        )
        entry = Entry(frame, width=5, justify=CENTER, textvariable=stringVar)
        entry.insert(0, command.n)
        entry.grid(row=0, column=1, sticky="nswe")

        label = Label(frame, text=" pas")
        label.grid(row=0, column=2, sticky="nswe")

        return frame

    def visitBackward(self, command: Backward):
        super().visitBackward(command)
        frame = Frame(self.parent, bd=2, relief=RAISED, cursor="hand2")
        frame.columnconfigure((0, 1, 2), weight=1)

        label = Label(frame, text="Reculer de ")
        label.grid(row=0, column=0, sticky="nswe")

        stringVar = StringVar()
        stringVar.trace(
            "w", lambda a, b, c, sv=stringVar: self.updateValue(command, sv)
        )
        entry = Entry(frame, width=5, justify=CENTER, textvariable=stringVar)
        entry.insert(0, command.n)
        entry.grid(row=0, column=1, sticky="nswe")

        label = Label(frame, text=" pas")
        label.grid(row=0, column=2, sticky="nswe")

        return frame

    def visitTurnLeft(self, command: TurnLeft):
        super().visitTurnLeft(command)
        frame = Frame(self.parent, bd=2, relief=RAISED, cursor="hand2")
        frame.columnconfigure((0, 1, 2), weight=1)

        label = Label(frame, text="Rotation gauche de ")
        label.grid(row=0, column=0, sticky="nswe")

        stringVar = StringVar()
        stringVar.trace(
            "w", lambda a, b, c, sv=stringVar: self.updateValue(command, sv)
        )
        entry = Entry(frame, width=5, justify=CENTER, textvariable=stringVar)
        entry.insert(0, command.n)
        entry.grid(row=0, column=1, sticky="nswe")

        label = Label(frame, text=" degrés")
        label.grid(row=0, column=2, sticky="nswe")

        return frame

    def visitTurnRight(self, command: TurnRight):
        super().visitTurnRight(command)
        frame = Frame(self.parent, bd=2, relief=RAISED, cursor="hand2")
        frame.columnconfigure((0, 1, 2), weight=1)

        label = Label(frame, text="Rotation droite de ")
        label.grid(row=0, column=0, sticky="nswe")

        stringVar = StringVar()
        stringVar.trace(
            "w", lambda a, b, c, sv=stringVar: self.updateValue(command, sv)
        )
        entry = Entry(frame, width=5, justify=CENTER, textvariable=stringVar)
        entry.insert(0, command.n)
        entry.grid(row=0, column=1, sticky="nswe")

        label = Label(frame, text=" degrés")
        label.grid(row=0, column=2, sticky="nswe")

        return frame

    def visitLiftPencil(self, command: LiftPencil):
        super().visitLiftPencil(command)
        frame = Frame(self.parent, bd=2, relief=RAISED, cursor="hand2")

        label = Label(frame, text="Lever le crayon")
        label.pack(expand=True, fill=BOTH)

        return frame

    def visitLowerPencil(self, command: LowerPencil):
        super().visitLowerPencil(command)
        frame = Frame(self.parent, bd=2, relief=RAISED, cursor="hand2")

        label = Label(frame, text="Baisser le crayon")
        label.pack(expand=True, fill=BOTH)

        return frame

    def visitOrigin(self, command: Origin):
        super().visitOrigin(command)
        frame = Frame(self.parent, bd=2, relief=RAISED, cursor="hand2")

        label = Label(frame, text="Retour au centre")
        label.pack(expand=True, fill=BOTH)

        return frame

    def visitRestore(self, command: Restore):
        super().visitRestore(command)
        frame = Frame(self.parent, bd=2, relief=RAISED, cursor="hand2")

        label = Label(frame, text="Réinitialisation")
        label.pack(expand=True, fill=BOTH)

        return frame

    def visitClean(self, command: Clean):
        super().visitClean(command)
        frame = Frame(self.parent, bd=2, relief=RAISED, cursor="hand2")

        label = Label(frame, text="Effacer les traces")
        label.pack(expand=True, fill=BOTH)

        return frame

    def visitFCC(self, command: FCC):
        def updateR(*args):
            try:
                command.n[0] = int(stringVarR.get())
            except ValueError:
                command.n[0] = 0

        def updateG(*args):
            try:
                command.n[1] = int(stringVarG.get())
            except ValueError:
                command.n[1] = 0

        def updateB(*args):
            try:
                command.n[2] = int(stringVarB.get())
            except ValueError:
                command.n[2] = 0

        super().visitFCC(command)
        frame = Frame(self.parent, bd=2, relief=RAISED, cursor="hand2")
        frame.columnconfigure((0, 1, 2, 3), weight=1)

        label = Label(frame, text="FCC ")
        label.grid(row=0, column=0, sticky="nswe")

        stringVarR = StringVar()
        stringVarR.trace("w", updateR)
        entryR = Entry(frame, width=5, justify=CENTER, textvariable=stringVarR)
        entryR.insert(0, command.n[0])
        entryR.grid(row=0, column=1, sticky="nswe")

        stringVarG = StringVar()
        stringVarG.trace("w", updateG)
        entryG = Entry(frame, width=5, justify=CENTER, textvariable=stringVarG)
        entryG.insert(0, command.n[1])
        entryG.grid(row=0, column=2, sticky="nswe")

        stringVarB = StringVar()
        stringVarB.trace("w", updateB)
        entryB = Entry(frame, width=5, justify=CENTER, textvariable=stringVarB)
        entryB.insert(0, command.n[2])
        entryB.grid(row=0, column=3, sticky="nswe")

        return frame

    def visitFCAP(self, command: FCAP):
        super().visitFCAP(command)
        frame = Frame(self.parent, bd=2, relief=RAISED, cursor="hand2")
        frame.columnconfigure((0, 1, 2), weight=1)

        label = Label(frame, text="FCAP ")
        label.grid(row=0, column=0, sticky="nswe")

        stringVar = StringVar()
        stringVar.trace(
            "w", lambda a, b, c, sv=stringVar: self.updateValue(command, sv)
        )
        entry = Entry(frame, width=5, justify=CENTER, textvariable=stringVar)
        entry.insert(0, command.n)
        entry.grid(row=0, column=1, sticky="nswe")

        label = Label(frame, text=" degrés")
        label.grid(row=0, column=2, sticky="nswe")

        return frame

    def visitFPOS(self, command: FPOS):
        def updateX(*args):
            try:
                command.n[0] = int(stringVarX.get())
            except ValueError:
                command.n[0] = 0

        def updateY(*args):
            try:
                command.n[1] = int(stringVarY.get())
            except ValueError:
                command.n[1] = 0

        super().visitFPOS(command)
        frame = Frame(self.parent, bd=2, relief=RAISED, cursor="hand2")
        frame.columnconfigure((0, 1, 2, 3), weight=1)

        label = Label(frame, text="FPOS ")
        label.grid(row=0, column=0, sticky="nswe")

        stringVarX = StringVar()
        stringVarX.trace("w", updateX)
        entryX = Entry(frame, width=5, justify=CENTER, textvariable=stringVarX)
        entryX.insert(0, command.n[0])
        entryX.grid(row=0, column=1, sticky="nswe")

        stringVarY = StringVar()
        stringVarY.trace("w", updateY)
        entryY = Entry(frame, width=5, justify=CENTER, textvariable=stringVarY)
        entryY.insert(0, command.n[1])
        entryY.grid(row=0, column=2, sticky="nswe")

        return frame

    def visitRepeat(self, command: Repeat):
        super().visitRepeat(command)

        res = LabelFrame(self.parent, cursor="hand2", padx=10, pady=10, relief=RAISED)
        Label(res, text="Placer vos commandes ci-dessous").pack()

        # region CONFIGURE LABEL WIDGET
        labelWidget = Frame(res)

        textLW = Label(labelWidget, text="Repete ")
        textLW.pack(side=LEFT)

        stringVar = StringVar()
        stringVar.trace(
            "w", lambda a, b, c, sv=stringVar: self.updateValue(command, sv)
        )
        entry = Entry(labelWidget, width=5, justify=CENTER, textvariable=stringVar)
        entry.insert(0, command.n)
        entry.pack(side=LEFT)

        textLW = Label(labelWidget, text="fois")
        textLW.pack(side=LEFT)

        res.configure(labelwidget=labelWidget)
        # endregion

        command.visitorDrawEditor = VisitorEditorVisualiser(res)

        return res


class VisitorVisualizer(VisitorVisualize):
    """Abstract class. A visitor to draw commands on a visualizer"""

    # TODO faire que les visualiseurs ne puissent pas appeler la commande boucle


class VisitorTextualVisualizer(VisitorVisualizer):
    pass


class VisitorGraphicalVisualizer(VisitorVisualizer):
    pass
