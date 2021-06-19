##########################################################################
##                                                                      ##
##  This Utility Package is written by Zhi-Li Liu                       ##
##  You may use it for free, but leave this here!                       ##
##                                                                      ##
##  This package contains utilities that makes the use of PyopenGL      ##
##  less of a pain. It deals with loading textures, making skyboxes,    ##
##  and loading model files (.obj). The model loading part has been     ##
##  made inspired by Oscar Veerhoek from the Coding Universe            ##
##                                                                      ##
##  For contact please email: Z.Liu-4@student.tudelft.nl                ##
##                                                                      ##
##  (c)2014 Zhi-Li Liu                                                  ##
##                                                                      ##
##                                                                      ##
##########################################################################
from pathlib import PurePath

import PIL.Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from numpy import *

###################################################################
#
#  Texture class
#
###################################################################
class Texture:
    imgid = 0
    width = 0
    height = 0

    def __init__(self, width, height, img):
        self.width = width
        self.height = height
        img = img.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        img_data = array(list(img.getdata()), int8)
        bpp = dict([("RGBA", GL_RGBA), ("RGB", GL_RGB)])

        # generate new texture
        self.imgid = glGenTextures(1)

        # bind texture
        glBindTexture(GL_TEXTURE_2D, self.imgid)

        # set texture filters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Copy buffer into texture
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            bpp[img.mode],
            width,
            height,
            0,
            bpp[img.mode],
            GL_UNSIGNED_BYTE,
            img_data,
        )

        # Unbind Texture
        glBindTexture(GL_TEXTURE_2D, 0)

    ###################################################################
    #
    #   Tell openGL to use this Texture
    #
    ###################################################################
    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.imgid)

    ###################################################################
    #
    #   Load the image file
    #   @param
    #   path    - The path to the image
    #   @out
    #   tex     - Texture object
    #
    ###################################################################
    @staticmethod
    def loadFromFile(path):
        # load file
        img = PIL.Image.open(path)

        # generate texture
        tex = Texture(img.size[0], img.size[1], img)
        del img
        return tex


