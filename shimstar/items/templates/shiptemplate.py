import xml.dom.minidom
import os, sys
from shimstar.core.shimconfig import *
from shimstar.core.constantes import *
from shimstar.items.templates.itemtemplate import *
from shimstar.items.slot import *

class ShipTemplate(ItemTemplate):
	listOfTemplate={}
	
	def __init__(self,xmlPart):
		#~ super(ShipTemplate,self).__init__(xmlPart)
		#~ print xmlPart.toxml()
		self.name=str(xmlPart.getElementsByTagName('name')[0].firstChild.data)
		self.maxHullPoints=int(xmlPart.getElementsByTagName('maxhullpoints')[0].firstChild.data)
		self.egg=str(xmlPart.getElementsByTagName('egg')[0].firstChild.data)
		self.img=str(xmlPart.getElementsByTagName('img')[0].firstChild.data)
		self.templateId=int(xmlPart.getElementsByTagName('templateid')[0].firstChild.data)
		slots=xmlPart.getElementsByTagName('slot')
		self.slots=[]
		ShipTemplate.listOfTemplate[self.templateId]=self
		for s in slots:
			tempSlot=Slot(s)
			self.slots.append(tempSlot)
		
	def getInfos(self):
		return self.name,self.maxHullPoints,self.egg,self.img,self.slots
	
	@staticmethod
	def loadXml():
		dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() +"config\\itemtemplates.xml")
		it=dom.getElementsByTagName('item')
		for i in it:
			typeitem=int(i.getElementsByTagName('typeitem')[0].firstChild.data)
			if typeitem==C_ITEM_SHIP:
				ShipTemplate(i)
		
	def getSpeedMax(self):
		return self.speedMax
		
	def getAcceleration(self):
		return self.acceleration
		
	@staticmethod
	def getTemplate(idTemplate):
		
		if len(ShipTemplate.listOfTemplate)==0:
			ShipTemplate.loadXml()
		if ShipTemplate.listOfTemplate.has_key(idTemplate)==False:
			ShipTemplate.loadXml()
			
		print ShipTemplate.listOfTemplate
		print "shiptemplate::getTempalte " + str(idTemplate)
		print ShipTemplate.listOfTemplate[idTemplate]
		if ShipTemplate.listOfTemplate.has_key(idTemplate)==True:
			return ShipTemplate.listOfTemplate[idTemplate]
			
		return None
		
