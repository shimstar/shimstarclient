import xml.dom.minidom
import os, sys
from shimstar.core.shimconfig import *
from shimstar.core.constantes import *
from shimstar.items.templates.itemtemplate import *


class ShieldTemplate(ItemTemplate):
    listOfTemplate = {}

    def __init__(self, xmlPart):
        super(ShieldTemplate, self).__init__(xmlPart)
        self.hitpoints =  int(xmlPart.getElementsByTagName('hp')[0].firstChild.data)
        self.tempoLoad = int(xmlPart.getElementsByTagName('tempo')[0].firstChild.data)
        ShieldTemplate.listOfTemplate[self.templateId] = self


    def getInfos(self):
        return self.name, self.hitpoints, self.tempoLoad, self.cost, self.sell, self.energyCost, self.space, self.img, self.location, self.sound, self.skillItems


    @staticmethod
    def loadXml():
        dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() + "config\\itemtemplates.xml")
        it = dom.getElementsByTagName('item')
        for i in it:
            typeitem = int(i.getElementsByTagName('typeitem')[0].firstChild.data)
            if typeitem == C_ITEM_SHIELD:
                ShieldTemplate(i)


    def getHitPoints(self):
        return self.hitpoints


    def getTempoLoad(self):
        return self.tempoLoad


    @staticmethod
    def getTemplate(idTemplate):
        if len(ShieldTemplate.listOfTemplate) == 0:
            ShieldTemplate.loadXml()
        if ShieldTemplate.listOfTemplate.has_key(idTemplate) == False:
            ShieldTemplate.loadXml()
        if ShieldTemplate.listOfTemplate.has_key(idTemplate) == True:
            return ShieldTemplate.listOfTemplate[idTemplate]

        return None

