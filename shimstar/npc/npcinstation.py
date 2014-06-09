from shimstar.items.ship import *
from math import sqrt
from shimstar.user.user import *
#~ from shimstar.user.character.mission import *
from shimstar.core.constantes import *
from shimstar.core.decorators import *
from shimstar.npc.dialog import *
#~ from shimstar.user.character.mission import *
from shimstar.core.shimconfig import *

class NPCInStation:
	listOfNpc={}
	def __init__(self,id):
		self.id=id
		self.location=0
		self.name=""
		self.face=""
		self.typeNpc=0
		self.dialogs=[]
		self.missions=[]		
		self.loadXml()
		NPCInStation.listOfNpc[self.id]=self
			
	@staticmethod
	def getNPCById(idNpc):
		if NPCInStation.listOfNpc.has_key(idNpc)==False:
			NPCInStation(idNpc)
			
		return NPCInStation.listOfNpc[idNpc]
	
	@staticmethod
	def getListOfNPCByStation(idStation):
		dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() +"config\\pnjs.xml")
		pnjs=dom.getElementsByTagName('pnj')
		listOfNpc=[]
		for p in pnjs:
			idStationXml=int(p.getElementsByTagName('zone')[0].firstChild.data)
			if idStationXml==idStation:
				id=int(p.getElementsByTagName('id')[0].firstChild.data)
				listOfNpc.append(id)
		return listOfNpc
		
	def loadXml(self):
		dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() +"config\\pnjs.xml")
		pnjs=dom.getElementsByTagName('pnj')
		for p in pnjs:
			id=int(p.getElementsByTagName('id')[0].firstChild.data)
			if id == self.id:
				self.name=str(p.getElementsByTagName('name')[0].firstChild.data)
				self.face=str(p.getElementsByTagName('face')[0].firstChild.data)
				self.location=int(p.getElementsByTagName('zone')[0].firstChild.data)
				self.typeNpc=int(p.getElementsByTagName('typenpc')[0].firstChild.data)
				dialogues=p.getElementsByTagName('iddialogue')
				for diaXml in dialogues:
					iddiag=int(diaXml.firstChild.data)
					self.dialogs.append(dialog(iddiag))
					
				missions=p.getElementsByTagName('idmission')
				for missionsXml in missions:
					idm=int(missionsXml.firstChild.data)
					#~ self.missions.append(mission(idm))
					
	def getTypeNpc(self):
		return self.typeNpc
		
	def getDialogueFromKeyword(self,keyword):
		for d in self.dialogs:
			listOfKeywords=d.getKeywords()
			for k in listOfKeywords:
				if listOfKeywords[k]==keyword:
					return d
		return None
		
	def getMission(self,id):
		for m in self.missions:
			if m.getId()==int(id):
				return m
			
		return None

	def getListOfKeywords(self):
		keywords=[]
		for d in self.dialogs:
			keyw=d.getKeywords()
			for k in keyw:
				keywords.append(keyw[k])
				
		return keywords
		
	def getClassName(self):
		return 'NPC'
		
	def getPos(self):
		return self.ship.getPos()

	def getName(self):
		return self.name
		
	def getLocation(self):
		return self.location
		
	def getId(self):
		return self.id
		
	def getDialogs(self):
		return self.dialogs
		
	def getMissions(self):
		return self.missions
		
	def getFace(self):
		return self.face
		
	def getShip(self):
		return self.ship
		
	def destroy(self):
		self.ship.destroy()

