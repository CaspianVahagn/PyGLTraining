from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy as np
import sys, math, os




WIDTH = None
HEIGHT = None
aktY = None
shadow = True
scale_trans = 1

COLOR = (1.0, 1.0, 1.0)
BACKGROUNDCOLOR = (0.2, 0.0, 0.8, 0.5)
points = {}
triangles = []
vertex_data = []
normals = {}
_vbo = None

degree = 0
light = [3.0, 1600.0, 0.0]
x_pos = None
y_pos = None
pos = [0, 0, 0]
y_foot = None

translate = False
angle = 0
axis = np.array([1., 1., 1.])
scaleFactor = None
startP = np.array([0., 0., 0., 0.])
orientation = np.array([[1., 0., 0., 0.],
                           [0., 1., 0., 0.],
                           [0., 0., 1., 0.],
                           [0., 0., 0., 1.]])
doRotation = False
scaling = np.array([[1., 0., 0., 0.],
                       [0., 1., 0., 0.],
                       [0., 0., 1., 0.],
                       [0., 0., 0., 1.]])
scalefac = 1
orthogonal_projection = True

EXIT = -1

def sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def reset():
    global _vbo, triangles, vertex_data, normals, points
    points = {}
    triangles = []
    vertex_data = []
    normals = {}
    _vbo = None

def einlese(pfad):
    global _vbo
    lines = open(pfad).read().split("\n")
    reset()
    p_count = 1
    n_count = 1
    for ele in lines:
        line = ele.split()
        if "".join(ele).strip():
            if (line[0] == "v"):
                points[p_count] = [float(v) for v in line[1:4]]
                p_count += 1
            elif (line[0] == "vn"):
                a,b,c = [float(v) for v in line[1:4]]
                normals[n_count] = [a, b, c]
                n_count += 1
            elif (line[0] == "f"):
                if "//" not in line[1]:

                    a,b,c = [int(v) for v in line[1:4]]
                    na = np.cross(sub(points[c], points[a]), sub(points[b], points[a]))
                    na = [abs(x) for x in list(na)]
                    nb = np.cross(sub(points[c], points[b]), sub(points[a], points[b]))
                    nb = [abs(x) for x in list(nb)]
                    nc = np.cross(sub(points[a], points[c]), sub(points[b], points[c]))
                    nc = [abs(x) for x in list(nc)]
                    triangles.append([a, na])
                    triangles.append([b, nb])
                    triangles.append([c, nc])

                else:
                    kanten = [ x.split("//") for x in line[1:4]]
                    triangles.append((int(kanten[0][0]), int(kanten[0][1])))
                    triangles.append((int(kanten[1][0]), int(kanten[1][0])))
                    triangles.append((int(kanten[2][0]), int(kanten[2][0])))

    for ele in triangles:
        if type(ele) is list:
            vertex_data.append(points[ele[0]] + ele[1])
        else:
            # print(ele)
            vertex_data.append(points[ele[0]] + normals[ele[1]])

    _vbo = vbo.VBO(np.array(vertex_data, 'f'))
    global scale_trans
    scale_trans = maxlen(bounding_box())
    translate_y()


def init():
    """ Initialize an OpenGL window """
    global orthogonal_projection
    glClearColor(BACKGROUNDCOLOR[0], BACKGROUNDCOLOR[1], BACKGROUNDCOLOR[2], BACKGROUNDCOLOR[3])  # background color
    glMatrixMode(GL_PROJECTION)  # switch to projection matrix
    glLoadIdentity()  # set to 1

    glOrtho(-1.5, 1.5, -1.5, 1.5, -1.0, 1.0)  # multiply with new p-matrix

    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)

    ambient = [0.15, 0.15, 0.15, 1.0]
    diffuse = [0.6, 0.6, 0.6, 1.0]
    specular = [0.1, 0.1, 0.1, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light)


def translate_y():
    global y_foot
    y_foot = bounding_box()[1][1]


def bounding_box():
    global y_foot

    min_values = (
        min(list(map(lambda x: x[0], points.values()))),
        min(list(map(lambda x: x[1], points.values()))),
        min(list(map(lambda x: x[2], points.values())))
    )

    max_values = (
            max(list(map(lambda x: x[0], points.values()))),
            max(list(map(lambda x: x[1], points.values()))),
            max(list(map(lambda x: x[2], points.values())))
            )



    y_foot = min_values[1]

    return [max_values, min_values]


def maxlen(maxmin):
    return max([(x - y) for x in maxmin[0] for y in maxmin[1]])


def scaleMax():
    max = maxlen(bounding_box())
    glScalef(1 / max, 1 / max, 1 / max)
    actSc = np.array([[1 / max, 0., 0., 0.],
                         [0., 1 / max, 0., 0.],
                         [0., 0., 1 / max, 0.],
                         [0., 0., 0., 1.]])
    return actSc