###################################################################
#
#   Skybox class, needs texture class.
#
###################################################################
class Skybox:

    ###################################################################
    #   @param
    #   top     - Texture object for the top of the box
    #   bottom  - Texture object for the bottom of the box
    #   left    - TExture object for the left of the box
    #   right   - Texture object for the tight of the box
    #   front   - Texture object for the front of the box
    #   back    - Texture object for the back of the box
    ###################################################################
    def __init__(self, top, bottom, left, right, front, back):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.front = front
        self.back = back

        self.init_skybox_as_gl_list()

    def init_skybox_as_gl_list(self):
        self.skybox = glGenLists(1)
        glNewList(self.skybox, GL_COMPILE)

        # Enable/Disable features
        glPushAttrib(GL_ENABLE_BIT)
        glEnable(GL_TEXTURE_2D)

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_BLEND)

        smallnumber = 0.002
        # Just in case we set all vertices to white.
        glColor4f(1, 1, 1, 1)

        # Render the front quad
        self.front.bind()
        glBegin(GL_QUADS)
        glTexCoord2f(0 + smallnumber, 0 + smallnumber)
        glVertex3f(0.5, -0.5, -0.5)
        glTexCoord2f(0 + smallnumber, 1 - smallnumber)
        glVertex3f(0.5, 0.5, -0.5)
        glTexCoord2f(1 - smallnumber, 1 - smallnumber)
        glVertex3f(-0.5, 0.5, -0.5)
        glTexCoord2f(1 - smallnumber, 0 + smallnumber)
        glVertex3f(-0.5, -0.5, -0.5)
        glEnd()

        # Render the left quad
        self.left.bind()
        glBegin(GL_QUADS)
        glTexCoord2f(0 + smallnumber, 1 - smallnumber)
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(1 - smallnumber, 1 - smallnumber)
        glVertex3f(0.5, 0.5, -0.5)
        glTexCoord2f(1 - smallnumber, 0 + smallnumber)
        glVertex3f(0.5, -0.5, -0.5)
        glTexCoord2f(0 + smallnumber, 0 + smallnumber)
        glVertex3f(0.5, -0.5, 0.5)
        glEnd()

        # Render the back quad
        self.back.bind()
        glBegin(GL_QUADS)
        glTexCoord2f(0 + smallnumber, 0 + smallnumber)
        glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(0 + smallnumber, 1 - smallnumber)
        glVertex3f(-0.5, 0.5, 0.5)
        glTexCoord2f(1 - smallnumber, 1 - smallnumber)
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(1 - smallnumber, 0 + smallnumber)
        glVertex3f(0.5, -0.5, 0.5)
        glEnd()

        # Render the right quad
        self.right.bind()
        glBegin(GL_QUADS)
        glTexCoord2f(0 + smallnumber, 0 + smallnumber)
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(0 + smallnumber, 1 - smallnumber)
        glVertex3f(-0.5, 0.5, -0.5)
        glTexCoord2f(1 - smallnumber, 1 - smallnumber)
        glVertex3f(-0.5, 0.5, 0.5)
        glTexCoord2f(1 - smallnumber, 0 + smallnumber)
        glVertex3f(-0.5, -0.5, 0.5)
        glEnd()

        # Render the top quad
        self.top.bind()
        glBegin(GL_QUADS)
        glTexCoord2f(1 - smallnumber, 0 + smallnumber)
        glVertex3f(-0.5, 0.5, -0.5)
        glTexCoord2f(0 + smallnumber, 0 + smallnumber)
        glVertex3f(0.5, 0.5, -0.5)
        glTexCoord2f(0 + smallnumber, 1 - smallnumber)
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(1 - smallnumber, 1 - smallnumber)
        glVertex3f(-0.5, 0.5, 0.5)
        glEnd()

        # Render the bottom quad
        self.bottom.bind()
        glBegin(GL_QUADS)
        glTexCoord2f(0 + smallnumber, 0 + smallnumber)
        glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(0 + smallnumber, 1 - smallnumber)
        glVertex3f(0.5, -0.5, -0.5)
        glTexCoord2f(1 - smallnumber, 1 - smallnumber)
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1 - smallnumber, 0 + smallnumber)
        glVertex3f(-0.5, -0.5, 0.5)
        glEnd()

        # Restore enable bits and matrix
        glPopAttrib()
        glEndList()

    def draw(self):
        ###################################################################
        #
        #   Draw the skybox. First time running this will generate the DL
        #
        ###################################################################
        glCallList(self.skybox)


###################################################################
#
#       Model Class. Load and store obj models
#
###################################################################


