import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import Texture
from pandac.PandaModules import BillboardEffect
from direct.task.Task import Task
from shimstar.core.shimconfig import *


class Explosion:
    nbExplo = 0

    @staticmethod
    def preload():
        loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() + 'models/plane')
        for i in range(16):
            loader.loadTexture((shimConfig.getInstance().getConvRessourceDirectory() + 'models/explo2/exp' + "%0" + str(
                2) + "d." + 'png') % i)
        for i in range(16):
            loader.loadTexture((shimConfig.getInstance().getConvRessourceDirectory() + 'models/shieldstrike/shield' + "%0" + str(
                2) + "d." + 'png') % i)

    def __init__(self, render, pos, scale, nameExplo):
        self.expPlane = loader.loadModel(
            shimConfig.getInstance().getConvRessourceDirectory() + 'models/plane')  # load the object
        self.expPlane.setPos(pos)  # set the position
        self.expPlane.reparentTo(render)  # reparent to render
        self.expPlane.setTransparency(1)  # enable transparency
        self.expPlane.setScale(scale)
        self.timeFps = 0
        self.expPlane.setName("explo" + str(Explosion.nbExplo))

        # load the texture movie

        if nameExplo == "explosion":
            self.timeFps = 16
            self.expTexs = self.loadTextureMovie(16,
                                                 shimConfig.getInstance().getConvRessourceDirectory() + '/models/explo2/exp',
                                                 'png', padding=2)
        elif nameExplo == "shield":
            self.timeFps = 16
            self.expTexs = self.loadTextureMovie(16,
                                                 shimConfig.getInstance().getConvRessourceDirectory() + '/models/shieldstrike/shield',
                                                 'png', padding=2)


            #This create the "billboard" effect that will rotate the object so that it
            #is always rendered as facing the eye (camera)
        self.expPlane.node().setEffect(BillboardEffect.makePointEye())
        Explosion.nbExplo += 1


    def getName(self):
        if self.expPlane != None:
            return self.expPlane.getName()
        return None


    def getTimeFps(self):
        return self.timeFps


    def delete(self):
        if self.expPlane != None and self.expPlane.isEmpty() != True:
            self.expPlane.detachNode()
            self.expPlane.removeNode()
            self.expPlane = None


    def getExpPlane(self):
        return self.expPlane


    def getexpTexs(self):
        return self.expTexs


    # Our custom load function to load the textures needed for a movie into a
    #list. It assumes the the files are named
    #"path/name<serial number>.extention"
    #It takes the following arguments
    #Frames: The number of frames to load
    #name: The "path/name" part of the filename path
    #suffix: The "extention" part of the path
    #padding: The number of digit the serial number contians:
    #         e.g. if the serial number is 0001 then padding is 4
    def loadTextureMovie(self, frames, name, suffix, padding=1):
        #The following line is very complicated but does a lot in one line
        #Here's the explanation from the inside out:
        #first, a string representing the filename is built an example is:
        #"path/name%04d.extention"
        #The % after the string is an operator that works like C's sprintf function
        #It tells python to put the next argument (i) in place of the %04d
        #For more string formatting information look in the python manual
        #That string is then passed to the loader.loadTexture function
        #The loader.loadTexture command gets done in a loop once for each frame,
        #And the result is returned as a list.
        #For more information on "list comprehensions" see the python manual
        return [loader.loadTexture((name + "%0" + str(padding) + "d." + suffix) % i)
                for i in range(frames)]
