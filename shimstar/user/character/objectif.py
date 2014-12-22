from shimstar.core.decorators import *

class Objectif:
	def __init__(self,id,idtype,text,iditem,tableitem,zone,nbitem):
		self.id=id
		self.idType=idtype
		self.text=text
		self.idItem=iditem
		self.tableItem=tableitem
		self.zone=zone
		self.nbItem=nbitem
		self.nbItemCharacter=0
		self.status=False
		
	def setNbItemCharacter(self,nb):
		self.nbItemCharacter=nb
		
	def getNbItemCharacter(self):
		return self.nbItemCharacter
		
	def getId(self):
		return self.id
		
	def getIdType(self):
		return self.idType
		
	def getText(self):
		return self.text
		
	def getIdItem(self):
		return self.idItem
		
	def getTableItem(self):
		return self.tableItem
		
	def getZone(self):
		return self.zone
		
	def getNbItem(self):
		return self.nbItem
		
	def getStatus(self):
		return self.status
		
	def setStatus(self,status):
		self.status=status
	