class Model:
    vertices = []
    normals = []
    texcoords = []
    faces = []
    mtl = []
    DLID = 0

    def generateDL(self):
        currentMTL = ""
        # generate new display list
        self.DLID = glGenLists(1)
        # configure Display List
        glNewList(self.DLID, GL_COMPILE)
        # Enable blend
        glEnable(GL_BLEND)

        # Draw all faces
        for a in range(len(self.faces)):

            face = self.faces[a]

            if not (str(face.mtl) == str(currentMTL)):
                try:
                    self.mtl[face.mtl].useMTL()
                except:
                    pass

            glBegin(GL_TRIANGLES)

            ####### Vertex 1 #########
            n1 = self.normals[face.normal.x]
            glNormal3f(n1.x, n1.y, n1.z)

            try:
                t1 = self.texcoords[face.tex.x]
                glTexCoord2f(t1.x, t1.y)
            except:
                pass

            v1 = self.vertices[face.vertex.x]
            glVertex3f(v1.x, v1.y, v1.z)

            ####### Vertex 2 #########
            n2 = self.normals[face.normal.y]
            glNormal3f(n2.x, n2.y, n2.z)

            try:
                t2 = self.texcoords[face.tex.y]
                glTexCoord2f(t2.x, t2.y)
            except:
                pass

            v2 = self.vertices[face.vertex.y]
            glVertex3f(v2.x, v2.y, v2.z)

            ####### Vertex 3 #########
            n3 = self.normals[face.normal.z]
            glNormal3f(n3.x, n3.y, n3.z)

            try:
                t3 = self.texcoords[face.tex.z]
                glTexCoord2f(t3.x, t3.y)
            except:
                pass

            v3 = self.vertices[face.vertex.z]
            glVertex3f(v3.x, v3.y, v3.z)

            glEnd()
        glDisable(GL_BLEND)
        glEndList()
        return self.DLID

    def draw(self):
        glCallList(self.DLID)

    ###################################################################
    #
    #   Parses the obj file
    #   @param
    #   folder  - string of the folder in which the file is located
    #   file    - string of the name of the file
    #   @out
    #   m       - Model object
    #
    ###################################################################
    @staticmethod
    def loadModel(folder, filename):
        path = PurePath(folder, filename)       
        m = Model()
        currentMTL = ""
        mtlpath = ""

        with open(path) as f:
            for line_raw in f:   
                line = line_raw.strip()     
                splitted_line = line.split(" ")

                if line.startswith("mtllib "):
                    mtlpath = splitted_line[1]
                    try:
                        m.mtl = Materialm.loadMTL(folder, mtlpath)
                    except:
                        pass
                elif line.startswith("v "):
                    x = float(splitted_line[1])
                    y = float(splitted_line[2])
                    z = float(splitted_line[3])
                    m.vertices.append(Vector3f(x, y, z))
                elif line.startswith("vn "):
                    x = float(splitted_line[1])
                    y = float(splitted_line[2])
                    z = float(splitted_line[3])
                    m.normals.append(Vector3f(x, y, z))
                elif line.startswith("vt "):
                    x = float(splitted_line[1])
                    y = float(splitted_line[2])
                    m.texcoords.append(Vector2f(x, y))
                elif line.startswith("usemtl "):
                    currentMTL = splitted_line[1]
                elif line.startswith("f "):
                    # couple the vertices
                    vx = int(splitted_line[1].split("/")[0]) - 1
                    vy = int(splitted_line[2].split("/")[0]) - 1
                    vz = int(splitted_line[3].split("/")[0]) - 1
                    vertexIndices = Vector3f(vx, vy, vz)
                    # couple the texcoordinates
                    textureIndices = []
                    try:
                        tx = int(splitted_line[1].split("/")[1]) - 1
                        ty = int(splitted_line[2].split("/")[1]) - 1
                        tz = int(splitted_line[3].split("/")[1]) - 1
                        textureIndices = Vector3f(tx, ty, tz)
                    except:
                        pass
                    # couple normals
                    nx = int(splitted_line[1].split("/")[2]) - 1
                    ny = int(splitted_line[2].split("/")[2]) - 1
                    nz = int(splitted_line[3].split("/")[2]) - 1
                    normalIndices = Vector3f(nx, ny, nz)

                    m.faces.append(
                        Face(vertexIndices, normalIndices, textureIndices, currentMTL)
                    )

        return m


###################################################################
#
#   Face class for the model.
#
###################################################################
class Face:
    ###################################################################
    #
    #   @param
    #   vertex  -   Vector3f object, containing the vertexindices
    #   normal  -   Vector3f object, containing the normalindices
    #   tex     -   Vector2f object, containing the tecoordindices
    #   mtl     -  String containing the name of the material
    #
    ###################################################################
    def __init__(self, vertex, normal, tex, mtl):
        self.vertex = vertex
        self.normal = normal
        self.tex = tex
        self.mtl = mtl

    def __str__(self):
        return (
            "Vertexindices: "
            + str(self.vertex)
            + "\n"
            + "TextureIndices: "
            + str(self.tex)
            + "\n"
            + "NormalIndices: "
            + str(self.normal)
            + "\n"
            + "Material name: "
            + str(self.mtl)
        )


