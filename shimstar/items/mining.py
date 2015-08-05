import os, sys
from shimstar.core.constantes import *
from shimstar.core.decorators import *
from shimstar.items.templates.miningtemplate import *
from shimstar.items.item import *


class Mining(ShimstarItem):
    def __init__(self, templateId=None, xmlPart=None):
        # print "Shield::init " + str(templateId)
        super(Mining, self).__init__(templateId, C_ITEM_MINING, xmlPart)
        self.typeItem = C_ITEM_MINING
        self.distance = 0
        self.minerals = []
        self.fileToSound = ""
        self.idTemplate = templateId
        if xmlPart != None:
            self.loadXml(xmlPart)
        else:
            temp = MiningTemplate.getTemplate(self.idTemplate)
            self.name, self.distance, self.nb, self.minerals, self.cost, self.sell, self.energyCost, self.space, self.img, self.location, self.skillsItem = temp.getInfos()


    def loadXml(self, xmlPart):
        self.id = int(xmlPart.getElementsByTagName('iditem')[0].firstChild.data)
        self.idTemplate = int(xmlPart.getElementsByTagName('template')[0].firstChild.data)
        temp = MiningTemplate.getTemplate(self.idTemplate)
        self.name, self.distance, self.nb, self.minerals, self.cost, self.sell, self.energyCost, self.space, self.img, self.location, self.skillsItem = temp.getInfos()
        if len(xmlPart.getElementsByTagName('place')) > 0:
            self.place = int(xmlPart.getElementsByTagName('place')[0].firstChild.data)
        if len(xmlPart.getElementsByTagName('location')) > 0:
            self.location = int(xmlPart.getElementsByTagName('location')[0].firstChild.data)


    def getDistance(self):
        return self.distance

    def getNb(self):
        return self.nb

