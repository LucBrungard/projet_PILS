from abc import ABC, abstractmethod

class Command(ABC):
   def __init__(self) -> None:
      super().__init__()
      self.name = self.__class__.__name__

   @abstractmethod
   def save(self, visitor):
      if (not isinstance(visitor, VisitorSave)):
         raise TypeError()
      pass

   @abstractmethod
   def visualize(self, visitor):
      if (not isinstance(visitor, VisitorVisualize)):
         raise TypeError()
      pass

   @abstractmethod
   def toLOGO(self):
      pass

class LiftPencil(Command):
   def save(self, visitor):
      super().save(visitor)
      return visitor.visitLiftPencil(self)

   def visualize(self, visitor):
      pass

   def toLOGO(self):
      return "LEVECRAYON"

class LowerPencil(Command):
   def save(self, visitor):
      super().save(visitor)
      return visitor.visitLowerPencil(self)
   
   def visualize(self, visitor):
      pass

   def toLOGO(self):
      return "BAISSECRAYON"

class Origin(Command):
   def save(self, visitor):
      super().save(visitor)
      return visitor.visitOrigin(self)

   def visualize(self, visitor):
      pass

   def toLOGO(self):
      return "ORIGINE"

class Restore(Command):
   def save(self, visitor):
      super().save(visitor)
      return visitor.visitRestore(self)

   def visualize(self, visitor):
      pass

   def toLOGO(self):
      return "RESTAURE"

class Clean(Command):
   def save(self, visitor):
      super().save(visitor)
      return visitor.visitClean(self)

   def visualize(self, visitor):
      pass

   def toLOGO(self):
      return "NETTOIE"

class CommandWithParameter(Command):
   def __init__(self, n) -> None:
      super().__init__()
      self.n = n

class Forward(CommandWithParameter):
   def __init__(self, n) -> None:
      super().__init__(n)
   
   def visualize(self, visitorVisualize):
      pass # TODO

   def save(self, visitor):
      super().save(visitor)
      return visitor.visitForward(self)

   def toLOGO(self):
      return f"AVANCER {self.n}"

class Backward(CommandWithParameter):
   def __init__(self, n) -> None:
      super().__init__(n)

   def visualize(self, visitorVisualize):
      super().visualize(visitorVisualize)

   def save(self, visitor):
      super().save(visitor)
      return visitor.visitBackward(self)

   def toLOGO(self):
      return f"RECULER {self.n}"

class TurnLeft(CommandWithParameter):
   def __init__(self, n) -> None:
      super().__init__(n)

   def visualize(self, visitorVisualize):
      super().visualize(visitorVisualize)

   def save(self, visitor):
      super().save(visitor)
      return visitor.visitTurnLeft(self)

   def toLOGO(self):
      return f"TOURNERGAUCHE {self.n}"

class TurnRight(CommandWithParameter):
   def __init__(self, n) -> None:
      super().__init__(n)

   def visualize(self, visitorVisualize):
      super().visualize(visitorVisualize)

   def save(self, visitor):
      super().save(visitor)
      return visitor.visitTurnRight(self)

   def toLOGO(self):
      return f"TOURNERDROITE {self.n}"


class VisitorCommands:
   @abstractmethod
   def visitForward(self, command: Forward):
      if (not isinstance(command, Forward)):
         raise TypeError()

   @abstractmethod
   def visitBackward(self, command: Backward):
      if (not isinstance(command, Backward)):
         raise TypeError()

   @abstractmethod
   def visitTurnLeft(self, command: TurnLeft):
      if (not isinstance(command, TurnLeft)):
         raise TypeError()

   @abstractmethod
   def visitTurnRight(self, command: TurnRight):
      if (not isinstance(command, TurnRight)):
         raise TypeError()

   @abstractmethod
   def visitLiftPencil(self, command: LiftPencil):
      if (not isinstance(command, LiftPencil)):
         raise TypeError()

   @abstractmethod
   def visitLowerPencil(self, command: LowerPencil):
      if (not isinstance(command, LowerPencil)):
         raise TypeError()

   @abstractmethod
   def visitOrigin(self, command: Origin):
      if (not isinstance(command, Origin)):
         raise TypeError()

   @abstractmethod
   def visitRestore(self, command: Restore):
      if (not isinstance(command, Restore)):
         raise TypeError()

   @abstractmethod
   def visitClean(self, command: Clean):
      if (not isinstance(command, Clean)):
         raise TypeError()

class VisitorSave(VisitorCommands):
   pass

class VisitorSaveXML(VisitorSave):
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

class VisitorVisualize(VisitorCommands):
   pass


if __name__ == "__main__":
   print("Test class Command")
   try:
      command = Command()
      raise SyntaxError("Class command should not be instanciated")
   except TypeError as e:
      print("Works fine !\n")

   print("Test class CommandWithParameter")
   try:
      command = CommandWithParameter()
      raise SyntaxError("Class CommandWithParameter should not be instanciated")
   except TypeError as e:
      print("Works fine !\n")

   visitorSaveXML = VisitorSaveXML()

   print("Test class Forward")
   command = Forward(50)
   print(command.save(visitorSaveXML))
   print(command.toLOGO())
   print()

   print("Test class Backward")
   command = Backward(50)
   print(command.save(visitorSaveXML))
   print(command.toLOGO())
   print()

   print("Test class TurnLeft")
   command = TurnLeft(50)
   print(command.save(visitorSaveXML))
   print(command.toLOGO())
   print()

   print("Test class TurnRight")
   command = TurnRight(50)
   print(command.save(visitorSaveXML))
   print(command.toLOGO())
   print()

   print("Test class LiftPencil")
   command = LiftPencil()
   print(command.save(visitorSaveXML))
   print(command.toLOGO())
   print()

   print("Test class LowerPencil")
   command = LowerPencil()
   print(command.save(visitorSaveXML))
   print(command.toLOGO())
   print()

   print("Test class Origin")
   command = Origin()
   print(command.save(visitorSaveXML))
   print(command.toLOGO())
   print()

   print("Test class Restore")
   command = Restore()
   print(command.save(visitorSaveXML))
   print(command.toLOGO())
   print()

   print("Test class Clean")
   command = Clean()
   print(command.save(visitorSaveXML))
   print(command.toLOGO())
   print()