###################################################################
#   Material class for the model
#
###################################################################
class Materialm:
    ambient = []
    diffuse = []
    specular = []
    alpha = 0
    shininess = 0
    tex = []

    def __init__(self, name):
        self.name = name

    ###################################################################
    #
    #   Parses the mtl file
    #   @param
    #   folder  - string of the folder in which the file is located
    #   file    - string of the name of the file
    #   @out
    #   mtllist - Dictionary containing all materials in the mtl file
    #
    ###################################################################
    @staticmethod
    def loadMTL(folder, filename):
        path = PurePath(folder, filename)
        mtllist = dict()
        # data = open(path)
        # lines = data.read().splitlines()
        # data.close()

        currentMTL = ""
        adjust = 1

        with open(path) as f:
            for line_raw in f:
                line = line_raw.strip()
                splitted_line = line.split(" ")

                if line.startswith("newmtl"):
                    currentMTL = splitted_line[1]
                    mtllist[currentMTL] = Materialm(currentMTL)
                elif line.startswith("Ns ") and len(currentMTL) > 0:
                    mtllist[currentMTL].shininess = float(splitted_line[1])
                elif line.startswith("Ka ") and len(currentMTL) > 0:
                    Kax = float(splitted_line[1])
                    Kay = float(splitted_line[2])
                    Kaz = float(splitted_line[3])
                    mtllist[currentMTL].ambient = Vector3f(
                        Kax * adjust, Kay * adjust, Kaz * adjust
                    )
                elif line.startswith("Kd ") and len(currentMTL) > 0:
                    Kdx = float(splitted_line[1])
                    Kdy = float(splitted_line[2])
                    Kdz = float(splitted_line[3])
                    mtllist[currentMTL].diffuse = Vector3f(
                        Kdx * adjust, Kdy * adjust, Kdz * adjust
                    )
                elif line.startswith("Ks ") and len(currentMTL) > 0:
                    Ksx = float(splitted_line[1])
                    Ksy = float(splitted_line[2])
                    Ksz = float(splitted_line[3])
                    mtllist[currentMTL].specular = Vector3f(
                        Ksx * adjust, Ksy * adjust, Ksz * adjust
                    )
                elif line.startswith("d ") and len(currentMTL) > 0:
                    mtllist[currentMTL].alpha = float(splitted_line[1])
                elif line.startswith("map_Kd ") and len(currentMTL) > 0:
                    try:
                        mtllist[currentMTL].tex = Texture.loadFromFile(
                            folder + "/" + splitted_line[1]
                        )
                    except:
                        print("hier")
        return mtllist

    ###################################################################
    #
    #   Tell openGL the material properties
    #
    ###################################################################
    def useMTL(self):

        glMaterialfv(
            GL_FRONT,
            GL_AMBIENT,
            [self.ambient.x, self.ambient.y, self.ambient.z, self.alpha],
        )
        glMaterialfv(
            GL_FRONT,
            GL_DIFFUSE,
            [self.diffuse.x, self.diffuse.y, self.diffuse.z, self.alpha],
        )
        glMaterialfv(
            GL_FRONT,
            GL_SPECULAR,
            [self.specular.x, self.specular.y, self.specular.z, self.alpha],
        )
        glMaterialf(GL_FRONT, GL_SHININESS, self.shininess)

        try:
            glEnable(GL_TEXTURE_2D)
            self.tex.bind()
        except:
            glDisable(GL_TEXTURE_2D)

    def __str__(self):
        return (
            self.name + "\n"
            "ambient: " + str(self.ambient) + "\n"
            "diffuse: " + str(self.diffuse) + "\n"
            "specular: " + str(self.specular) + "\n"
            "alpha: " + str(self.alpha) + "\n"
            "Shininess:" + str(self.shininess)
        )


