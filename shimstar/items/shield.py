import os, sys
from shimstar.core.constantes import *
from shimstar.core.decorators import *
from shimstar.items.templates.shieldtemplate import *
from shimstar.items.item import *


class Shield(ShimstarItem):
    def __init__(self, templateId=None, xmlPart=None):
        # print "Shield::init " + str(templateId)
        super(Shield, self).__init__(templateId, C_ITEM_SHIELD, xmlPart)
        self.typeItem = C_ITEM_SHIELD
        self.hitpoints = 0

        self.tempoLoad = 0
        self.fileToSound = ""
        self.idTemplate = templateId
        if xmlPart != None:
            self.loadXml(xmlPart)
        else:
            temp = ShieldTemplate.getTemplate(self.idTemplate)
            self.name, self.hitpoints, self.tempoLoad, self.cost, self.sell, self.energyCost, self.space, self.img, self.location, self.fileToSound, self.skillsItem = temp.getInfos()


    def loadXml(self, xmlPart):
        self.id = int(xmlPart.getElementsByTagName('iditem')[0].firstChild.data)
        self.idTemplate = int(xmlPart.getElementsByTagName('template')[0].firstChild.data)
        temp = ShieldTemplate.getTemplate(self.idTemplate)
        self.name, self.hitpoints, self.tempoLoad, self.cost, self.sell, self.energyCost, self.space, self.img, self.location, self.fileToSound, self.skillsItem = temp.getInfos()
        if len(xmlPart.getElementsByTagName('place')) > 0:
            self.place = int(xmlPart.getElementsByTagName('place')[0].firstChild.data)
        if len(xmlPart.getElementsByTagName('location')) > 0:
            self.location = int(xmlPart.getElementsByTagName('location')[0].firstChild.data)


    def getHitPoints(self):
        return self.hitpoints


    def getTempoLoad(self):
        return self.tempoLoad


    def getSpeedMax(self):
        return self.speedMax
