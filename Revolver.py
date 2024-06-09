import pygame
from pygame.locals import *

from objloader import OBJ
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import random
import math

class Revolver:
    def __init__(self, scale, playerPosition, playerDirection):
        self.scale = scale
        self.distance = 2
        self.hitbox = 12
        self.Direction = playerDirection
        self.Direction = self.Direction / np.linalg.norm(self.Direction)
        self.Direction = self.Direction / np.linalg.norm(self.Direction)
        self.Direction *= self.distance
        self.Position = playerPosition + self.Direction
        self.obj = OBJ("revolver.obj", swapyz=True)
        self.obj.generate()

        
    def update(self, playerPosition, playerDirection):
        self.Direction = playerDirection
        self.Direction = self.Direction / np.linalg.norm(self.Direction)
        self.Direction = self.Direction / np.linalg.norm(self.Direction)
        self.Direction *= self.distance
        self.Position = playerPosition + self.Direction



    def calculateRotationAngleXZ(self):
        # Calculate the angle in degrees between the direction vector and the positive z-axis
        angle = math.degrees(math.atan2(self.Direction[0], self.Direction[2]))
        return angle
    
    def calculateRotationAngleXY(self):
        # Calculate the angle in degrees between the direction vector and the positive z-axis in the YZ plane
        angle = math.degrees(math.atan2(self.Direction[0], self.Direction[1]))
        return angle
    
    def calculateRotationAngleYZ(self):
        # Calculate the angle in degrees between the direction vector and the positive z-axis in the YZ plane
        angle = math.degrees(math.atan(self.Direction[1] / self.Direction[2]))  # Using atan for YZ plane
        return angle
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1] - 0.75, self.Position[2])
        glScaled(self.scale,self.scale,self.scale)
        glColor3f(1.0, 1.0, 1.0)
        angleXZ = self.calculateRotationAngleXZ()
        angleYZ = self.calculateRotationAngleYZ()
        angleXY = self.calculateRotationAngleXY()
        glRotatef(angleXZ - 90, 0.0, 1.0, 0.0)
        # glRotatef(angleYZ, 1.0, 0.0, 0.0)

        # glRotatef(-90.0, 1.0, 0.0, 0.0)
        self.obj.render()
        glPopMatrix()
        
        