###################################################################
#
#       Font Utility class. Used to render Fonts in openGL
#       Uses The Texture class. To make a font, use F2IBuilder
#       By avid de Almeida Ferreira
#
###################################################################
class Font:
    def __init__(self, fontpath, gridsize, initfont, spacing):
        self.tex = Texture.loadFromFile(fontpath)
        self.gridsize = gridsize
        self.initfont = initfont
        self.spacing = spacing

    def drawString(self, yourstring, fontsize, xloc, yloc, red=1, green=1, blue=1):
        dispwidth = glutGet(GLUT_WINDOW_WIDTH)
        dispheight = glutGet(GLUT_WINDOW_HEIGHT)
        gs = self.gridsize
        spacing = self.spacing
        glPushAttrib(GL_ENABLE_BIT)
        glDisable(GL_CULL_FACE)
        glDisable(GL_LIGHTING)
        glClear(GL_DEPTH_BUFFER_BIT)
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(red, green, blue, 1)

        self.tex.bind()
        scale = fontsize / float(self.initfont)

        # switch to 2D view
        changeto2D()
        glTranslatef(xloc, yloc, 0)
        glPushMatrix()
        glScalef(
            scale * dispheight / 6.0, scale * dispheight / 6.0, scale * dispheight / 6.0
        )
        for a in range(len(yourstring)):
            letter = yourstring[a]
            x = ord(letter) % gs
            y = gs - int(ord(letter) / gs) - 1
            width = 1.0 / gs
            glBegin(GL_QUADS)
            glTexCoord2f((x + spacing) * width, y * width + width)
            glVertex2f(0, 0)
            glTexCoord2f((x + 1 - spacing) * width, y * width + width)
            glVertex2f(1 - 2 * spacing, 0)
            glTexCoord2f((x + 1 - spacing) * width, y * width)
            glVertex2f(1 - 2 * spacing, 1)
            glTexCoord2f((x + spacing) * width, y * width)
            glVertex2f(0, 1)
            glEnd()
            glTranslatef(1 - 2 * spacing, 0, 0)
        backto3D()
        glPopMatrix()
        glPopAttrib()

    def getHeight(self, fontsize):
        dispheight = glutGet(GLUT_WINDOW_HEIGHT)
        scale = fontsize / float(self.initfont)
        return scale * dispheight / 6.0

    def getWidth(self, fontsize, string):
        dispheight = glutGet(GLUT_WINDOW_HEIGHT)
        scale = fontsize / float(self.initfont)
        spacing = self.spacing
        return scale * dispheight / 6.0 * (1 - 2 * spacing) * len(string)


###################################################################
#
#       Button Utility. Makes use of Font and Texture
#
###################################################################
class Button:
    mouselocX = 0
    mouselocY = 0
    mouseover = False
    font = None

    def __init__(self, x, y, text, buttonid, font, fontsize):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.fontsize = fontsize
        self.height = font.getHeight(fontsize)
        self.width = font.getWidth(fontsize, text)
        self.buttonid = buttonid

    def isButton(self):
        if (
            Button.mouselocX > self.x
            and Button.mouselocX < self.x + self.width
            and Button.mouselocY > self.y
            and Button.mouselocY < self.y + self.height
        ):
            self.mouseover = True
            return self.buttonid
        else:
            self.mouseover = False
            return 0

    def draw(self):
        height = self.height
        width = self.width
        changeto2D()
        if self.mouseover:
            glColor3f(1, 1, 1)
        else:
            glColor3f(0, 0, 0)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x, self.y + height)
        glVertex2f(self.x + width, self.y + height)
        glVertex2f(self.x + width, self.y)
        glEnd()
        try:
            if self.mouseover:
                self.font.drawString(self.text, self.fontsize, self.x, self.y, 0, 0, 0)
            else:
                self.font.drawString(self.text, self.fontsize, self.x, self.y, 1, 1, 1)
        except:
            print("here")
        backto3D()

    @staticmethod
    def setFont(font):
        Button.font = font


