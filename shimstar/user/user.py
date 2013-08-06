import xml.dom.minidom
from shimstar.user.character.character import *

class User:
	listOfUser={}
	instance=None
	def __init__(self,xmlPart,currentPlayer=False):
		self.listOfCharacter=[]
		self.login=""
		self.password=""
		self.id=0
		self.loadXmlPart(xmlPart)
		User.listOfUser[self.id]=self
		if currentPlayer==True:
			User.instance=self
		
	@staticmethod
	def getInstance():
		return User.instance
		
	
	def getCharacters(self):
		return self.listOfCharacter
		
	def getId(self):
		return self.id
		
	@staticmethod
	def getUserById(id):
		for usr in User.listOfUser:
			if User.listOfUser[usr].getId()==id:
				return User.listOfUser[usr]
		return None
		
	def chooseCharacter(self,id):
		for ch in self.listOfCharacter:
			if ch.getId()==id:
				ch.setCurrent(True)
			else:
				ch.setCurrent(False)
	
	def getCurrentCharacter(self):
		for ch in self.listOfCharacter:
			if ch.isCurrent()==True:
				return ch
				
		return None
	
	def getCharacterById(self,id):
		for ch in self.listOfCharacter:
			if ch.getId()==id:
				return ch
		return None
	
	def loadXmlPart(self,xmlPart):
		document = xml.dom.minidom.parseString(xmlPart)
		self.login=str(document.getElementsByTagName('name')[0].firstChild.data)
		self.id=int(document.getElementsByTagName('iduser')[0].firstChild.data)
		characters=document.getElementsByTagName('characters')
		for charact in characters:
			chs=charact.getElementsByTagName('character')
			for ch in chs:
				temp=Character(ch,self)
				self.listOfCharacter.append(temp)
		
		