from tkinter import *
from PIL import Image, ImageTk
import math

COORDS_ORIGIN = [300, 300]


class Tortue:
   def __init__(self):
      self.angle = (270 % 360)  # en degre

      self.vitesse = 1
      self.trace = True
      self.coord = COORDS_ORIGIN
      self.changerCouleur([0, 0, 0])  # noir

    #   image = Image.open("tortue.png")
    #   self.image = ImageTk.PhotoImage(image.resize((30, 30)))

   def image(self, canvas: Canvas):
      self.canvas = canvas

      self.imageAngle = (360 % 360)

      self.imageDebut = Image.open("tortue.png")
      redim_image = self.imageDebut.resize((30, 30))
      self.imageFin = ImageTk.PhotoImage(redim_image)

      self.dessinImage = self.canvas.create_image(
          self.coord[0], self.coord[1], anchor=NW, image=self.imageFin)

   def restaurer(self):
      self.canvas.delete("all")

      self.angle = (270 % 360)
      self.imageAngle = (360 % 360)
      self.coord = [200, 200]
      self.trace = True

      self.image(self.canvas)

   def nettoyer(self):
      self.canvas.delete("all")
      self.dessinImage = self.canvas.create_image(
          self.coord[0], self.coord[1], anchor=NW, image=self.imageFin)

   def origine(self):
      self.canvas.delete(self.dessinImage)

      redim_image = self.imageDebut.resize((30, 30))
      self.imageFin = ImageTk.PhotoImage(redim_image)

      self.angle = (270 % 360)
      self.imageAngle = (360 % 360)
      self.coord = COORDS_ORIGIN

      self.dessinImage = self.canvas.create_image(
          self.coord[0], self.coord[1], anchor=NW, image=self.imageFin)

   def avancer(self, compteur, n, debut):
      angle_radian = self.angle * math.pi / 180

      self.canvas.move(self.dessinImage, self.vitesse *
                       math.cos(angle_radian), self.vitesse * math.sin(angle_radian))

      ligne = self.canvas.create_line(
          debut[0], debut[1], debut[0], debut[1], fill=self.couleur)

      if compteur != n:
         self.canvas.after(30, self.avancer, compteur+1, n, debut)
         self.coord = self.canvas.coords(self.dessinImage)

         if self.trace:
            self.canvas.coords(ligne, debut[0], debut[1],
                               (self.coord[0] + (self.coord[0] + 30)) / 2, (self.coord[1] + (self.coord[1] + 30)) / 2)

      '''else :      
         self.canvas.create_line(self.coord[0], self.coord[1], self.coord[0] + 30, self.coord[1] +30)'''

   def reculer(self, compteur, n, debut):
      angle_radian = self.angle * math.pi / 180

      self.canvas.move(self.dessinImage, -self.vitesse *
                       math.cos(angle_radian), -self.vitesse * math.sin(angle_radian))

      ligne = self.canvas.create_line(
          debut[0], debut[1], debut[0], debut[1], fill=self.couleur)

      if compteur != n:
         self.canvas.after(30, self.reculer, compteur+1, n, debut)
         self.coord = self.canvas.coords(self.dessinImage)

         if self.trace:
            self.canvas.coords(ligne, debut[0], debut[1],
                               (self.coord[0] + (self.coord[0] + 30)) / 2, (self.coord[1] + (self.coord[1] + 30)) / 2)

   def tourner(self, n):

      if n != 0:
         if (-n) > 0:
            self.angle = ((self.angle - 1) % 360)
            self.imageAngle = ((self.imageAngle + 1) % 360)
         else:
            self.angle = ((self.angle + 1) % 360)
            self.imageAngle = ((self.imageAngle - 1) % 360)

         self.canvas.delete(self.dessinImage)
         rotated_image = self.imageDebut.rotate(self.imageAngle, expand=True)
         redim_image = rotated_image.resize((30, 30))
         self.imageFin = ImageTk.PhotoImage(redim_image)
         self.dessinImage = self.canvas.create_image(
             self.coord[0], self.coord[1], anchor=NW, image=self.imageFin)

         if n > 0:
            self.canvas.after(30, self.tourner, n-1)
         else:
            self.canvas.after(30, self.tourner, n+1)

   def leverCrayon(self):
      self.trace = False

   def baisserCrayon(self):
      self.trace = True

   def changerCouleur(self, rgb):
      try:
         r, g, b = rgb[0], rgb[1], rgb[2]
      except:
         print("Pas assez d'arguments")

      self.couleur = f'#{r:02x}{g:02x}{b:02x}'

   def fixerPos(self, coord):
      self.canvas.delete(self.dessinImage)
      self.coord = coord
      self.dessinImage = self.canvas.create_image(
          self.coord[0], self.coord[1], anchor=NW, image=self.imageFin)
