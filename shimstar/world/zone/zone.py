import xml.dom.minidom
import os, sys
from direct.stdpy import threading

from shimstar.core.shimconfig import *
from shimstar.world.zone.asteroid import *
from shimstar.world.zone.station import *

C_TYPEZONE_SPACE=1
C_TYPEZONE_STATION=2

class Zone(threading.Thread):
	instance=None
	def __init__(self,id):
		threading.Thread.__init__(self)
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
		
	def run(self):
		while not self.stopThread:
			pass
			
		print "le thread Zone " + str(self.id) + " s'est termine proprement"
		
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
		