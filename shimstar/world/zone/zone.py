import xml.dom.minidom
import os, sys
from direct.stdpy import threading

from shimstar.core.shimconfig import *
from shimstar.world.zone.asteroid import *
from shimstar.world.zone.station import *
from shimstar.user.user import *
from shimstar.npc.npc import *
from shimstar.core.constantes import *

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
			self.runUpdatePosNPC()
			self.runNewShot()
			self.runUpdateShot()
			
		print "le thread Zone " + str(self.id) + " s'est termine proprement"
		
	def runNpc(self):
		self.runNewIncoming()
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
				NPC.lock.acquire()
				for n in self.npc:
					if n.getId()==idNpc:
						n.destroy()
						npcToRemove=n
				if npcToRemove!=None:
					self.npc.remove(npcToRemove)
				NPC.lock.release()
				NetworkZoneServer.getInstance().removeMessage(msg)
				
	def runNewIncoming(self):
		tempMsg=NetworkZoneServer.getInstance().getListOfMessageById(C_NETWORK_CHAR_INCOMING)
		if len(tempMsg)>0:
			for msg in tempMsg:
				tabMsg=msg.getMessage()
				print tabMsg
				userXml=tabMsg[0]
				xmlPart = xml.dom.minidom.parseString(userXml)
				usrId=int(xmlPart.getElementsByTagName('iduser')[0].firstChild.data)
				charId=tabMsg[1]
				User.lock.acquire()
				if User.listOfUser.has_key(usrId)==False:
					tempUsr=User(userXml,False)
					tempUsr.chooseCharacter(charId)
					tempUsr.getCurrentCharacter().setPos((tabMsg[2],tabMsg[3],tabMsg[4]))
					tempUsr.getCurrentCharacter().setQuat((tabMsg[5],tabMsg[6],tabMsg[7],tabMsg[8]))
					self.listOfUsers[usrId]=tempUsr
				User.lock.release()
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
				id=netMsg[0]
				existingNpc=self.getNpcById(id)
				NPC.lock.acquire()
				if existingNpc==None:
					temp=NPC(id,netMsg[1],netMsg[2],netMsg[3])
					self.npc.append(temp)
				NPC.lock.release()
				NetworkZoneServer.getInstance().removeMessage(msg)
		
	def runUpdatePosChar(self):
		tempMsg=NetworkZoneUdp.getInstance().getListOfMessageById(C_NETWORK_CHARACTER_UPDATE_POS)
		
		if len(tempMsg)>0:
			for msg in tempMsg:
				netMsg=msg.getMessage()
				usr=int(netMsg[0])
				charact=int(netMsg[1])
				if usr==User.getInstance().getId():
					if  User.getInstance().getCurrentCharacter().getShip()!=None:
						User.getInstance().getCurrentCharacter().getShip().setHprToGo((netMsg[2],netMsg[3],netMsg[4],netMsg[5]))
						User.getInstance().getCurrentCharacter().getShip().setPosToGo((netMsg[6],netMsg[7],netMsg[8]))
				else:
					tempUser=User.getUserById(usr)
					if tempUser!=None:
						ch=tempUser.getCharacterById(charact)
						if ch!=None:
							if  ch.getShip()!=None:
								ch.getShip().setHprToGo((netMsg[2],netMsg[3],netMsg[4],netMsg[5]))
								ch.getShip().setPosToGo((netMsg[6],netMsg[7],netMsg[8]))
				NetworkZoneUdp.getInstance().removeMessage(msg)
			
	def runUpdatePosNPC(self):
		tempMsg=NetworkZoneUdp.getInstance().getListOfMessageById(C_NETWORK_NPC_UPDATE_POS)
		
		if len(tempMsg)>0:
			for msg in tempMsg:
				netMsg=msg.getMessage()
				nbNpc=int(netMsg[0])
				for itNbNpc in range (nbNpc):
					npcId=int(netMsg[1+itNbNpc*8])
					for n in self.npc:
							if npcId==n.getId():
								#~ NPC.lock.acquire()
								#~ print "npc pos " + str((netMsg[5],netMsg[6],netMsg[7]))
								n.ship.setHprToGo((netMsg[2+itNbNpc*8],netMsg[3+itNbNpc*8],netMsg[4+itNbNpc*8],netMsg[5+itNbNpc*8]))
								n.ship.setPosToGo((netMsg[6+itNbNpc*8],netMsg[7+itNbNpc*8],netMsg[8+itNbNpc*8]))
								#~ print "zone::runUpdatePosNPC pos Npc " + str(npcId) + "  :: " + str((netMsg[6+itNbNpc*8],netMsg[7+itNbNpc*8],netMsg[8+itNbNpc*8]))
								#~ NPC.lock.release()
				NetworkZoneUdp.getInstance().removeMessage(msg)
			
	def runNewShot(self):
		tempMsg=NetworkZoneServer.getInstance().getListOfMessageById(C_NETWORK_NEW_CHAR_SHOT)
		
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
				
		tempMsg=NetworkZoneServer.getInstance().getListOfMessageById(C_NETWORK_NEW_NPC_SHOT)
		if len(tempMsg)>0:
			for msg in tempMsg:
				netMsg=msg.getMessage()
				
				npcId=int(netMsg[0])
				bulId=int(netMsg[1])
				pos=(netMsg[2],netMsg[3],netMsg[4])
				quat=(netMsg[5],netMsg[6],netMsg[7],netMsg[8])
				n=NPC.getNPCById(npcId)
				if n!=None:
					Bullet.lock.acquire()
					n.addBullet(bulId,pos,quat)
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
		