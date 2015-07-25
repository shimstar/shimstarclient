import xml.dom.minidom
import os, sys
from shimstar.core.shimconfig import *
from shimstar.core.constantes import *
from shimstar.items.templates.itemtemplate import *


class ReactorTemplate(ItemTemplate):
    listOfTemplate = {}

    def __init__(self, xmlPart):
        super(ReactorTemplate, self).__init__(xmlPart)

        self.energy =  int(xmlPart.getElementsByTagName('energy')[0].firstChild.data)
        ReactorTemplate.listOfTemplate[self.templateId] = self


    def getInfos(self):
        return self.name, self.energy,self.cost, self.sell, self.energyCost, self.space, self.img, self.location, self.sound, self.skillItems


    @staticmethod
    def loadXml():
        dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() + "config\\itemtemplates.xml")
        it = dom.getElementsByTagName('item')
        for i in it:
            typeitem = int(i.getElementsByTagName('typeitem')[0].firstChild.data)
            if typeitem == C_ITEM_ENERGY:
                ReactorTemplate(i)


    def getHitPoints(self):
        return self.hitpoints


    def getTempoLoad(self):
        return self.tempoLoad


    @staticmethod
    def getTemplate(idTemplate):
        if len(ReactorTemplate.listOfTemplate) == 0:
            ReactorTemplate.loadXml()
        if ReactorTemplate.listOfTemplate.has_key(idTemplate) == False:
            ReactorTemplate.loadXml()
        if ReactorTemplate.listOfTemplate.has_key(idTemplate) == True:
            return ReactorTemplate.listOfTemplate[idTemplate]

        return None

