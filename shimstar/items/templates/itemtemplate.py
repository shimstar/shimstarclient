import xml.dom.minidom
import os, sys
from shimstar.core.shimconfig import *
from shimstar.core.constantes import *

class ItemTemplate(object):
	listOfTemplate={}
	
	def __init__(self,xmlPart):
		self.skillItems={}
		self.templateId=int(xmlPart.getElementsByTagName('templateid')[0].firstChild.data)
		self.name=str(xmlPart.getElementsByTagName('name')[0].firstChild.data)
		self.cost=int(xmlPart.getElementsByTagName('cost')[0].firstChild.data)
		self.sell=int(xmlPart.getElementsByTagName('sell')[0].firstChild.data)
		self.energyCost=int(xmlPart.getElementsByTagName('energyCost')[0].firstChild.data)
		self.space=int(xmlPart.getElementsByTagName('space')[0].firstChild.data)
		self.img=str(xmlPart.getElementsByTagName('img')[0].firstChild.data)
		self.typeItem=int(xmlPart.getElementsByTagName('typeitem')[0].firstChild.data)
		self.location=int(xmlPart.getElementsByTagName('location')[0].firstChild.data)
		ItemTemplate.listOfTemplate[self.templateId]=self
		skillItems=xmlPart.getElementsByTagName('skillitem')
		for s in skillItems:
			sk=int(xmlPart.getElementsByTagName('skillid')[0].firstChild.data)
			lvl=int(xmlPart.getElementsByTagName('skilllevel')[0].firstChild.data)
			self.skillItems[sk]=lvl
		
	def getTypeItem(self):
		return self.typeItem
		
	def getInfos(self):
		return self.name,self.cost,self.sell,self.energyCost,self.space,self.img,self.location,self.typeItem
		
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
	def loadXml():
		dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() +"config\\itemtemplates.xml")
		it=dom.getElementsByTagName('item')
		for i in it:
			typeitem=int(i.getElementsByTagName('typeitem')[0].firstChild.data)
			ItemTemplate(i)
		
	@staticmethod
	def getListOfTemplate():
		if len(itemTemplate.listOfTemplate)==0:
			itemTemplate.loadXml()
		return itemTemplate.listOfTemplate
		
	@staticmethod
	def getTemplate(idTemplate):
		if len(ItemTemplate.listOfTemplate)==0:
			ItemTemplate.loadXml()
		if ItemTemplate.listOfTemplate.has_key(idTemplate)==True:
			return ItemTemplate.listOfTemplate[idTemplate]
			
		return None
		
