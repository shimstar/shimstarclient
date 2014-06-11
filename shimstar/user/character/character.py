import xml.dom.minidom
import os, sys

from shimstar.network.networkmainserver import *
from shimstar.network.message import *
from shimstar.network.netmessage import *
from shimstar.game.gamestate import *
from shimstar.items.ship import *


class Character:
	def __init__(self,id,name,egg,idZone,userRef):
		self.id=id
		self.name=name
		self.face=egg
		self.coin=0
		self.current=False
		self.ship=None
		self.idZone=idZone
		self.lastStation=0
		self.visible=False
		self.userRef=userRef #user obj
		self.readDialogs=[]
		print "character::init" + str(self.id)
		
	def getReadDialogs(self):
		return self.readDialogs
		
	def appendDialogs(self,id):
		if (id in self.readDialogs)==False:
			self.readDialogs.append(id)
			return True
		return False
		
	def manageDeath(self):
		if self.ship!=None:
			self.ship.destroy()
			self.ship=None
				
	def setShip(self,idShip,idTemplate,hullpoints,visible=True):
		#~ print "character :: setsHip " + str(hullpoints)
		self.ship=Ship(idShip,idTemplate,hullpoints,visible)
		self.ship.setOwner(self)
		print "character:setShip" + str(self.ship)
	
	def destroy(self):
		if self.ship!=None:
			self.ship.destroy()
			self.ship=None
			
	def takeDamage(self,damage):
		#~ print "character::takedamage " + str(damage)
		if self.ship!=None:
			return self.ship.takeDamage(damage)
		return None
				
	def setPos(self,pos):
		self.ship.setPos(pos)
	
	def setQuat(self,quat):
		self.ship.setQuat(quat)
				
	def getUserId(self):
		return self.userRef.getId()
				
	def run(self):
		if self.ship!=None:
			self.ship.move()
				
	def getShip(self):
		return self.ship
		
	def addBullet(self,bulId,pos,quat):
		self.ship.addBullet(bulId,pos,quat)
		
	def getName(self):
		return self.name
		
	def getId(self):
		return self.id
		
	def getIdZone(self):
		return self.idZone
		
	def getFace(self):
		return self.face
		
	def setCurrent(self,current):
		self.current=current
		
	def isCurrent(self):
		return self.current
		
	def changeZone(self,death=False):
		if GameState.getInstance().getNewZone()!=0:			
			self.idZone=GameState.getInstance().getNewZone()
		msg=netMessage(C_NETWORK_USER_CHANGE_ZONE)
		msg.addUInt(self.userRef.getId())
		msg.addUInt(self.id)
		msg.addUInt(self.idZone)
		NetworkMainServer.getInstance().sendMessage(msg)
		if self.ship!=None:
			self.ship.changeZone()
		if death:
			GameState.getInstance().setState(C_DEATH)
		else:
			GameState.getInstance().setState(C_CHANGEZONE)
		return 

		
		