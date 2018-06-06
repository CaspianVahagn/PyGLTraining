from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.arrays import vbo
from numpy import array
import numpy
import sys, math, os

EXIT = -1
FIRST = 0

width = None
height = None
aktY = None
shadow = True

COLOR = (1.0,1.0,1.0)
BACKGROUNDCOLOR = (0.2, 0.0, 0.8, 0.5)
punkte = {}
dreiecke = []
data = []
normalen = {}
myvbo = None

degree = 0
lightPos = [0.0,5.0,0.0]

angle = 0
axis = numpy.array([1.,1.,1.])
scaleFactor = None
startP = numpy.array([0.,0.,0.,0.])
actOri = numpy.array([[1.,0.,0.,0.],
                      [0.,1.,0.,0.],
                      [0.,0.,1.,0.],
                      [0.,0.,0.,1.]])
doRotation = False
actSc = numpy.array([[1.,0.,0.,0.],
                      [0.,1.,0.,0.],
                      [0.,0.,1.,0.],
                      [0.,0.,0.,1.]])
scalefac = 1
isOrtho = True
actX = None
actY = None
pos = [0,0,0]
minY = None

doTrans = False

def sub(a,b):

    return[a[0]-b[0],a[1]-b[1],a[2]-b[2]]

def einlese(pfad):

    global myvbo
    lines = open(pfad).read().split("\n")


    counter = 1
    counterN = 1
    for ele in lines:
        line = ele.split()
        if "".join(ele).strip():
            if (line[0] == "v"):
                punkte[counter] = [float(line[1]),float(line[2]),float(line[3])]
                counter+=1
            elif (line[0] == "vn"):

                a = (float(line[1]))
                b = (float(line[2]))
                c = (float(line[3]))

                normalen[counterN] = [a,b,c]
                counterN+=1
            elif (line[0] == "f"):
                if "//" not in line[1]:
                    a = int(line[1])
                    b = int(line[2])
                    c = int(line[3])
                    na = numpy.cross(sub(punkte[c],punkte[a]),sub(punkte[b],punkte[a]))
                    na = [abs(x) for x in list(na)]
                    nb = numpy.cross(sub(punkte[c], punkte[b]), sub(punkte[a], punkte[b]))
                    nb = [abs(x) for x in list(nb)]
                    nc = numpy.cross(sub(punkte[a], punkte[c]), sub(punkte[b], punkte[c]))
                    nc = [abs(x) for x in list(nc)]
                    dreiecke.append([a,na])
                    dreiecke.append([b,nb])
                    dreiecke.append([c,nc])

                else:
                    lin1 = line[1].split("//")
                    lin2 = line[2].split("//")
                    lin3 = line[3].split("//")
                    dreiecke.append((int(lin1[0]), int(lin1[1])))
                    dreiecke.append((int(lin2[0]), int(lin2[1])))
                    dreiecke.append((int(lin3[0]), int(lin3[1])))

    for ele in dreiecke:
        if type(ele) is list:
            data.append(punkte[ele[0]]+ele[1])
        else:
            #print(ele)
            data.append(punkte[ele[0]]+ normalen[ele[1]])


    myvbo = vbo.VBO(numpy.array(data, 'f'))

    verschiebungY()


def init(width, height):
   """ Initialize an OpenGL window """
   global isOrtho
   glClearColor(BACKGROUNDCOLOR[0],BACKGROUNDCOLOR[1],BACKGROUNDCOLOR[2],BACKGROUNDCOLOR[3])         #background color
   glMatrixMode(GL_PROJECTION)              #switch to projection matrix
   glLoadIdentity()                         #set to 1

   glOrtho(-1.5, 1.5, -1.5, 1.5, -1.0, 1.0) #multiply with new p-matrix

   glMatrixMode(GL_MODELVIEW)               #switch to modelview matrix

   glEnable(GL_LIGHTING)
   glEnable(GL_LIGHT0)
   glEnable(GL_DEPTH_TEST)
   glEnable(GL_NORMALIZE)
   glEnable(GL_COLOR_MATERIAL)

   ambient = [0.15,0.15,0.15,1.0]
   diffuse = [0.6,0.6,0.6,1.0]
   specular = [0.1,0.1,0.1,1.0]
   #lightPos = [0.0,0,1.0,0]

   glLightfv(GL_LIGHT0,GL_AMBIENT,ambient)
   glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
   glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
   glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

def verschiebungY():

    global minY

    minimax = maxmin()
    minY = minimax[1][1]



def maxmin():

    mini = (min(list(map(lambda x: x[0],punkte.values()))),min(list(map(lambda x: x[1],punkte.values()))),min(list(map(lambda x: x[2],punkte.values()))))
    maxi = (max(list(map(lambda x: x[0], punkte.values()))), max(list(map(lambda x: x[1], punkte.values()))), max(list(map(lambda x: x[2], punkte.values()))))

    global minY


    minY = mini[1]

    return[maxi,mini]

def maxlen(maxmin):

    return max([(x-y) for x in maxmin[0] for y in maxmin[1]])

