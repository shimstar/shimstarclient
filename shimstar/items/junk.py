from pandac.PandaModules import *
from shimstar.core.shimconfig import *
from direct.stdpy import threading

class Junk:
    junkList = []
    def __init__(self,id,pos=(0,0,0)):
        self.id = id
        self.lock = threading.Lock()
        self.pos = pos
        self.name = "junk"
        self.egg = "models/junk.bam"
        self.img = "junk"
        self.items={}
        self.node = loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() + self.egg)
        self.node.setName("junk" + str(self.id))
        self.node.setTag("classname", "junk")
        self.node.setTag("id", str(self.id))
        self.node.reparentTo(render)
        self.node.setPos(pos)
        Junk.junkList.append(self)

    @staticmethod
    def getJunkById(id):
        for junk in Junk.junkList:
            if junk.id == id:
                return junk
        return None

    def getName(self):
        return self.name

    def getNode(self):
        return self.node

    def addItem(self,item):
        self.items[item.getId()]=item

    def removeItemById(self,id):
        itemToRemove = None
        if id in self.items:
            itemToRemove=self.items[id]
            del self.items[id]
        return itemToRemove

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
        self.lock.acquire()
        if self.node is not None and  not self.node.isEmpty():
            self.node.detachNode()
            self.node.removeNode()
        Junk.junkList.remove(self)
        self.lock.release()
