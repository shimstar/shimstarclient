from pandac.PandaModules import *
from shimstar.core.shimconfig import *

class Junk:
    junkList = {}
    def __init__(self,id,pos=(0,0,0)):
        self.id = id
        self.pos = pos
        self.egg = "models/junk.bam"
        self.items={}
        self.node = loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() + self.egg)
        self.node.reparentTo(render)


    def addItem(self,item):
        self.items[item.getId()]=item

    def removeItem(self,item):
        if item.getId() in self.items:
            del self.items[item.getId()]

    def getItems(self):
        return self.items

    def getId(self):
        return self.id

    def getPos(self):
        return self.pos

    def setPos(self,pos):
        self.pos=pos
        if self.node is not None and  not self.isEmpty():
            self.node.setPos(pos)

    def destroy(self):
        if self.node is not None and  not self.isEmpty():
            self.node.detachNode()
            self.node.removeNode()
