from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GLUT as GLUT
import numpy as np
import sys, math
from ctypes import *

from OpenGL.raw.GLUT import glutMouseFunc

angle, angle2 = 0,0
animate = False
centerZ = -4.0
centerX = 0.0
centerY = 0.0
WIDTH = 500
HEIGHT = 500
MouseAction = (-1, -1, -1, -1)
startX = 0
startY = 0
ambient_intensity = [0.3, 0.3, 0.3, 1.0]
intensity = [0.7, 0.7, 0.7, 1.0]
direction = [0.0, 2.0, -1.0, 1.0]
surface = GL_SMOOTH


def readPoints():
    x = open("squirrel_ar.obj","r")
    print(x.read())


def initGL(width, height):
    glClearColor(0.0, 0.0, 1.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, float(width)/height,0.1,100.0)
    glMatrixMode(GL_MODELVIEW)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.2, 0.7, 0.6)
    glShadeModel(surface)
    glLoadIdentity()
    glTranslate(centerX, centerY, centerZ)
    glRotate(angle, 0.0, 1.0, 0.0)
    glRotate(angle2, 1.0, 0.0, 0.0)
    GLUT.glutSolidTeapot(1.0)
    GLUT.glutSwapBuffers()


def keyPressed(key, x,y):
    global animate
    print ("ok")
    if key == "a":
        animate = not animate
        GLUT.glutPostRedisplay()


def animation():
    global angle, startX,startY, MouseAction

    GLUT.glutPostRedisplay()






def resizing(width, height):
    global WIDTH, HEIGHT
    if height == 0:
            height = 1
    glViewport(0,0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/height, 0.1, 100.0)
    #light
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_intensity)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, direction)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    #
    glMatrixMode(GL_MODELVIEW)
    GLUT.glutSwapBuffers()
    WIDTH = width
    height = height


def mouseFun(button, state, x, y):

    global centerZ
    global MouseAction
    MouseAction = (button,state,x,y)
    if button == 4:
        centerZ += 0.2
        print centerZ
    if button == 3:
        centerZ -= 0.2
        print centerZ


def mouseMotion(x,y):

    global angle, angle2, MouseAction, centerX, centerY
    btn, state, _, __ = MouseAction
    if btn == 0:
        angle = x - _
        angle2 = y - __
    if btn == 2:
        trans_x = (x - _)
        trans_y = (__ - y)
        if trans_x == 0:
            trans_x = 1.0
        if trans_y == 0:
            trans_y = 1.0
        centerX = float(trans_x)/WIDTH
        centerY = float(trans_y)/HEIGHT
        print centerX, centerY




def main():
    GLUT.glutInit(sys.argv)
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB | GLUT.GLUT_DEPTH)
    GLUT.glutInitWindowSize(500,500)
    GLUT.glutCreateWindow("TEAPOT")
    GLUT.glutReshapeFunc(resizing)
    GLUT.glutDisplayFunc(display)
    GLUT.glutKeyboardFunc(keyPressed)
    GLUT.glutIdleFunc(animation)
    GLUT.glutMouseFunc(mouseFun)
    GLUT.glutMotionFunc(mouseMotion)
    initGL(WIDTH, HEIGHT)
    GLUT.glutMainLoop()


if __name__ == '__main__':
    main()