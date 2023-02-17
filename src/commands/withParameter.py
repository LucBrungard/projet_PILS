from command import Command
from abc import ABC, abstractmethod
import sys
import pathlib

# Add the parent folder toPYTHONPATH to import from sibling folder
sys.path.insert(0,
                str(pathlib.Path(__file__).parent.parent.absolute()))
from visitors.visitorCommands import *


class CommandWithParameter(Command):
   def __init__(self, n) -> None:
      super().__init__()
      self.n = n

   @ abstractmethod
   def visualize(self, visitorVisualize):
      super().visualize(visitorVisualize)

   @ abstractmethod
   def save(self, visitorSave):
      super().save(visitorSave)

   @ abstractmethod
   def toLOGO(self):
      super().toLOGO()


class Forward(CommandWithParameter):
   def __init__(self, n) -> None:
      super().__init__(n)
   
   def visualize(self, visitorVisualize):
      super().visualize(visitorVisualize)

   def save(self, visitorSave):
      super().save(visitorSave)

   def toLOGO(self):
      super().toLOGO()


class Backward(CommandWithParameter):
   def __init__(self, n) -> None:
      super().__init__(n)

   def visualize(self, visitorVisualize):
      super().visualize(visitorVisualize)

   def save(self, visitorSave):
      super().save(visitorSave)

   def toLOGO(self):
      super().toLOGO()


class TurnLeft(CommandWithParameter):
   def __init__(self, n) -> None:
      super().__init__(n)

   def visualize(self, visitorVisualize):
      super().visualize(visitorVisualize)

   def save(self, visitorSave):
      super().save(visitorSave)

   def toLOGO(self):
      super().toLOGO()


class TurnRight(CommandWithParameter):
   def __init__(self, n) -> None:
      super().__init__(n)

   def visualize(self, visitorVisualize):
      super().visualize(visitorVisualize)

   def save(self, visitorSave):
      super().save(visitorSave)

   def toLOGO(self):
      super().toLOGO()


if __name__ == "__main__":
   print("Test abstract class")
   try:
      command = CommandWithParameter("name")
      raise SyntaxError("Class CommandWithParameter should not be instanciated")
   except TypeError as e:
      print("Works fine !\n")

   visitorSave = VisitorSave()
   visitorVisualize = VisitorVisualize()

   print("Test class Forward")
   command = Forward(10)
   command.save(visitorSave)
   command.visualize(visitorVisualize)
   command.toLOGO()
   try:
      command.save("visitorSave")
      raise SyntaxError("Command save should be called with argument of type VisitorSave")
   except TypeError as e:
      pass
   try:
      command.visualize("visitorVisualize")
      raise SyntaxError("Command visualize should be called with argument of type VisitorSave")
   except TypeError as e:
      pass
   print("Works fine !\n")

   print("Test class Backward")
   command = Backward(10)
   command.save(visitorSave)
   command.visualize(visitorVisualize)
   command.toLOGO()
   try:
      command.save("visitorSave")
      raise SyntaxError("Command save should be called with argument of type VisitorSave")
   except TypeError as e:
      pass
   try:
      command.visualize("visitorVisualize")
      raise SyntaxError("Command visualize should be called with argument of type VisitorSave")
   except TypeError as e:
      pass
   print("Works fine !\n")

   print("Test class TurnLeft")
   command = TurnLeft(10)
   command.save(visitorSave)
   command.visualize(visitorVisualize)
   command.toLOGO()
   try:
      command.save("visitorSave")
      raise SyntaxError("Command save should be called with argument of type VisitorSave")
   except TypeError as e:
      pass
   try:
      command.visualize("visitorVisualize")
      raise SyntaxError("Command visualize should be called with argument of type VisitorSave")
   except TypeError as e:
      pass
   print("Works fine !\n")

   print("Test class TurnRight")
   command = TurnRight(10)
   command.save(visitorSave)
   command.visualize(visitorVisualize)
   command.toLOGO()
   try:
      command.save("visitorSave")
      raise SyntaxError("Command save should be called with argument of type VisitorSave")
   except TypeError as e:
      pass
   try:
      command.visualize("visitorVisualize")
      raise SyntaxError("Command visualize should be called with argument of type VisitorSave")
   except TypeError as e:
      pass
   print("Works fine !\n")
