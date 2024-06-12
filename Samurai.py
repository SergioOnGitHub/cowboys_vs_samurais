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
        self.scale = scale
        self.hitbox = 12
        self.DimBoard = dim
        self.vel = 3
        self.Position = self.generate_position_near_border()
        self.Direction = [random.random(), 0, random.random()]
        self.Direction[0] /= math.sqrt(self.Direction[0]**2 + self.Direction[2]**2)
        self.Direction[2] /= math.sqrt(self.Direction[0]**2 + self.Direction[2]**2)
        self.Direction[0] *= self.vel
        self.Direction[2] *= self.vel
        self.player_collision = False
        self.bullet_collision = False
        self.existence = True
        self.activation_zone = 200
        self.obj = OBJ("Samurai_low_poly.obj", swapyz=True)
        self.obj.generate()


    def generate_position_near_border(self):
        x = random.randint(self.DimBoard * 0.5, self.DimBoard -10) * random.choice([1, -1])
        z = random.randint(self.DimBoard *0.5, self.DimBoard - 10) * random.choice([1, -1])
        return [x, 0, z]


    def get_position(self):
        return np.array(self.Position)

    def get_hitbox(self):
        return self.hitbox

    def on_hit(self):
        self.bullet_collision = True
        self.existence = False
        print("Samurai hit!")

    def collisionDetection(self, playerPosition, playerHitbox):
        distance = np.linalg.norm(self.get_position() - playerPosition)
        if distance < self.hitbox + playerHitbox:
            return True
        return False
        

    def activate_zone(self, playerPosition):
        distance = np.linalg.norm(self.get_position() - playerPosition)
        return distance < self.activation_zone
        
    def update(self, playerPosition, playerDirection, playerHitbox):
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


    def calculateRotationAngle(self):
    # Calcular el ángulo en grados entre el vector de dirección y el eje z positivo
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
        self.obj.render()
        glPopMatrix()
        
        