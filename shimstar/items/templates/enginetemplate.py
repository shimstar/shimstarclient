import xml.dom.minidom
import os, sys
from shimstar.core.shimconfig import *
from shimstar.core.constantes import *
from shimstar.items.templates.itemtemplate import *

class EngineTemplate(ItemTemplate):
	listOfTemplate={}
	
	def __init__(self,xmlPart):
		super(EngineTemplate,self).__init__(xmlPart)
		self.speedMax=int(xmlPart.getElementsByTagName('speedMax')[0].firstChild.data)
		self.acceleration=int(xmlPart.getElementsByTagName('acceleration')[0].firstChild.data)
		self.sound=str(xmlPart.getElementsByTagName('sound')[0].firstChild.data)
		EngineTemplate.listOfTemplate[self.templateId]=self
		
		
	def getInfos(self):
		print "EngineTemplate::getInfo"
		return self.name,self.speedMax,self.acceleration,self.cost,self.sell,self.energyCost,self.space,self.img,self.location,self.sound,self.skillItems
	
	@staticmethod
	def loadXml():
		dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() +"config\\itemtemplates.xml")
		it=dom.getElementsByTagName('item')
		for i in it:
			typeitem=int(i.getElementsByTagName('typeitem')[0].firstChild.data)
			if typeitem==C_ITEM_ENGINE:
				EngineTemplate(i)
		
	def getSpeedMax(self):
		return self.speedMax
		
	def getAcceleration(self):
		return self.acceleration
		
	@staticmethod
	def getTemplate(idTemplate):
		
		if len(EngineTemplate.listOfTemplate)==0:
			EngineTemplate.loadXml()
		if EngineTemplate.listOfTemplate.has_key(idTemplate)==False:
			EngineTemplate.loadXml()
		if EngineTemplate.listOfTemplate.has_key(idTemplate)==True:
			return EngineTemplate.listOfTemplate[idTemplate]
			
		return None
		
