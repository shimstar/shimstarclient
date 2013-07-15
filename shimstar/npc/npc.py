from shimstar.core.decorators import *
from shimstar.items.ship import *

class NPC:
	def __init__(self,xmlPart):
		self.id=id
		self.idZone=0
		self.name=""
		self.faction=0
		self.loadFromXml(xmlPart)
		print "NPC::__init__"  + str(self.id)
		
	def getName(self):
		return self.name
		
	def getId(self):
		return self.id
		
	def destroy(self):
		self.ship.destroy()
		
	def getShip(self):
		return self.ship
		
	def getFaction(self):
		return self.faction
		
	def run(self):
		self.ship.move()
		
	def loadFromXml(self,xmlPart):
		document = xml.dom.minidom.parseString(xmlPart)
		self.id=int(document.getElementsByTagName('idnpc')[0].firstChild.data)
		self.name=str(document.getElementsByTagName('name')[0].firstChild.data) + " " + str(self.id)
		self.idZone=int(document.getElementsByTagName('idZone')[0].firstChild.data)
		sh=document.getElementsByTagName('ship')
		if sh!=None:
			for s in sh:
				self.ship=Ship(0,s)
				self.ship.setVisible()
		
	def setPos(self,pos):
		self.ship.setPos(pos)

	def setQuat(self,quat):
		self.ship.setQuat(quat)
		
	def takeDamage(self,dmg):
		self.ship.takeDamage(dmg)