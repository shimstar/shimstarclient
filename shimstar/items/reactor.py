import os, sys
from shimstar.core.constantes import *
from shimstar.core.decorators import *
from shimstar.items.templates.reactortemplate import *
from shimstar.items.item import *

class Reactor(ShimstarItem):
    def __init__(self, templateId=None, xmlPart=None):
        # print "Shield::init " + str(templateId)
        super(Reactor, self).__init__(templateId, C_ITEM_ENERGY, xmlPart)
        self.typeItem = C_ITEM_ENERGY
        self.energy = 0

        self.fileToSound = ""
        self.idTemplate = templateId
        if xmlPart != None:
            self.loadXml(xmlPart)
        else:
            temp = ReactorTemplate.getTemplate(self.idTemplate)
            self.name, self.hitpoints, self.tempoLoad, self.cost, self.sell, self.energyCost, self.space, self.img, self.location, self.fileToSound, self.skillsItem = temp.getInfos()

    def loadXml(self, xmlPart):
        self.id = int(xmlPart.getElementsByTagName('iditem')[0].firstChild.data)
        self.idTemplate = int(xmlPart.getElementsByTagName('template')[0].firstChild.data)
        temp = ReactorTemplate.getTemplate(self.idTemplate)
        self.name, self.energy, self.cost, self.sell, self.energyCost, self.space, self.img, self.location, self.fileToSound, self.skillsItem = temp.getInfos()
        if len(xmlPart.getElementsByTagName('place')) > 0:
            self.place = int(xmlPart.getElementsByTagName('place')[0].firstChild.data)
        if len(xmlPart.getElementsByTagName('location')) > 0:
            self.location = int(xmlPart.getElementsByTagName('location')[0].firstChild.data)

    def getEnergy(self):
        return self.energy

