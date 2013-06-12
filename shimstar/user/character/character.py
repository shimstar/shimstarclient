import xml.dom.minidom
import os, sys

from shimstar.network.networkmainserver import *
from shimstar.network.message import *
from shimstar.network.netmessage import *
from shimstar.game.gamestate import *
from shimstar.items.ship import *


class Character:
	def __init__(self,xmlPart,userRef):
		self.id=0
		self.name=0
		self.face=""
		self.coin=0
		self.current=False
		self.ship=None
		self.idZone=0
		self.lastStation=0
		self.visible=False
		self.loadXmlPart(xmlPart)
		self.userRef=userRef
		
	def loadXmlPart(self,xmlPart):
		self.name=str(xmlPart.getElementsByTagName('name')[0].firstChild.data)
		self.face=str(xmlPart.getElementsByTagName('face')[0].firstChild.data)
		self.coin=int(xmlPart.getElementsByTagName('coin')[0].firstChild.data)
		self.idZone=int(xmlPart.getElementsByTagName('zone')[0].firstChild.data)
		self.lastStation=int(xmlPart.getElementsByTagName('laststation')[0].firstChild.data)
		self.id=int(xmlPart.getElementsByTagName('idchar')[0].firstChild.data)
		
		sh=xmlPart.getElementsByTagName('ship')
		if sh!=None:
			for s in sh:
				self.ship=Ship(0,s)
		
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
		
	def changeZone(self):
		if GameState.getInstance().getNewZone()!=0:			
			self.idZone=GameState.getInstance().getNewZone()
		msg=netMessage(C_NETWORK_USER_CHANGE_ZONE)
		msg.addInt(self.userRef.getId())
		msg.addInt(self.id)
		msg.addInt(self.idZone)
		NetworkMainServer.getInstance().sendMessage(msg)
		self.ship.changeZone()
		GameState.getInstance().setState(C_CHANGEZONE)
		return 

		
		