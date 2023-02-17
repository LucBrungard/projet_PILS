from abc import ABC, abstractmethod
import sys
import pathlib

# Add the parent folder toPYTHONPATH to import from sibling folder
sys.path.insert(0,
                str(pathlib.Path(__file__).parent.parent.absolute()))
from visitors.visitorCommands import *


class Command(ABC):
   def __init__(self) -> None:
      super().__init__()
      self.name = self.__class__.__name__

   @ abstractmethod
   def visualize(self, visitorVisualize):
      if (not isinstance(visitorVisualize, VisitorVisualize)):
         raise TypeError("Should be of type VisitorVisualize")
      print("visualize")

   @ abstractmethod
   def save(self, visitorSave):
      if (not isinstance(visitorSave, VisitorSave)):
         raise TypeError("Should be of type VisitorSave")
      print("save")

   @ abstractmethod
   def toLOGO(self):
      print("toLOGO")


if __name__ == "__main__":
   print("Test abstract class")
   try:
      command = Command("name")
      raise SyntaxError("Class command should not be instanciated")
   except TypeError as e:
      print("Works fine !")
