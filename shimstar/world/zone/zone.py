import xml.dom.minidom
import os, sys
from direct.stdpy import threading

from shimstar.core.shimconfig import *
from shimstar.world.zone.asteroid import *
from shimstar.world.zone.station import *
from shimstar.user.user import *
from shimstar.npc.npc import *

C_TYPEZONE_SPACE=1
C_TYPEZONE_STATION=2

class Zone(threading.Thread):
	instance=None
	def __init__(self,id):
		threading.Thread.__init__(self)
		self.stopThread=False
		self.listOfAsteroid=[]
		self.listOfStation=[]
		self.npc=[]
		self.junks=[]
		self.listOfWormHole=[]
		self.listOfUsers={}
		self.typeZone=0
		self.boxEgg=""
		self.boxScale=0
		self.file=""
		self.id=id
		Zone.instance=self
		self.typeZone=0
		self.box=None
		self.loadXml()
		
	@staticmethod
	def getInstance():
		return Zone.instance
		
	def getNpcById(self,id):
		for user in self.npc:
			if user.getId()==id:
				return user
		return None
		
	def getListOfNPC(self):
		return self.npc
		
	def run(self):
		while not self.stopThread:
			self.runUpdatePosChar()
			self.runNpc()
			#~ self.runUpdatePosNPC()
			self.runNewShot()
			self.runUpdateShot()
			
		print "le thread Zone " + str(self.id) + " s'est termine proprement"
		
	def runNpc(self):
		self.runNewNpc()
		self.runUpdatePosNPC()
		self.runDamageNpc()
		self.runRemoveNpc()
		
	def runRemoveNpc(self):
		tempMsg=NetworkZoneServer.getInstance().getListOfMessageById(C_NETWORK_REMOVE_NPC)
		if len(tempMsg)>0:
			for msg in tempMsg:
				netMsg=msg.getMessage()
				idNpc=int(netMsg[0])
				npcToRemove=None
				for n in self.npc:
					if n.getId()==idNpc:
						n.destroy()
						npcToRemove=n
				if npcToRemove!=None:
					self.npc.remove(npcToRemove)
				NetworkZoneServer.getInstance().removeMessage(msg)
		
	def runDamageNpc(self):
		tempMsg=NetworkZoneServer.getInstance().getListOfMessageById(C_NETWORK_TAKE_DAMAGE_NPC)
		
		if len(tempMsg)>0:
			for msg in tempMsg:
				netMsg=msg.getMessage()
				idNpc=int(netMsg[0])
				damage=int(netMsg[1])
				for n in self.npc:
					if n.getId()==idNpc:
						n.takeDamage(damage)
				NetworkZoneServer.getInstance().removeMessage(msg)
		
	def runNewNpc(self):
		tempMsg=NetworkZoneServer.getInstance().getListOfMessageById(C_NETWORK_NPC_INCOMING)
		if len(tempMsg)>0:
			for msg in tempMsg:
				netMsg=msg.getMessage()
				npcPart=netMsg[0]
				xmlPart = xml.dom.minidom.parseString(npcPart)
				id=int(xmlPart.getElementsByTagName('idnpc')[0].firstChild.data)
				existingNpc=self.getNpcById(id)
				if existingNpc==None:
					temp=NPC(npcPart)
					temp.setPos((float(netMsg[1]),float(netMsg[2]),float(netMsg[3])))
					temp.setQuat((float(netMsg[4]),float(netMsg[5]),float(netMsg[6]),float(netMsg[7])))
					self.npc.append(temp)
				NetworkZoneServer.getInstance().removeMessage(msg)
		
	def runUpdatePosChar(self):
		tempMsg=NetworkZoneUdp.getInstance().getListOfMessageById(C_NETWORK_CHARACTER_UPDATE_POS)
		
		if len(tempMsg)>0:
			for msg in tempMsg:
				netMsg=msg.getMessage()
				usr=int(netMsg[0])
				charact=int(netMsg[1])
				User.getInstance().getCurrentCharacter().getShip().setHprToGo((netMsg[2],netMsg[3],netMsg[4],netMsg[5]))
				User.getInstance().getCurrentCharacter().getShip().setPosToGo((netMsg[6],netMsg[7],netMsg[8]))
				NetworkZoneUdp.getInstance().removeMessage(msg)
			
	def runUpdatePosNPC(self):
		tempMsg=NetworkZoneUdp.getInstance().getListOfMessageById(C_NETWORK_NPC_UPDATE_POS)
		
		if len(tempMsg)>0:
			for msg in tempMsg:
				netMsg=msg.getMessage()
				npcId=int(netMsg[0])
				for n in self.npc:
						if npcId==n.getId():
							#~ print "npc pos " + str((netMsg[5],netMsg[6],netMsg[7]))
							n.ship.setHprToGo((netMsg[1],netMsg[2],netMsg[3],netMsg[4]))
							n.ship.setPosToGo((netMsg[5],netMsg[6],netMsg[7]))
				NetworkZoneUdp.getInstance().removeMessage(msg)
			
	def runNewShot(self):
		tempMsg=NetworkZoneServer.getInstance().getListOfMessageById(C_NETWORK_NEW_SHOT)
		
		if len(tempMsg)>0:
			for msg in tempMsg:
				netMsg=msg.getMessage()
				usrID=int(netMsg[0])
				bulId=int(netMsg[1])
				pos=(netMsg[2],netMsg[3],netMsg[4])
				quat=(netMsg[5],netMsg[6],netMsg[7],netMsg[8])
				user=User.getUserById(usrID)
				Bullet.lock.acquire()
				user.getCurrentCharacter().addBullet(bulId,pos,quat)
				Bullet.lock.release()
				NetworkZoneServer.getInstance().removeMessage(msg)
		
	def runUpdateShot(self):
		tempMsg=NetworkZoneServer.getInstance().getListOfMessageById(C_NETWORK_REMOVE_SHOT)
		if len(tempMsg)>0:
			for msg in tempMsg:
				netMsg=msg.getMessage()
				Bullet.lock.acquire()
				Bullet.removeBullet(netMsg[0])
				Bullet.lock.release()
				NetworkZoneServer.getInstance().removeMessage(msg)
				
		tempMsg=NetworkZoneUdp.getInstance().getListOfMessageById(C_NETWORK_POS_SHOT)
		if len(tempMsg)>0:
			for msg in tempMsg:
				netMsg=msg.getMessage()
				Bullet.lock.acquire()
				bulId=int(netMsg[0])
				b=Bullet.getBullet(bulId)
				if b!=None:
					b.setPos((float(netMsg[1]),float(netMsg[2]),float(netMsg[3])))
				Bullet.lock.release()
				NetworkZoneUdp.getInstance().removeMessage(msg)
		
	def stop(self):
		self.stopThread=True

	def loadXml(self):
		dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() +"config\\zones.xml")
		zs=dom.getElementsByTagName('zone')
		for z in zs:
			id=int(z.getElementsByTagName('id')[0].firstChild.data)
			if id==self.id:
				self.name=str(z.getElementsByTagName('name')[0].firstChild.data)
				self.typeZone=int(z.getElementsByTagName('typezone')[0].firstChild.data)
				self.egg=str(z.getElementsByTagName('egg')[0].firstChild.data)
				self.scale=float(z.getElementsByTagName('scale')[0].firstChild.data)
				self.music=str(z.getElementsByTagName('music')[0].firstChild.data)
				#~ if self.visible==True:
				self.box = loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() +self.egg)
				self.box.setScale(self.scale)
				self.box.reparentTo(render)
				self.box.setLightOff()
				self.box.clearFog()
				asts=z.getElementsByTagName('asteroid')
				for a in asts:
					self.listOfAsteroid.append(Asteroid(a))
					
				stations=z.getElementsByTagName('station')
				for s in stations:
					stationLoaded=Station(0,s)
					self.listOfStation.append(stationLoaded)
					
				#~ wormHole=z.getElementsByTagName('wormhole')
				#~ for w in wormHole:
					#~ wormHoleLoaded=wormhole(w)
					#~ self.listOfWormHole.append(wormHoleLoaded)
					
	def getMusic(self):
		return self.music
		
	def getName(self):
		return self.name
		
	def getId(self):
		return self.id
		
	def getTypeZone(self):
		return self.typeZone
		
	@staticmethod
	def getTinyInfosFromZone(idZone):
		dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() +"config\\zones.xml")
		zs=dom.getElementsByTagName('zone')
		for z in zs:
			id=int(z.getElementsByTagName('id')[0].firstChild.data)
			if id==idZone:
				name=str(z.getElementsByTagName('name')[0].firstChild.data)
				typezone=int(z.getElementsByTagName('typezone')[0].firstChild.data)
				return name,typezone
		return None,None
		
	def destroy(self):
		"""
			destructor
		"""
		for aster in self.listOfAsteroid:
			aster.destroy()
		for sta in self.listOfStation:
			sta.destroy()
		for worm in self.listOfWormHole:
			worm.destroy()
		for npc in self.npc:
			npc.destroy()  
		for j in self.junks:
			j.destroy()
		self.box.detachNode()
		self.box.removeNode()
		