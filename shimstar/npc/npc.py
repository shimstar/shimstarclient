from shimstar.core.decorators import *
from shimstar.items.ship import *
from direct.stdpy import threading

class NPC(threading.Thread):
	lock=threading.Lock()
	listOfNpc=[]
	def __init__(self,id,name,template,idTemplateShip):
		threading.Thread.__init__(self)
		self.id=id
		self.template=template
		self.name=name
		self.faction=0
		self.ship=Ship(0,idTemplateShip)
		self.ship.setVisible()
		self.ship.setOwner(self)
		NPC.listOfNpc.append(self)
	
	@staticmethod
	def getListOfNpc():
		return NPC.listOfNpc
	
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
		NPC.listOfNpc.remove(self)
		self.ship.destroy()
		
	def getShip(self):
		return self.ship
		
	def getFaction(self):
		return self.faction
		
	def run(self):
		self.ship.move()
		
	def setPos(self,pos):
		self.ship.setPos(pos)

	def setQuat(self,quat):
		self.ship.setQuat(quat)
		
	def takeDamage(self,dmg):
		self.ship.takeDamage(dmg)