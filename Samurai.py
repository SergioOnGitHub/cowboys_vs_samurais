import pygame
from pygame.locals import *

from objloader import OBJ
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import random
import math

class Samurai:
    def __init__(self, dim, scale):
        # Initialize the coordinates of the cube vertices
        self.points = np.array([
            [-1.0, -1.0,  1.0], [ 1.0, -1.0,  1.0], [ 1.0, -1.0, -1.0], [-1.0, -1.0, -1.0],
            [-1.0,  1.0,  1.0], [ 1.0,  1.0,  1.0], [ 1.0,  1.0, -1.0], [-1.0,  1.0, -1.0]
        ])
        self.scale = scale
        self.radius = 20
        self.DimBoard = dim
        self.vel = 2
        self.Position = [random.randint(-1 * self.DimBoard, self.DimBoard), 0, random.randint(-1 * self.DimBoard, self.DimBoard)]
        self.Direction = [random.random(), self.scale, random.random()]
        self.Direction[0] /= math.sqrt(self.Direction[0]**2 + self.Direction[2]**2)
        self.Direction[2] /= math.sqrt(self.Direction[0]**2 + self.Direction[2]**2)
        self.Direction[0] *= self.vel
        self.Direction[2] *= self.vel
        self.player_collision = False
        self.bullet_collision = False
        self.existence = True
        self.activation_zone = 100
        self.obj = OBJ("Samurai_low_poly.obj", swapyz=True)
        self.obj.generate()

    def get_position(self):
        return np.array(self.Position)

    def get_radius(self):
        return self.radius

    def on_hit(self):
        self.bullet_collision = True
        self.existence = False
        print("Samurai Position: ", self.Position)
        print("Samurai hit!")

        # Handle what happens when the samurai is hit

    def collisionDetection(self, playerPosition, playerRadius):
        distance = np.linalg.norm(self.get_position() - playerPosition)
        if distance < self.radius + playerRadius:
            print("Player has lost")
            return True
        return False
        

    def activate_zone(self, playerPosition):
        distance = np.linalg.norm(self.get_position() - playerPosition)
        return distance < self.activation_zone
        
    def update(self, playerPosition, playerDirection, playerRadius):
        if self.activate_zone(np.array(playerPosition)):
            self.Direction = np.array(playerDirection) * -1
            self.Direction /= np.linalg.norm(self.Direction)
            self.Direction *= self.vel
            self.Position[0] += self.Direction[0]
            self.Position[2] += self.Direction[2]
        else:
            new_x = self.Position[0] + self.Direction[0]
            new_z = self.Position[2] + self.Direction[2]
            if abs(new_x) <= self.DimBoard:
                self.Position[0] = new_x
            else:
                self.Direction[0] *= -1.0
                self.Position[0] += self.Direction[0]
            if abs(new_z) <= self.DimBoard:
                self.Position[2] = new_z
            else:
                self.Direction[2] *= -1.0
                self.Position[2] += self.Direction[2]
        self.collisionDetection(playerPosition, playerRadius)

    def calculateRotationAngle(self):
        # Calculate the angle in degrees between the direction vector and the positive z-axis
        angle = math.degrees(math.atan2(self.Direction[0], self.Direction[2]))
        return angle
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(self.scale,self.scale,self.scale)
        glColor3f(1.0, 1.0, 1.0)
        angle = self.calculateRotationAngle()
        glRotatef(angle - 180, 0.0, 1.0, 0.0)
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        # glTranslatef(0.0, 0.0, 15.0)
        # glScale(0.01, 0.01, 0.01)
        self.obj.render()
        glPopMatrix()
        
        