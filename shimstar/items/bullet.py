from pandac.PandaModules import Point3, Vec3, Vec4
from pandac.PandaModules import *
from direct.showbase import Audio3DManager
from shimstar.core.functions import *
from shimstar.game.gamestate import *
from shimstar.items.weapon import *
from shimstar.core.shimconfig import *
from math import sqrt
from direct.stdpy import threading


class Bullet(threading.Thread):
    listOfBullet = {}
    lock = threading.Lock()

    def __init__(self, id, pos, quat, egg, range, speed, weapon, sound):
        threading.Thread.__init__(self)
        self.id = id
        self.lock = threading.Lock()
        self.weapon = weapon
        self.lastMove = globalClock.getRealTime()
        self.fileToSound = sound
        self.bulletSound = None
        self.node = None
        try:
            self.node = loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() + "models/" + egg)
        except:
            print "Bullet:__init__ loadModel failed on " + str(
                shimConfig.getInstance().getConvRessourceDirectory() + "models/" + egg) + " #### egg=" + str(egg)
        if self.node != None:
            self.node.setPos(pos)
            self.initPos = self.node.getPos()
            self.node.setQuat(Quat(quat))
            forward = self.node.getQuat().getForward()
            forward.normalize()
            self.node.reparentTo(render)
            self.range = range
            self.lastMove = globalClock.getRealTime()
            self.speed = speed
            Bullet.listOfBullet[self.id] = self

    @staticmethod
    def getBullet(id):
        if Bullet.listOfBullet.has_key(id) == True:
            return Bullet.listOfBullet[id]
        else:
            return None

    @staticmethod
    def getBullets():
        return Bullet.listOfBullet

    @staticmethod
    def removeBullet(id):
        if Bullet.listOfBullet.has_key(id) == True:
            # ~ Bullet.listOfBullet[id].lock.acquire()
            Bullet.listOfBullet[id].destroy()
            del Bullet.listOfBullet[id]

    def initAudio(self):
        audio3d = shimConfig.getInstance().getAudio3DManager()
        self.bulletSound = audio3d.loadSfx(shimConfig.getInstance().getConvRessourceDirectory() + self.fileToSound)
        audio3d.setSoundVelocityAuto(self.bulletSound)
        audio3d.setListenerVelocityAuto()
        audio3d.attachSoundToObject(self.bulletSound, self.node)
        self.bulletSound.setLoop(True)
        self.bulletSound.play()
        audio3d.setDropOffFactor(0.8)

    def getWeapon(self):
        return self.weapon

    def getClassName(self):
        return bullet.className

    def getPos(self):
        return self.node.getPos()

    def getHpr(self):
        return self.node.getHpr()

    def setHpr(self, hpr):
        self.node.setHpr(hpr)

    def setPos(self, pos):
        self.node.setPos(pos)

    def destroy(self):
        # ~ audio3d = shimConfig.getInstance().getAudio3DManager()
        #~ audio3d.detachSound(self.bulletSound)
        #~ audio3d.detachSound(self.node)
        #~ self.node.setLightOff()
        self.lock.acquire()
<<<<<<< HEAD
=======

>>>>>>> b5efca133cb488ec5bc3d44f7de126d3fddedf91
        try:
            self.node.detachNode()
            self.node.removeNode()
        except:
<<<<<<< HEAD
            print "Exception : Bullet remove node"
=======
            print "exception : exception in release node in bullet"
>>>>>>> b5efca133cb488ec5bc3d44f7de126d3fddedf91
            self.lock.release()
            self.node = None


    def stateBullet(self):
        """
        determines if a bullet is at end of life or not
        return 1, if the bullet must be destroyed, 0 otherwise
        """
        distance = self.calcDistance()
        if distance > self.range:
            return 1
        return 0


    def calcDistance(self):
        pos1 = self.initPos
        pos2 = self.node.getPos()
        dx = pos1.getX() - pos2.getX()
        dy = pos1.getY() - pos2.getY()
        dz = pos1.getZ() - pos2.getZ()
        distance = int(round(sqrt(dx * dx + dy * dy + dz * dz), 0))
        return distance


    def move(self):
        self.lock.acquire()
        dt = globalClock.getRealTime() - self.lastMove
        self.lastMove = globalClock.getRealTime()
        if dt < 1 and dt > -1:
<<<<<<< HEAD
=======

>>>>>>> b5efca133cb488ec5bc3d44f7de126d3fddedf91
            if self.node != None and self.node.isEmpty() != True:
                try:
                    self.node.setPos(self.node, Vec3(0, 1 * dt * self.speed, 0))
                except:
<<<<<<< HEAD
                    print "Exception : Bullet setPos"
=======
                    print "exception in move bullet"
>>>>>>> b5efca133cb488ec5bc3d44f7de126d3fddedf91
        self.lock.release()


    def getName(self):
        return self.name


    def getName(self):
        return self.name
	
