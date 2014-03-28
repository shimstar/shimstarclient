import xml.dom.minidom
from shimstar.user.character.character import *
from direct.stdpy import threading

class User(threading.Thread):
	listOfUser={}
	instance=None
	lock=threading.Lock()
	#~ def __init__(self,xmlPart,currentPlayer=False):
	def __init__(self,id,name,currentPlayer=False):
		threading.Thread.__init__(self)
		self.listOfCharacter=[]
		self.login=name
		self.password=""
		self.id=id
		#~ self.name=name
		#~ self.loadXmlPart(xmlPart)
		User.listOfUser[self.id]=self
		if currentPlayer==True:
			User.instance=self
	
	@staticmethod
	def getListOfCharacters(withoutCurrent=False):
		listOfChar=[]
		for uid in User.listOfUser:
			if withoutCurrent==True:
				if uid!=User.getInstance().getId():
					listOfChar.append(User.listOfUser[uid].getCurrentCharacter())
			else:
				listOfChar.append(User.listOfUser[uid].getCurrentCharacter())
		return listOfChar
		
	@staticmethod
	def getInstance():
		return User.instance
	
	def getCharacters(self):
		return self.listOfCharacter
		
	def getId(self):
		return self.id
		
	def deleteCharacter(self,idChar):
		chToDelete=None
		for c in self.listOfCharacter:
			if c.getId()==idChar:
				chToDelete=c
				break
		if chToDelete!=None:
			chToDelete.destroy()
			self.listOfCharacter.remove(chToDelete)
			
	def destroy(self):
		for c in self.listOfCharacter:
			c.destroy()
		del User.listOfUser[self.id]
		
	@staticmethod
	def getUserById(id):
		for usr in User.listOfUser:
			if User.listOfUser[usr].getId()==id:
				return User.listOfUser[usr]
		return None
		
	def chooseCharacter(self,id):
		print "usr::choosecharacter " + str(id)
		for ch in self.listOfCharacter:
			print "usr::choosecharacter ch = " + str(ch.getId())
			if ch.getId()==id:
				ch.setCurrent(True)
			else:
				ch.setCurrent(False)
	
	def getCurrentCharacter(self):
		for ch in self.listOfCharacter:
			if ch.isCurrent()==True:
				return ch
				
		return None
	
	def addCharacter(self,id,name,egg,idZone):
		print "user:addCharacter" + str(id) + "/" + str(name) + "/" + str(egg) + "/" + str(idZone)
		temp=Character(id,name,egg,idZone,self)
		self.listOfCharacter.append(temp)
		return temp
	
	def getCharacterById(self,id):
		for ch in self.listOfCharacter:
			if ch.getId()==id:
				return ch
		return None
		
	def addCharacterFromXml(self,xmlPart):
		document = xml.dom.minidom.parseString(xmlPart)
		temp=Character(document,self)
		self.listOfCharacter.append(temp)
	
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
		
		