def scaleMax():
    max = maxlen(maxmin())
    glScalef(1 / max, 1 / max, 1 / max)
    actSc = numpy.array([[1 / max, 0., 0., 0.],
                         [0., 1 / max, 0., 0.],
                         [0., 0., 1 / max, 0.],
                         [0., 0., 0., 1.]])
    return actSc


def scale():

    glScalef(scalefac,scalefac,scalefac)
    actSc = numpy.array([[scalefac, 0., 0., 0.],
                        [0., scalefac, 0., 0.],
                        [0., 0., scalefac, 0.],
                        [0., 0., 0., 1.]])

    return actSc

def mittelpunkt():

    werte = maxmin()

    x = float((werte[0][0]) - (werte[1][0])) /2 + werte[1][0]
    y= float((werte[0][1]) - (werte[1][1])) / 2 + werte[1][1]
    z = float((werte[0][2]) - (werte[1][2])) / 2 + werte[1][2]

    return (x,y,z)


def rotate():
    mp = mittelpunkt()
    global degree
    degree += math.pi / 8
    glRotatef(degree,mp[0],mp[1],mp[2])

def rotate(angle, axis):
    c,mc = math.cos(angle),1-math.cos(angle)
    s = math.sin(angle)
    l = math.sqrt(numpy.dot(numpy.array(axis),numpy.array(axis)))
    x,y,z = numpy.array(axis)/l
    r = numpy.matrix(
        [[x*x*mc+c, x*y*mc-z*s,x*z*mc+y*s,0],
         [x*y*mc+z*s, y*y*mc+c, y*z*mc-x*s, 0],
         [x*z*mc-y*s, y*z*mc+x*s, z*z*mc+c, 0],
         [0, 0 ,0 , 1]]
    )

    return r.transpose()

def projectOnSphere(x,y,r):
    x,y = x-width / 2.0, height/2.0-y
    a = min(r*r,x**2 + y**2)
    z = math.sqrt(r*r - a)
    l = math.sqrt(x**2 + y**2 + z**2)
    return x/l, y/l, z/l



def display():
   global myvbo,lightPos

   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT ) #clear screen

   glClearColor(BACKGROUNDCOLOR[0], BACKGROUNDCOLOR[1], BACKGROUNDCOLOR[2], BACKGROUNDCOLOR[3])

   glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

   glLoadIdentity()

   scaleMax() #skalieren auf -1 bis 1
   mp = mittelpunkt()

   glTranslate(-mp[0], -mp[1], -mp[2])


   glMultMatrixf(actOri * rotate(angle, axis)) #rotate
   glTranslate(pos[0], pos[1], pos[2]) #move position

   scale() #scale um scaleFac


   myvbo.bind()

   glEnableClientState(GL_VERTEX_ARRAY)
   glEnableClientState(GL_NORMAL_ARRAY)
   glVertexPointer(3,GL_FLOAT,24,myvbo)
   glNormalPointer(GL_FLOAT,24,myvbo+12)
   glColor3f(COLOR[0], COLOR[1], COLOR[2])
   glDrawArrays(GL_TRIANGLES, 0, len(data))

   myvbo.unbind()


   glDisableClientState(GL_VERTEX_ARRAY)
   glDisableClientState(GL_NORMAL_ARRAY)


   if shadow:

       p = [1.0, 0., 0., 0., 0., 1.0, 0., -1.0 / lightPos[1], 0., 0., 1.0, 0., 0., 0., 0., 0.]
       glDisable(GL_LIGHTING)

       myvbo.bind()

       glColor3f(0., 0., 0.)

       glEnableClientState(GL_VERTEX_ARRAY)
       glEnableClientState(GL_NORMAL_ARRAY)

       glVertexPointer(3, GL_FLOAT, 24, myvbo)
       glNormalPointer(GL_FLOAT, 24, myvbo + 12)

       glLoadIdentity()
       scaleMax()# skalieren auf -1 bis 1
       glTranslate(0, minY, 0)
       mp = mittelpunkt()

       glTranslate(-mp[0], -mp[1], -mp[2])
       #
       glTranslate(pos[0], pos[1], pos[2])  # move position
       scale()  # scale um scaleFac


       glTranslatef(lightPos[0],lightPos[1],lightPos[2])

       glMultMatrixf(p)

       glTranslatef(-lightPos[0], -lightPos[1], -lightPos[2])


       glMultMatrixf(actOri * rotate(angle, axis))  # rotate


       glDrawArrays(GL_TRIANGLES, 0, len(data))

       myvbo.unbind()
       glEnable(GL_LIGHTING)

       glDisableClientState(GL_VERTEX_ARRAY)
       glDisableClientState(GL_NORMAL_ARRAY)




   glutSwapBuffers()            #swap buffer



