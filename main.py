
import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from Samurai import Samurai
from Bullet import Bullet

# Import obj loader
from objloader import *

import numpy as np

pygame.init()
pygame.mixer.init()

# Load and play the music
pygame.mixer.music.load("RDE_american_venom.mp3")  # Replace with your music file path
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop indefinitely

# Load the shooting sound effect
shooting_sound = pygame.mixer.Sound("gun_shot.mp3")
shooting_sound.set_volume(0.5) # Set the volume for the sound effect

screen_width = 1000
screen_height = 800
#vc para el obser.
FOVY=60.0
ZNEAR=0.1
ZFAR=1000.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X = 0.0
EYE_Y = 15.0 # ALTURA
EYE_Z = 0.0
CENTER_X = 100
CENTER_Y = 10
CENTER_Z = 100
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500


yaw = 0.0 # Yaw rotates around the y-axis (vertical axis). This changes the direction on the xz-plane.
pitch = 0.0 # Pitch rotates around the x-axis (lateral axis). This changes the vertical direction (y-axis).

radius = 10

mouse_sensitivity = 1

movement_speed = 3 # How many pixels does it move by iteration and key down

#Dimension del plano
DimBoard = 400

#Variables asociados a los objetos de la clase Cubo
#cubo = Cubo(DimBoard, 1.0)
samurais = []
nSamurais = 20
samurai_scale = 0.05
# objetos = []


bullets = []

#Variables para el control del observador
theta = 0.0




pygame.init()

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)


def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Cowboy vs Samurai")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    for i in range(nSamurais):
        samurais.append(Samurai(DimBoard, samurai_scale))
        
    #glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded        
    # objetos.append(OBJ("Ejemplo10_objetos a/Samurai(Low Poly).obj", swapyz=True))
    # objetos[0].generate()

# Se mueve al observador circularmente al rededor del plano XZ a una altura fija (EYE_Y)
# def lookat():
#     global EYE_X
#     global EYE_Z
#     global radius
#     EYE_X = radius * (math.cos(math.radians(theta)) + math.sin(math.radians(theta)))
#     EYE_Z = radius * (-math.sin(math.radians(theta)) + math.cos(math.radians(theta)))
#     glLoadIdentity()
#     gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)

# def displayobj():
#     glPushMatrix()  
#     #correcciones para dibujar el objeto en plano XZ
#     #esto depende de cada objeto
#     glRotatef(-90.0, 1.0, 0.0, 0.0)
#     glTranslatef(0.0, 0.0, 15.0)
#     glScale(0.1, 0.1, 0.1)
#     objetos[0].render()  
#     glPopMatrix()
    
def display():
    global radius, yaw, pitch
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    #Se dibuja el plano gris
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    #Se dibuja samurais
    for obj in samurais:
        if not (obj.bullet_collision) and obj.existence:
        # if obj.existence:
            obj.draw()
            obj.update(playerPos(), get_player_dir(yaw, pitch), radius)
        elif not obj.existence:
            samurais.remove(obj)
            print("Numero de samurais: ", len(samurais))

    for obj in bullets:
        if not (obj.collision) and obj.existence:
            obj.draw()
            obj.update()
        elif not obj.existence:
            bullets.remove(obj)

    
    # displayobj()


def playerPos():
    playerPos = [EYE_X, EYE_Y, EYE_Z]
    return np.array(playerPos)

def get_player_dir(yaw, pitch):
    # Convert angles from degrees to radians
    yaw_rad = np.radians(yaw)
    pitch_rad = np.radians(pitch)

    # Calculate the direction vector
    direction = np.array([
        np.cos(pitch_rad) * np.cos(yaw_rad), # x component
        np.sin(pitch_rad),                   # y component 
        np.cos(pitch_rad) * np.sin(yaw_rad)  # z component
    ])

    # Normalize the direction vector
    direction /= np.linalg.norm(direction)

    return direction

def calculate_look_at():
    radians_yaw = math.radians(yaw)
    radians_pitch = math.radians(pitch)
    
    cos_pitch = math.cos(radians_pitch)
    sin_pitch = math.sin(radians_pitch)
    cos_yaw = math.cos(radians_yaw)
    sin_yaw = math.sin(radians_yaw)
    
    direction_x = cos_yaw * cos_pitch
    direction_y = sin_pitch
    direction_z = sin_yaw * cos_pitch
    
    # print(direction_x, direction_y, direction_z)

    look_at_x = EYE_X + direction_x
    look_at_y = EYE_Y + direction_y
    look_at_z = EYE_Z + direction_z
    
    # print(look_at_x, look_at_y, look_at_z)
    return [look_at_x, look_at_y, look_at_z]


def handle_keyboard():
    global EYE_X, EYE_Y, EYE_Z, yaw, pitch
    keys = pygame.key.get_pressed()
    
    # Calculate forward and right vectors
    radians_yaw = math.radians(yaw)
    cos_yaw = math.cos(radians_yaw)
    sin_yaw = math.sin(radians_yaw)
    
    forward_x = cos_yaw
    forward_z = sin_yaw
    
    right_x = -sin_yaw
    right_z = cos_yaw
    
    if keys[pygame.K_w] or keys[pygame.K_UP]:  # Forward
        EYE_X += forward_x * movement_speed
        EYE_Z += forward_z * movement_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # Backward
        EYE_X -= forward_x * movement_speed
        EYE_Z -= forward_z * movement_speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # Left
        EYE_X -= right_x * movement_speed
        EYE_Z -= right_z * movement_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # Right
        EYE_X += right_x * movement_speed
        EYE_Z += right_z * movement_speed





rx, ry = (0,0)
tx, ty, tz = (0,0,0)
ypos = 10
zpos = 5


ubiX = 0
ubiZ = 0

rotate = move = False
code = ""

done = False
Init()
while not done:

    keys = pygame.key.get_pressed()
    #avanzar observador
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3: rotate = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 3: rotate = False
        if event.type == MOUSEMOTION:
            if rotate == True:
                i, j = event.rel
                yaw += i * mouse_sensitivity
                pitch -= j * mouse_sensitivity
                pitch = max(-89.0, min(89.0, pitch))

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                bullets.append(Bullet(DimBoard, samurais, playerPos(), get_player_dir(yaw, pitch), shooting_sound))
    handle_keyboard()
    look_at = calculate_look_at()


    
    
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,look_at[0], look_at[1], look_at[2] ,UP_X,UP_Y,UP_Z)

    # print(playerPos())

    display()

    pygame.display.flip()
    pygame.time.wait(10)


pygame.mixer.music.stop()
pygame.quit()