def scale():
    glScalef(scalefac, scalefac, scalefac)
    actSc = np.array([[scalefac, 0., 0., 0.],
                         [0., scalefac, 0., 0.],
                         [0., 0., scalefac, 0.],
                         [0., 0., 0., 1.]])

    return actSc


def get_center():
    werte = bounding_box()
    x = float((werte[0][0]) - (werte[1][0])) / 2 + werte[1][0]
    y = float((werte[0][1]) - (werte[1][1])) / 2 + werte[1][1]
    z = float((werte[0][2]) - (werte[1][2])) / 2 + werte[1][2]
    return (x, y, z)


def rotate():
    mp = get_center()
    global degree
    degree += math.pi / 8
    glRotatef(degree, mp[0], mp[1], mp[2])


def rotate(angle, axis):
    c, mc = math.cos(angle), 1 - math.cos(angle)
    s = math.sin(angle)
    l = math.sqrt(np.dot(np.array(axis), np.array(axis)))
    x, y, z = np.array(axis) / l
    r = np.matrix(
        [
         [x * x * mc + c, x * y * mc - z * s, x * z * mc + y * s, 0],
         [x * y * mc + z * s, y * y * mc + c, y * z * mc - x * s, 0],
         [x * z * mc - y * s, y * z * mc + x * s, z * z * mc + c, 0],
         [0, 0, 0, 1]
         ]
    )

    return r.transpose()


def projectOnSphere(x, y, r):
    x, y = x - WIDTH / 2.0, HEIGHT / 2.0 - y
    a = min(r * r, x ** 2 + y ** 2)
    z = math.sqrt(r * r - a)
    l = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    return x / l, y / l, z / l


def display():
    global _vbo, light

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear screen

    glClearColor(BACKGROUNDCOLOR[0], BACKGROUNDCOLOR[1], BACKGROUNDCOLOR[2], BACKGROUNDCOLOR[3])

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glLoadIdentity()

    scaleMax()  # skalieren auf -1 bis 1
    mp = get_center()

    glTranslate(-mp[0], -mp[1], -mp[2])

    glMultMatrixf(orientation * rotate(angle, axis))  # rotate
    glTranslate(pos[0], pos[1], pos[2])  # move position

    scale()  # scale um scaleFac

    _vbo.bind()

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glVertexPointer(3, GL_FLOAT, 24, _vbo)
    glNormalPointer(GL_FLOAT, 24, _vbo + 12)
    glColor3f(COLOR[0], COLOR[1], COLOR[2])
    glDrawArrays(GL_TRIANGLES, 0, len(vertex_data))

    _vbo.unbind()

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)

    if shadow:
        calcShadow()

    glutSwapBuffers()


def calcShadow():
    global _vbo, light
    p = [1.0, 0., 0., 0., 0., 1.0, 0., -1.0 / light[1], 0., 0., 1.0, 0., 0., 0., 0., 0.]
    glDisable(GL_LIGHTING)

    _vbo.bind()

    glColor3f(0., 0., 0.)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    glVertexPointer(3, GL_FLOAT, 24, _vbo)
    glNormalPointer(GL_FLOAT, 24, _vbo + 12)

    glLoadIdentity()
    scaleMax()
    glTranslate(0, y_foot, 0)
    mp = get_center()

    glTranslate(-mp[0], -mp[1], -mp[2])
    #
    glTranslate(pos[0], 0, pos[2])  # move position
    scale()  # scale um scaleFac
    glTranslatef(light[0], light[1], light[2])

    glMultMatrixf(p)

    glTranslatef(-light[0], -light[1], -light[2])

    glMultMatrixf(orientation * rotate(angle, axis))  # rotate

    glDrawArrays(GL_TRIANGLES, 0, len(vertex_data))

    _vbo.unbind()
    glEnable(GL_LIGHTING)

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)



def resize(width, height):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if orthogonal_projection == True:
        if width <= height:
            glOrtho(-1.5, 1.5,
                    -1.5 * height / width, 1.5 * height / width,
                    -1.0, 1.0)
        else:
            glOrtho(-1.5 * width / height, 1.5 * width / height,
                    -1.5, 1.5,
                    -1.0, 1.0)
    else:
        gluPerspective(45., float(width) / height, 0.01, 50.)
        gluLookAt(0, 0, 4, 0, 0, 0, 0, 1, 0)

    glMatrixMode(GL_MODELVIEW)
    glutSwapBuffers()


