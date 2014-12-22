import os, sys
from shimstar.core.constantes import *
from shimstar.core.decorators import *
from shimstar.items.templates.enginetemplate import *
from shimstar.items.item import *

class Engine(ShimstarItem):
	def __init__(self,templateId=None,xmlPart=None):
		print "Engine::init " + str(templateId)
		super(Engine,self).__init__(templateId,C_ITEM_ENGINE,xmlPart)	
		self.typeItem=C_ITEM_ENGINE
		self.speedMax=0
		self.fileToSound=""
		self.idTemplate=templateId
		if xmlPart!=None:
			self.loadXml(xmlPart)
		else:
			temp=EngineTemplate.getTemplate(self.idTemplate)
			self.name,self.speedMax,self.acceleration,self.cost,self.sell,self.energyCost,self.space,self.img,self.location,self.fileToSound,self.skillsItem=temp.getInfos()		
			
		
	def loadXml(self,xmlPart):
		self.id=int(xmlPart.getElementsByTagName('iditem')[0].firstChild.data)
		self.idTemplate=int(xmlPart.getElementsByTagName('template')[0].firstChild.data)
		temp=EngineTemplate.getTemplate(self.idTemplate)
		self.name,self.speedMax,self.acceleration,self.cost,self.sell,self.energyCost,self.space,self.img,self.location,self.fileToSound,self.skillsItem=temp.getInfos()		
		if len(xmlPart.getElementsByTagName('place'))>0:
			self.place=int(xmlPart.getElementsByTagName('place')[0].firstChild.data)
		if len(xmlPart.getElementsByTagName('location'))>0:
			self.location=int(xmlPart.getElementsByTagName('location')[0].firstChild.data)
		
	def getAcceleration(self):
		return self.acceleration
		
	def getFileToSound(self):
		return self.fileToSound

	def getSpeedMax(self):
		return self.speedMax
		
	