import xml.dom.minidom
import os, sys
from shimstar.core.shimconfig import *


class asteroidTemplate():
    listOfTemplate = {}

    def __init__(self, id, name, egg, mass, text,eggMiddle,eggFar):
        self.idTemplate = id
        self.name = name
        self.egg = egg
        self.eggMiddle = eggMiddle
        self.eggFar = eggFar
        self.mass = mass
        self.text = text
        self.minerals = {}


    def getInfos(self):
        return self.name, self.egg, self.mass, self.text, self.eggMiddle, self.eggFar


    @staticmethod
    def loadXml():
        dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() + "config\\asteroids.xml")
        ast = dom.getElementsByTagName('asteroidtemplate')
        for a in ast:
            idtemplate = int(a.getElementsByTagName('idtemplate')[0].firstChild.data)
            name = str(a.getElementsByTagName('name')[0].firstChild.data)
            egg = str(a.getElementsByTagName('egg')[0].firstChild.data)
            eggMiddle = str(a.getElementsByTagName('eggmiddle')[0].firstChild.data)
            eggFar = str(a.getElementsByTagName('eggfar')[0].firstChild.data)
            mass = float(a.getElementsByTagName('mass')[0].firstChild.data)
            if a.getElementsByTagName('text')[0].firstChild != None:
                text = str(a.getElementsByTagName('text')[0].firstChild.data)
            ast = asteroidTemplate(idtemplate, name, egg, mass, text, eggMiddle, eggFar)
            asteroidTemplate.listOfTemplate[idtemplate] = ast
            minerals = a.getElementsByTagName('mineral')
            for m in minerals:
                id = int(m.getElementsByTagName('idmineral')[0].firstChild.data)
                nb = int(m.getElementsByTagName('nbmineral')[0].firstChild.data)
                ast.minerals[id] = nb


    def getMinerals(self):
        return self.minerals


    @staticmethod
    def getTemplate(idTemplate):
        if len(asteroidTemplate.listOfTemplate) == 0:
            asteroidTemplate.loadXml()
        if asteroidTemplate.listOfTemplate.has_key(idTemplate) == True:
            return asteroidTemplate.listOfTemplate[idTemplate]

        return None
		