###################################################################
#
#       Statusbars
#
###################################################################
class Statusbar:
    def __init__(self, x, y, width, height, borderwidth, red=0, green=1, blue=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.borderwidth = borderwidth
        self.red = red
        self.green = green
        self.blue = blue

    def draw(self, percentagefull):
        changeto2D()
        glLineWidth(self.borderwidth)
        glColor3f(0, 0, 0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x, self.y + self.height)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x + self.width, self.y)
        glEnd()
        glColor3f(self.red, self.green, self.blue)
        glBegin(GL_QUADS)
        glVertex2f(self.x + self.borderwidth / 2.0, self.y + self.borderwidth / 2.0)
        glVertex2f(
            self.x + self.borderwidth / 2.0,
            self.y + self.height - self.borderwidth / 2.0,
        )
        glVertex2f(
            self.x + percentagefull * self.width - self.borderwidth / 2.0,
            self.y + self.height - self.borderwidth / 2.0,
        )
        glVertex2f(
            self.x + percentagefull * self.width - self.borderwidth / 2.0,
            self.y + self.borderwidth / 2.0,
        )
        glEnd()

        backto3D()


###################################################################
#
#       Display methods
#
###################################################################
def changeto2D():
    dispwidth = glutGet(GLUT_WINDOW_WIDTH)
    dispheight = glutGet(GLUT_WINDOW_HEIGHT)
    glPushAttrib(GL_ENABLE_BIT)
    glDisable(GL_LIGHTING)
    glPushMatrix()
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, dispwidth, dispheight, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def backto3D():
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopAttrib()


###################################################################
#
#       Input help classes (Keyboard, Mouse)
#
###################################################################
class Mouse:
    x = 0
    y = 0
    dx = 0
    dy = 0
    grabbed = False
    leftdown = False

    @staticmethod
    def setGrabbed(boolean):
        if boolean:
            Mouse.grabbed = True
            Mouse.x = int(glutGet(GLUT_WINDOW_WIDTH) / 2)
            Mouse.y = int(glutGet(GLUT_WINDOW_HEIGHT) / 2)
            glutWarpPointer(Mouse.x, Mouse.y)
            glutSetCursor(GLUT_CURSOR_NONE)

        else:
            Mouse.grabbed = False
            glutSetCursor(GLUT_CURSOR_LEFT_ARROW)

    @staticmethod
    def mousemove(x, y):
        Mouse.dy = -(Mouse.y - glutGet(GLUT_WINDOW_HEIGHT) / 2)
        Mouse.dx = Mouse.x - glutGet(GLUT_WINDOW_WIDTH) / 2
        Mouse.y = y
        Mouse.x = x

    @staticmethod
    def mousefunc(button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_UP:
                Mouse.leftdown = False
            else:
                Mouse.leftdown = True

    @staticmethod
    def warp():
        glutWarpPointer(
            int(glutGet(GLUT_WINDOW_WIDTH) / 2), int(glutGet(GLUT_WINDOW_HEIGHT) / 2)
        )


class Keyboard:
    keypressed = [False] * 256
    keyhold = [False] * 256
    KEY_ESC = 27
    KEY_SPACE = 32

    @staticmethod
    def keyup(key, x, y):
        Keyboard.keypressed[ord(key)] = False
        Keyboard.keyhold[ord(key)] = False

    @staticmethod
    def keydown(key, x, y):
        if Keyboard.keypressed[ord(key)]:
            Keyboard.keyhold[ord(key)] = True
        Keyboard.keypressed[ord(key)] = True


###################################################################
#
#       Vector Utility class. Used in the model
#
###################################################################
class Vector3f:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "<" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ">"


class Vector2f:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "<" + str(self.x) + "," + str(self.y) + ">"
