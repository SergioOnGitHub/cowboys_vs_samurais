import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np


class Bullet:
    
    def __init__(self, dim, samurais, playerPos, playerDir):
        #Se inicializa las coordenadas de los vertices del cubo
        self.points = np.array([[-1.0,-1.0, 1.0], [1.0,-1.0, 1.0], [1.0,-1.0,-1.0], [-1.0,-1.0,-1.0],
                                [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0,-1.0], [-1.0, 1.0,-1.0]])
        self.radius = 5
        self.vel = 5
        self.existence = True
        self.samurais = samurais
        #Se inicializa la dimension del tableros
        self.DimBoard = dim
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = np.array(playerPos)
        self.Position[1] -= 2
        # self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        # self.Position.append(5.0)
        # self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        #Se inicializa un vector de direccion aleatorio
        self.Direction = np.array(playerDir)
        self.Direction = self.Direction / np.linalg.norm(self.Direction)
        self.Direction *= self.vel
        # self.Direction.append(random.random())
        # self.Direction.append(5.0)
        # self.Direction.append(random.random())
        # #Se normaliza el vector de direccion

        #Se cambia la maginitud del vector direccion
        self.collision = False

    def getPosition(self):
        return self.Position
        
    def colisionDetection(self):
        for samurai in self.samurais:
            samurai_pos = samurai.get_position()  # Assuming samurais have a get_position method
            samurai_radius = samurai.get_radius()  # Assuming samurais have a get_radius method

            distance = np.linalg.norm(self.Position - samurai_pos)
            if distance < self.radius + samurai_radius:
                self.existence = False
                samurai.on_hit()  # Assuming samurais have an on_hit method
                break


    def update(self):
        if self.existence:
            print(self.Position, self.Direction)

            self.Position += self.Direction
            if np.any(np.abs(self.Position) > self.DimBoard):
                self.existence = False
            self.colisionDetection()

    def drawFaces(self):
        glBegin(GL_QUADS)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[7])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[4])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[5])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[7])
        glVertex3fv(self.points[6])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[7])
        glEnd()
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(0.5,0.5,0.5)
        glColor3f(1, 1, 0)
        self.drawFaces()
        glPopMatrix()
