import xml.dom.minidom
import os, sys
from shimstar.core.shimconfig import *
from shimstar.items.templates.itemtemplate import *
from shimstar.core.constantes import *


class WeaponTemplate(ItemTemplate):
    listOfTemplate = {}

    def __init__(self, xmlPart):
        # ~ print "WeaponTemplate::init " + str(xmlPart.toxml())
        super(WeaponTemplate, self).__init__(xmlPart)
        self.damage = int(xmlPart.getElementsByTagName('damage')[0].firstChild.data)
        self.range = int(xmlPart.getElementsByTagName('range')[0].firstChild.data)
        self.egg = str(xmlPart.getElementsByTagName('egg')[0].firstChild.data)
        self.cadence = float(xmlPart.getElementsByTagName('cadence')[0].firstChild.data)
        self.speed = int(xmlPart.getElementsByTagName('speed')[0].firstChild.data)
        self.bulletSound = str(xmlPart.getElementsByTagName('bulletsound')[0].firstChild.data)
        WeaponTemplate.listOfTemplate[self.templateId] = self


    def getFrequency(self):
        return self.cadence

    def getSpeed(self):
        return self.speed

    def getImg(self):
        return self.img

    def getRange(self):
        return self.range

    def getDamage(self):
        return self.damage

    def getInfos(self):
        return self.name, self.egg, self.damage, self.range, self.cadence, self.speed, self.sell, self.energyCost, self.space, self.img, self.cost, self.bulletSound, self.skillItems

    @staticmethod
    def loadXml():
        dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() + "config\\itemtemplates.xml")
        it = dom.getElementsByTagName('item')
        for i in it:
            typeitem = int(i.getElementsByTagName('typeitem')[0].firstChild.data)
            if typeitem == C_ITEM_WEAPON:
                WeaponTemplate(i)


    @staticmethod
    def getTemplate(idTemplate):
        if len(WeaponTemplate.listOfTemplate) == 0:
            WeaponTemplate.loadXml()
        if WeaponTemplate.listOfTemplate.has_key(idTemplate) == False:
            WeaponTemplate.loadXml()
        if WeaponTemplate.listOfTemplate.has_key(idTemplate) == True:
            return WeaponTemplate.listOfTemplate[idTemplate]

        return None
		
