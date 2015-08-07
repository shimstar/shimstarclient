import xml.dom.minidom
import os, sys
from shimstar.core.shimconfig import *


class Station:
    stations = []

    def __init__(self, id, xmlPart=None, inSpace=True):
        self.id = id
        self.inSpace = inSpace
        self.name = ""
        self.egg = ""
        self.node = None
        self.image = "station"
        self.exitZone = 0
        self.file = ""
        self.screen = ""
        if xmlPart != None:
            self.loadFromXmlPart(xmlPart)
        else:
            self.loadXml()
        Station.stations.append(self)


    def loadXml(self):
        dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() + "config\\stations.xml")
        stations = dom.getElementsByTagName('station')
        for s in stations:
            id = int(s.getElementsByTagName('idstation')[0].firstChild.data)
            if id == self.id:
                self.name = str(s.getElementsByTagName('name')[0].firstChild.data)
                self.exitZone = int(s.getElementsByTagName('exitzone')[0].firstChild.data)
                npcs = s.getElementsByTagName('idnpc')
                for n in npcs:
                    self.npc.append(NPCInStation(int(n.firstChild.data)))


    def loadFromXmlPart(self, xmlPart):
        """ Player is in space, and we need to load xmlPart from zone config xml file """
        """ we need to display the egg of the station """
        self.id = int(xmlPart.getElementsByTagName('idstation')[0].firstChild.data)
        self.name = str(xmlPart.getElementsByTagName('name')[0].firstChild.data)
        posx = float(xmlPart.getElementsByTagName('posx')[0].firstChild.data)
        posy = float(xmlPart.getElementsByTagName('posy')[0].firstChild.data)
        posz = float(xmlPart.getElementsByTagName('posz')[0].firstChild.data)
        hprh = float(xmlPart.getElementsByTagName('hprh')[0].firstChild.data)
        hprp = float(xmlPart.getElementsByTagName('hprp')[0].firstChild.data)
        hprr = float(xmlPart.getElementsByTagName('hprr')[0].firstChild.data)
        self.mass = float(xmlPart.getElementsByTagName('mass')[0].firstChild.data)
        self.egg = str(xmlPart.getElementsByTagName('egg')[0].firstChild.data)
        self.scale = float(xmlPart.getElementsByTagName('scale')[0].firstChild.data)
        self.exitZone = int(xmlPart.getElementsByTagName('exitzone')[0].firstChild.data)
        self.pos = (posx, posy, posz)
        self.hpr = (hprh, hprp, hprr)
        if self.inSpace == True:
            self.node = loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() + self.egg)
            self.node.reparentTo(render)
            self.node.setName(self.name)
            self.node.setPos(self.pos)
            self.node.setHpr(self.hpr)
            self.node.setTag("name", "station")
            self.node.setTag("classname", "station")
            self.node.setTag("id", str(self.id))
            self.node.setShaderAuto()


    @staticmethod
    def getStationById(id, visible=True):
        for s in Station.stations:
            if str(s.getId()) == str(id):
                return s
        s = Station(id, None, visible)
        return s


    def getId(self):
        return self.id


    def destroy(self):
        if self.node != None and not self.node.isEmpty():
            self.node.detachNode()
            self.node.removeNode()
        if Station.stations.count(self) > 0:
            Station.stations.remove(self)


    def getClassName(self):
        return self.className


    def getName(self):
        return self.name

    def getImage(self):
        return self.image


    def getNode(self):
        return self.node


    def getPos(self):
        return self.node.getPos()


    def getListOfNpc(self):
        return self.npc


    def getExitZone(self):
        return self.exitZone