def reshape(width, height):
   """ adjust projection matrix to window size"""
   if height == 0:
       height = 1
   glViewport(0, 0, width, height)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   if isOrtho == True:
       if width <= height:
           glOrtho(-1.5, 1.5,
                   -1.5*height/width, 1.5*height/width,
                   -1.0, 1.0)
       else:
           glOrtho(-1.5*width/height, 1.5*width/height,
                   -1.5, 1.5,
                   -1.0, 1.0)
   else:
       gluPerspective(45., float(width) / height, 0.01, 50.)
       gluLookAt(0, 0, 4, 0, 0, 0, 0, 1, 0)
       #gluLookAt(0, 0, -3, 0, 0, 500, 0, 1, 0)

   glMatrixMode(GL_MODELVIEW)
   glutSwapBuffers()


def keyPressed(key, x, y):
   """ handle keypress events """

   global COLOR,isOrtho,BACKGROUNDCOLOR,shadow
   if key == chr(27): # chr(27) = ESCAPE
       sys.exit()
   elif key == "g":
       COLOR = 0.0,1.0,0.0
       glutPostRedisplay()
   elif key == "s":
       COLOR = 0.0, 0.0, 0.0
       glutPostRedisplay()
   elif key == "w":
       COLOR = 1.0, 1.0, 1.0
       glutPostRedisplay()
   elif key == "b":
       COLOR = 0.0, 0.0, 1.0
       glutPostRedisplay()
   elif key == "r":
       COLOR = 1.0,0.0,0.0
       glutPostRedisplay()
   elif key == "R":
       BACKGROUNDCOLOR = (1.0, 0.0, 0.0,0.5)
       glutPostRedisplay()
   elif key == "G":
       BACKGROUNDCOLOR = (0.0, 1.0, 0.0,0.5)
       glutPostRedisplay()
   elif key == "S":
       BACKGROUNDCOLOR = (0.0, 0.0, 0.0,0.5)
       glutPostRedisplay()
   elif key == "W":
       BACKGROUNDCOLOR = (1.0, 1.0, 1.0,0.5)
       glutPostRedisplay()
   elif key == "B":
       BACKGROUNDCOLOR = (0.0, 0.0, 1.0,0.5)
       glutPostRedisplay()
   elif key == "o":
       isOrtho = True
       reshape(width,height)
       glutPostRedisplay()
   elif key == "p":
       isOrtho = False
       reshape(width,height)
       glutPostRedisplay()
   elif key =="h":
       if(shadow == True):
           shadow = False
       else:
           shadow = True
       glutPostRedisplay()


def mouse(button, state, x, y):
   """ handle mouse events """
   global aktY,startP,actOri,angle,doRotation,pos,actX,actY,doTrans
   r = min(width,height)/2.0
   if button == GLUT_LEFT_BUTTON:
       if state == GLUT_DOWN:
           doRotation = True
           startP = projectOnSphere(x,y,r)
       if state == GLUT_UP:
           doRotation = False
           actOri = actOri*rotate(angle,axis)
           angle = 0

   elif button == 3:
       global scalefac
       scalefac += 0.05
       glutPostRedisplay()
   elif button == 4:
       scalefac -= 0.05
       glutPostRedisplay()

   elif button == GLUT_RIGHT_BUTTON:
       actX = x
       actY = y
       if state == GLUT_DOWN:
           doTrans = True

       elif state == GLUT_UP:
           doTrans = False

def mouseMotion(x,y):
   """ handle mouse motion """
   global angle,axis,scaleFactor,actX,actY,pos
   if doRotation:
       r = min(width,height)/2.0
       moveP = projectOnSphere(x,y,r)
       angle = math.acos(numpy.dot(startP,moveP))
       axis = numpy.cross(startP,moveP)
       glutPostRedisplay()

   elif doTrans:
       scaleX = float(width)/2.0
       scaleY = float(height)/2.0
       diff_x = x - actX
       diff_y = actY -y
       pos[0] = diff_x/scaleX
       pos[1] = diff_y/scaleY
       glutPostRedisplay()




def menu_func(value):
   """ handle menue selection """
   if value == EXIT:
       sys.exit()
   glutPostRedisplay()


def main():
   einlese("squirrel_ar.obj")

   global height,width, aktY, actX, actY
   width = 500
   height = 500
   actX = width/2.
   actY = height/2.
   aktY = height/2.

   # Hack for Mac OS X
   cwd = os.getcwd()
   glutInit(sys.argv)
   os.chdir(cwd)

   glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
   glutInitWindowSize(width, height)
   glutCreateWindow(b"simple openGL/GLUT template")

   glutDisplayFunc(display)     #register display function
   glutReshapeFunc(reshape)     #register reshape function
   glutKeyboardFunc(keyPressed) #register keyboard function

   glutMouseFunc(mouse)         #register mouse function
   glutMotionFunc(mouseMotion)  #register motion function
   glutCreateMenu(menu_func)    #register menue function




   glutAddMenuEntry("First Entry",FIRST) #Add a menu entry
   glutAddMenuEntry("EXIT",EXIT)         #Add another menu entry
   #glutAttachMenu(GLUT_RIGHT_BUTTON)     #Attach mouse button to menue

   init(500,500) #initialize OpenGL state

   glutMainLoop() #start even processing


if __name__ == "__main__":
   main()