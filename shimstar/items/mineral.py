import xml.dom.minidom
import os, sys
from shimstar.core.constantes import *
from shimstar.core.decorators import *
from shimstar.core.shimconfig import *

class Mineral:
	def __init__(self,idTemplate):
		self.id=0
		self.typeItem=C_ITEM_MINERAL
		self.name=""
		self.img=""
		self.cost=0
		self.sell=0
		self.space=0
		self.template=idTemplate
		self.quantity=0
		self.loadMineral()
		
	def getTemplate(self):
		return self.template
		
	def setId(self,id):
		self.id=id
		
	def getId(self):
		return self.id
		
	def setQuantity(self,q):
		self.quantity=q
		
	def getQuantity(self):
		return self.quantity
	
	def loadMineral(self):
		#~ dom = xml.dom.minidom.parse("config/mineral.xml")
		dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() +"config\\mineral.xml")
		minerals=dom.getElementsByTagName('mineral')
		for m in minerals:
			idMineral=int(m.getElementsByTagName('id')[0].firstChild.data)
			if self.template==idMineral:
				self.name=m.getElementsByTagName('name')[0].firstChild.data
				self.img=m.getElementsByTagName('img')[0].firstChild.data
				self.space=float(m.getElementsByTagName('space')[0].firstChild.data)
				#~ self.cost=int(m.getElementsByTagName('cost')[0].firstChild.data)
				#~ self.sell=int(m.getElementsByTagName('sell')[0].firstChild.data)
				break
				
	def addMineral(self,qt):
		self.quantity+=qt

	def removeMineral(self,qt):
		self.quantity-=qt
					
	def getId(self):
		return self.id
				
	def getSpace(self):
		return self.space
		
	def getTypeItem(self):
		return self.typeItem
				
	def getName(self):
		return self.name
		
	def getImg(self):
		return self.img
				
	def getCost(self):
		return self.cost
		
	def getSell(self):
		return self.sell