__author__ = 'ogilp'

from pandac.PandaModules import *
from panda3d.bullet import *

from shimstar.core.shimconfig import *

class ItemInSpace:
    listOfItem = {}
    def __init__(self,id,idtemplate):
        self.id = id
        self.idtemplate = idtemplate
        self.pos = (0,0,0)
        self.quat = None
        self.mass = 0
        self.img = ""
        self.name = ""
        self.scale = 1
        self.typeItem = 0
        self.egg = ""
        self.eggMiddle = ""
        self.eggFar = ""
        self.hullpoints = 0
        self.maxHullpoints = 0
        self.bodyNP = None
        self.world = None
        self.worldNP = None
        self.loadXml()
        ItemInSpace.listOfItem[seld.id]=self

    def loadXml(self):
        dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() + "config\\iteminspace.xml")
        items = dom.getElementsByTagName('iteminspacetemplate')
        for it in items:
            idtemplate = int(it.getElementsByTagName('idtemplate')[0].firstChild.data)
            if idtemplate == self.idtemplate:
                self.name = str(it.getElementsByTagName('name')[0].firstChild.data)
                self.egg = str(it.getElementsByTagName('egg')[0].firstChild.data)
                self.typeItem = int(it.getElementsByTagName('typeitem')[0].firstChild.data)
                self.scale = int(it.getElementsByTagName('scale')[0].firstChild.data)
                self.maxHullpoints= int(it.getElementsByTagName('hullpoints')[0].firstChild.data)

    def setPos(self,pos):
        self.pos=pos

    def setQuat(self,quat):
        self.quat=quat

    def loadEgg(self):
        self.node = loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() + self.egg)
        self.node.reparentTo(render)
        self.node.setName(self.name)
        self.node.setPos(self.pos)
        self.node.setQuat(self.quat)
        self.node.setShaderAuto()


    def destroy(self):
        if self.node is not None and not self.node.isEmpty():
            self.node.detachNode()
            self.node.removeNode()
            self.node = None
        if self.id in ItemInSpace.listOfItem:
            del ItemInSpace[self.id]
