import os, sys
from shimstar.items.engine import *
from shimstar.items.weapon import *
#~ from shimstar.items.reactor import *

class Slot:
	def __init__(self,xmlPart,id=0):
		self.id=id
		self.location=0
		self.types=[]
		self.nb=0
		self.item=None
		self.loadXml(xmlPart)
			
	def loadXml(self,xmlPart):
		self.id=int(xmlPart.getElementsByTagName('id')[0].firstChild.data)
		self.location=int(xmlPart.getElementsByTagName('location')[0].firstChild.data)
		typeString=str(xmlPart.getElementsByTagName('types')[0].firstChild.data)
		tabTypes=typeString.split(",")
		for t in tabTypes:
			self.types.append(int(t))
		self.numero=	int(xmlPart.getElementsByTagName('numero')[0].firstChild.data)
		itemXml=xmlPart.getElementsByTagName('slotitem')
		for itXml in itemXml:
			typeItem=int(itXml.getElementsByTagName('typeitem')[0].firstChild.data)
			itTemplate=int(itXml.getElementsByTagName('template')[0].firstChild.data)
			if typeItem==C_ITEM_ENGINE:
				self.item=Engine(itTemplate)
			elif typeItem==C_ITEM_WEAPON:
					self.item=Weapon(itTemplate)
			#~ elif typeItem==C_ITEM_MINING:
				#~ self.item=mining(0,itXml)
			#~ else:
				#~ self.item=ShimstarItem(itTemplate)
			
	def getTypes(self):
		return self.types
		
	def setItem(self,item):
		self.item=item
	
	def getNb(self):
		return self.nb
		
	def getLocation(self):
		return self.location
		
	def getId(self):
		return self.id
		
	def getItem(self):
		return self.item