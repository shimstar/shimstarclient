import xml.dom.minidom
import os, sys
from shimstar.core.shimconfig import *
from shimstar.core.constantes import *


class ItemTemplate(object):
    listOfTemplate = {}

    def __init__(self, xmlPart):
        self.skillItems = {}
        self.sound = ""
        self.templateId = int(xmlPart.getElementsByTagName('templateid')[0].firstChild.data)
        self.name = str(xmlPart.getElementsByTagName('name')[0].firstChild.data)
        self.cost = 0
        if len(xmlPart.getElementsByTagName('cost')) > 0:
            self.cost = int(xmlPart.getElementsByTagName('cost')[0].firstChild.data)
        self.sell = 0
        if len(xmlPart.getElementsByTagName('sell')) > 0:
            self.sell = int(xmlPart.getElementsByTagName('sell')[0].firstChild.data)
        self.energyCost = 0
        if len(xmlPart.getElementsByTagName('energyCost')) > 0:
            self.energyCost = int(xmlPart.getElementsByTagName('energyCost')[0].firstChild.data)
        self.space = 0
        if len(xmlPart.getElementsByTagName('space')) > 0:
            self.space = int(xmlPart.getElementsByTagName('space')[0].firstChild.data)
        self.img = str(xmlPart.getElementsByTagName('img')[0].firstChild.data)
        self.typeItem = int(xmlPart.getElementsByTagName('typeitem')[0].firstChild.data)
        self.location = 0
        if len(xmlPart.getElementsByTagName('location')) > 0:
            self.location = int(xmlPart.getElementsByTagName('location')[0].firstChild.data)
        skillItems = xmlPart.getElementsByTagName('skillitem')
        for s in skillItems:
            sk = int(xmlPart.getElementsByTagName('skillid')[0].firstChild.data)
            lvl = int(xmlPart.getElementsByTagName('skilllevel')[0].firstChild.data)
            self.skillItems[sk] = lvl
        ItemTemplate.listOfTemplate[str(self.typeItem) + "-" + str(self.templateId)] = self


    def getSound(self):
        return self.sound

    def getTemplateId(self):
        return self.templateId

    def getTypeItem(self):
        return self.typeItem

    def getInfos(self):
        return self.name, self.cost, self.sell, self.energyCost, self.space, self.img, self.location, self.typeItem

    def getName(self):
        return self.name

    def getSell(self):
        return self.sell

    def getSpace(self):
        return self.space

    def getImg(self):
        return self.img

    def getLocation(self):
        return self.location

    def getEnergyCost(self):
        return self.energyCost

    def getCost(self):
        return self.cost

    def getSkillsItem(self):
        return self.skillItems



    @staticmethod
    def getListOfTemplate():
        return ItemTemplate.listOfTemplate

    @staticmethod
    def getTemplateById(idTemplate):
        for i in ItemTemplate.listOfTemplate:
            if ItemTemplate.listOfTemplate[i].templateId == idTemplate:
                return ItemTemplate.listOfTemplate[i]

    @staticmethod
    def getTemplate(idTemplate, typeItem):
        if ItemTemplate.listOfTemplate.has_key(str(typeItem) + "-" + str(idTemplate)) == True:
            return ItemTemplate.listOfTemplate[str(typeItem) + "-" + str(idTemplate)]

        return None
		
