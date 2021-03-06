import xml.dom.minidom
import os, sys
from shimstar.core.shimconfig import *
from shimstar.core.constantes import *
from shimstar.items.templates.itemtemplate import *

class MiningTemplate(ItemTemplate):
	listOfTemplate={}
	
	def __init__(self,xmlPart):
		super(MiningTemplate,self).__init__(xmlPart)
		self.vitesse=float(xmlPart.getElementsByTagName('vitesse')[0].firstChild.data)
		self.perf=float(xmlPart.getElementsByTagName('perf')[0].firstChild.data)
		self.nb=int(xmlPart.getElementsByTagName('nbextract')[0].firstChild.data)
		self.range=int(xmlPart.getElementsByTagName('range')[0].firstChild.data)
		self.minerals=[]
		minerals=xmlPart.getElementsByTagName('mineraltomine')
		for m in minerals:
			self.minerals.append(int(m.firstChild.data))
		MiningTemplate.listOfTemplate[self.templateId]=self
		
		
	def getInfos(self):
		return self.name,self.range,self.vitesse,self.perf,self.nb,self.minerals,self.cost,self.sell,self.energyCost,self.space,self.img,self.location,self.skillItems
	
	@staticmethod
	def loadXml():
		dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() +"config\\itemtemplates.xml")
		it=dom.getElementsByTagName('item')
		for i in it:
			typeitem=int(i.getElementsByTagName('typeitem')[0].firstChild.data)
			if typeitem==C_ITEM_MINING:
				MiningTemplate(i)
		
	def getVitesse(self):
		return self.vitesse
		
	def getNb(self):
		return self.nb
		
	def getPerf(self):
		return self.perf
		
	def getMinerals(self):
		return self.minerals
				
	@staticmethod
	def getTemplate(idTemplate):
		if len(MiningTemplate.listOfTemplate)==0:
			MiningTemplate.loadXml()
		if MiningTemplate.listOfTemplate.has_key(idTemplate)==True:
			return MiningTemplate.listOfTemplate[idTemplate]
			
		return None
		