def key_event(key, x, y):

    def exit():
        sys.exit()

    def yellow():
        global COLOR
        COLOR = 1.0, 1.0, 0.0

    def black():
        global COLOR
        COLOR = 0.0, 0.0, 0.0

    def white():
        global COLOR
        COLOR = 1.0, 1.0, 1.0

    def red():
        global COLOR
        COLOR = 1.0, 0.0, 0.0

    def blue():
        global COLOR
        COLOR = 0.0, 0.0, 1.0

    def bgred():
        global BACKGROUNDCOLOR
        BACKGROUNDCOLOR = (1.0, 0.0, 0.0, 0.5)

    def bgyellow():
        global BACKGROUNDCOLOR
        BACKGROUNDCOLOR = (1.0, 1.0, 0.0, 0.5)

    def bgblue():
        global BACKGROUNDCOLOR
        BACKGROUNDCOLOR = (0.0, 0.0, 1.0, 0.5)

    def bgblack():
        global BACKGROUNDCOLOR
        BACKGROUNDCOLOR = (.0, .0, .0, 0.5)

    def bgwhite():
        global BACKGROUNDCOLOR
        BACKGROUNDCOLOR = (1.0, 1.0, 1.0, 0.5)

    def orthogonal():
        global orthogonal_projection
        orthogonal_projection = True
        resize(WIDTH, HEIGHT)

    def central():
        global orthogonal_projection
        orthogonal_projection = False
        resize(WIDTH, HEIGHT)

    def setshading():
        global shadow
        shadow = not shadow

    commands= {
        chr(27): exit,
        'g' : yellow,
        's' : black,
        'w' : white,
        'r' : red,
        'b' : blue,
        'R' : bgred,
        'G' : bgyellow,
        'B' : bgblue,
        'S' : bgblack,
        'W' : bgwhite,
        'o' : orthogonal,
        'p' : central,
        'h' : setshading
    }

    func = commands.get(key, lambda: "no mapping")
    func()
    glutPostRedisplay()





def mouse_action(button, state, x, y):
    """ handle mouse events """
    global aktY, startP, orientation, angle, doRotation, pos, x_pos, y_pos, translate
    r = min(WIDTH, HEIGHT) / 2.0
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            doRotation = True
            startP = projectOnSphere(x, y, r)
        if state == GLUT_UP:
            doRotation = False
            orientation = orientation * rotate(angle, axis)
            angle = 0

    elif button == 3:
        global scalefac
        scalefac += 0.05
        glutPostRedisplay()
    elif button == 4:
        scalefac -= 0.05
        glutPostRedisplay()

    elif button == GLUT_RIGHT_BUTTON:
        x_pos = x
        y_pos = y
        if state == GLUT_DOWN:
            translate = True

        elif state == GLUT_UP:
            translate = False


def mouse_move(x, y):
    """ handle mouse motion """
    global angle, axis, scaleFactor, x_pos, y_pos, pos, scale_trans
    if doRotation:
        r = min(WIDTH, HEIGHT) / 2.0
        moveP = projectOnSphere(x, y, r)
        angle = math.acos(np.dot(startP, moveP))
        axis = np.cross(startP, moveP)
        glutPostRedisplay()

    elif translate:
        scaleX = float(WIDTH) / 2.0
        scaleY = float(HEIGHT) / 2.0
        delta_x = (x - x_pos) * scale_trans
        delta_y = (y_pos - y) * scale_trans
        pos = [(delta_x / scaleX), (delta_y / scaleY), pos[2]]
        glutPostRedisplay()


def option_menue(value):
    

    """ handle menue selection """
    menuedic = {
                0: "bunny.obj",
                1: "elephant.obj",
                2: "squirrel.obj",
                3: "squirrel_ar.obj",
                4: "cow.obj"
                }

    if value == EXIT:
        sys.exit()

    else:
        einlese(menuedic[value])




def main():
    einlese("random.obj")

    global HEIGHT, WIDTH, aktY, x_pos, y_pos
    WIDTH = 500
    HEIGHT = 500
    x_pos = WIDTH / 2.
    y_pos = HEIGHT / 2.
    aktY = HEIGHT / 2.
    cwd = os.getcwd()
    glutInit(sys.argv)
    os.chdir(cwd)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"simple openGL/GLUT template")

    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutKeyboardFunc(key_event)

    glutMouseFunc(mouse_action)
    glutMotionFunc(mouse_move)
    glutCreateMenu(option_menue)
    import ctypes as ct
    glutAddMenuEntry("Bunny", 0)
    glutAddMenuEntry("Elephant", 1)
    glutAddMenuEntry("Squirrel", 2)
    glutAddMenuEntry("Squirrel AR", 3)
    glutAddMenuEntry("Cow", 4)

    glutAddMenuEntry("EXIT", EXIT)
    glutAttachMenu(GLUT_MIDDLE_BUTTON)

    init()  # initialize OpenGL state

    glutMainLoop()  # start even processing


if __name__ == "__main__":
    main()
