from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import sys, math
from ctypes import *

from OpenGL.raw.GLUT import glutMouseFunc

angle = 0
animate = False

def readPoints():
    x = open("squirrel_ar.obj","r")
    print(x.read())


def initGL(width, height):
    glClearColor(0.0, 0.0, 1.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, float(width)/height,0.1,100.0)
    glMatrixMode(GL_MODELVIEW)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslate(0.0, 0.0, -4.0)
    glRotate(angle, 0.0, 1.0, 0.0)
    glutWireTeapot(1.0)

    glutSwapBuffers()


def keyPressed(key, x,y):
    global animate
    print ("ok")
    if key == "a":
        animate = not animate
        glutPostRedisplay()


def animation():
    global angle

    if animate:
        print angle
        angle = (angle+1)%360
        glutPostRedisplay()


def resizing(width, height):
    if height == 0:
            height = 1
    glViewport(0,0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glutSwapBuffers()


def mouseFun(button, state, x ,y):
    print x,y


def main():
    CMPFUNC = CFUNCTYPE(c_char, c_int, c_int)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(500,500)
    from OpenGL import GLUT
    glutCreateWindow("TEAPOT")
    glutReshapeFunc(resizing)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyPressed)
    glutIdleFunc(animation)

    GLUT.glutMouseFunc(mouseFun)
    initGL(500, 500)
    glutMainLoop()

if __name__ == '__main__':
    main()