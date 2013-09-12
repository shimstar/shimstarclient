from shimstar.core.decorators import *
from shimstar.items.ship import *
from direct.stdpy import threading

class NPC(threading.Thread):
	lock=threading.Lock()
	listOfNpc=[]
	def __init__(self,xmlPart):
		threading.Thread.__init__(self)
		self.id=id
		self.idZone=0
		self.name=""
		self.faction=0
		self.loadFromXml(xmlPart)
		NPC.listOfNpc.append(self)
		print "NPC::__init__"  + str(self.id)
	
	@staticmethod
	def getNPCById(id):
		for n in NPC.listOfNpc:
			if n.getId()==id:
				return n
		return None
		
	def getName(self):
		return self.name
		
	def getId(self):
		return self.id
		
	def addBullet(self,bulId,pos,quat):
		self.ship.addBullet(bulId,pos,quat)
		
	def destroy(self):
		NPC.listOfNpc.delete(self)
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
				self.ship.setOwner(self)
		
	def setPos(self,pos):
		self.ship.setPos(pos)

	def setQuat(self,quat):
		self.ship.setQuat(quat)
		
	def takeDamage(self,dmg):
		self.ship.takeDamage(dmg)