import os, sys
import xml.dom.minidom
from shimstar.core.decorators import *
from shimstar.npc.dialog import *
from shimstar.user.character.objectif import *
from shimstar.user.character.reward import *
from shimstar.core.shimconfig import *
from shimstar.core.constantes import *

class Mission:
	def __init__(self,id,ichar=0):
		self.id=int(id)
		self.label=""
		self.idChar=ichar
		self.preDialog=None
		self.currentDialog=None
		self.postDialog=None
		self.endingNPC=0
		self.status=0
		self.depMission=0
		self.objectifs=[]
		self.rewards=[]
		self.status=C_STATEMISSION_DONTHAVE
		self.loadXml()
		
	def loadXml(self):
		dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() +"config\\missions.xml")
		missions=dom.getElementsByTagName('mission')
		for m in missions:
			id=int(m.getElementsByTagName('idmission')[0].firstChild.data)
			if id == self.id:
				self.label=m.getElementsByTagName('label')[0].firstChild.data
				self.preDialog=dialog(int(m.getElementsByTagName('begindiag')[0].firstChild.data))
				self.currentDialog=dialog(int(m.getElementsByTagName('currentdiag')[0].firstChild.data))
				self.postDialog=dialog(int(m.getElementsByTagName('endingdiag')[0].firstChild.data))
				self.endingNPC=int(m.getElementsByTagName('endingnpc')[0].firstChild.data)
				self.depMission=int(m.getElementsByTagName('depmission')[0].firstChild.data)
				objectifs=m.getElementsByTagName('objectif')
				for o in objectifs:
					idobjectif=int(o.getElementsByTagName('idobjectif')[0].firstChild.data)
					idType=int(o.getElementsByTagName('idtype')[0].firstChild.data)
					text=o.getElementsByTagName('text')[0].firstChild.data
					idItem=int(o.getElementsByTagName('iditem')[0].firstChild.data)
					tableItem=o.getElementsByTagName('tableitem')[0].firstChild.data
					zone=int(o.getElementsByTagName('zone')[0].firstChild.data)
					nbItem=int(o.getElementsByTagName('nbitem')[0].firstChild.data)
					self.objectifs.append(Objectif(idobjectif,idType,text,idItem,tableItem,zone,nbItem))
				rewards=m.getElementsByTagName('reward')
				for r in rewards:
					idreward=int(r.getElementsByTagName('idreward')[0].firstChild.data)
					typereward=int(r.getElementsByTagName('typereward')[0].firstChild.data)
					templateitem=int(r.getElementsByTagName('templateitem')[0].firstChild.data)
					nb=int(r.getElementsByTagName('nb')[0].firstChild.data)
					self.rewards.append(Reward(idreward,typereward,templateitem,nb))

	def getDepMission(self):
		return self.depMission
		
	def getObjectifs(self):
		return self.objectifs

	def getId(self):
		return self.id
		
	def getRewards(self):
		return self.rewards
		
	def getEndingNPC(self):
		return self.endingNPC
		
	def getPreDialog(self):
		return self.preDialog
		
	def getCurrentDialog(self):
		return self.currentDialog
		
	def getPostDialog(self):
		return self.postDialog
	
	def setCharacterStatus(self,status):
		self.status=status
		
	def getStatus(self):
		return self.status
		
	def getLabel(self):
		return self.label
		
	def setStatus(self,s):
		self.status=s