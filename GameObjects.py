from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from numpy import *
from AapUtils import *


class GameObject:
    def __init__(self, locX, locY, locZ):
        self.locX = locX
        self.locY = locY
        self.locZ = locZ


class Player(GameObject, object):
    def __init__(self, locX, locY, locZ, width, height):
        super(Player, self).__init__(locX, locY, locZ)
        self.width = width
        self.height = height


class Board(GameObject, object):
    texture = 0

    def __init__(self, locX, locY, locZ):
        super(Board, self).__init__(locX, locY, locZ)

    def draw(self):
        if Board.texture == 0:
            Board.texture = Texture.loadFromFile("./resources/textures/bullseye.png")
        modifier = 0
        if -self.locZ > 0:
            modifier = 180
        glPushAttrib(GL_ENABLE_BIT)
        glPushMatrix()
        glTranslatef(self.locX, self.locY, self.locZ)
        glRotatef(degrees(arctan(float(self.locX) / self.locZ)) + modifier, 0, 1, 0)
        glColor3f(0, 0, 0)
        self.texture.bind()
        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0)
        glVertex3f(-1, -1, 0)
        glTexCoord2f(1, 1)
        glVertex3f(-1, 1, 0)
        glTexCoord2f(0, 1)
        glVertex3f(1, 1, 0)
        glTexCoord2f(0, 0)
        glVertex3f(1, -1, 0)
        glEnd()
        glPopMatrix()
        glPopAttrib()

    def dist2D(self, otherX, otherZ):
        a = -self.locX
        b = -self.locZ
        c = -(a * self.locX + b * self.locZ)
        length = sqrt(a ** 2 + b ** 2)
        return (a * otherX + b * otherZ + c) / length

    def distToMid(self, otherX, otherY, otherZ):
        return sqrt(
            (self.locX - otherX) ** 2
            + (self.locY - otherY) ** 2
            + (self.locZ - otherZ) ** 2
        )

    @staticmethod
    def generateBoard():
        sign = [1, -1]
        x = (5 + random.randint(10, 20)) * sign[random.randint(0, 2)]
        z = (5 + random.randint(10, 20)) * sign[random.randint(0, 2)]
        return Board(x, 1, z)


#######################################################################
#
#   Arrow class
#
#######################################################################
class Arrow:
    launched = False
    grav = -9.81
    model = 0
    grounded = False
    hitboard = False

    def __init__(self, dist, height, horAngle, verAngle, model):
        self.dist = dist
        self.height = height
        self.horAngle = horAngle
        self.verAngle = verAngle
        self.model = model

    def launch(self, velocity):
        # Todo
        self.launched = True
        # get Velocity from main loop
        self.velocity = velocity * 30
        self.vx = self.velocity * cos(radians(self.verAngle))
        self.vy = self.velocity * sin(radians(self.verAngle))

        # fix initial condition such as horAngle, verAngle etc

        # horAngle = 0 means that the arrow is pointing in the negative z direction

        # REmove pass when checking for the code to work
        pass

    def update(self, deltatime, board, horAngle=None, verAngle=None):
        # Todo
        # Apply dynamics, physics etc.
        locX = -((self.dist) * sin(radians(self.horAngle)))
        locZ = -((self.dist) * cos(radians(self.horAngle)))
        self.grounded = self.height < 0
        self.tomidpoint = board.distToMid(locX, self.height, locZ)
        self.hitboard = not (
            board.dist2D(locX, locZ) > 0
            or (self.height > 2 and board.dist2D(locX, locZ) <= 0)
            or board.dist2D(locX, locZ) <= -2
            or self.tomidpoint > 1
        )
        if self.launched and not self.grounded and not self.hitboard:
            dx = self.vx * deltatime / 1000.0
            dy = self.vy * deltatime / 1000.0
            self.dist += dx
            self.height += dy
            self.vy += Arrow.grav * deltatime / 1000.0
            self.verAngle = degrees(arctan(float(dy) / dx))
            locX = -((self.dist) * sin(radians(self.horAngle)))
            locZ = -((self.dist) * cos(radians(self.horAngle)))
            self.hitboard = not (
                board.dist2D(locX, locZ) > 0
                or (self.height > 2 and board.dist2D(locX, locZ) <= 0)
                or board.dist2D(locX, locZ) <= -2
                or self.tomidpoint > 1
            )
            newdist = board.dist2D(locX, locZ)
            if newdist < 0 and self.hitboard:
                self.dist += newdist
                self.height += dy * newdist / dx

        elif not self.launched:
            self.verAngle = verAngle
            self.horAngle = -horAngle
        # i.e. rotation of arrow and trajectory
        # REmove pass when checking for the code to work

        pass

    def draw(self):
        # Todo
        # Draw the arrow
        # Remove pass when having implemented the code
        if self.launched:
            glPushMatrix()
            glRotatef(self.horAngle, 0, 1, 0)
            glTranslatef(0, self.height, -self.dist)
            glRotatef(self.verAngle, 1, 0, 0)
            glRotatef(-90, 1, 0, 0)
            glScalef(0.5, 0.5, 0.5)
            self.model.draw()
            glPopMatrix()
        else:
            glPushMatrix()
            glRotatef(self.horAngle, 0, 1, 0)
            glRotatef(self.verAngle, 1, 0, 0)
            glRotatef(-90, 1, 0, 0)
            glTranslatef(0, self.dist, 0)
            glScalef(0.5, 0.5, 0.5)
            self.model.draw()
            glPopMatrix()
        pass
