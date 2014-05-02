import xml.dom.minidom
import os, sys
from direct.showbase import Audio3DManager

class shimConfig:
	instance=None
	
	def __init__(self):
		self.ressourceDirectory=""
		self.convDirectory=""
		self.version=""
		self.user=""
		self.pwd=""
		self.ip=""
		self.loadXml()
		
	def loadXml(self):
		if os.path.isfile("config.xml")!=False:
			print "shimconfig::getcurrentPath " + str(os.getcwd())
			fileHandle = open ( "./config.xml", 'r' )
			fileHandle.close()
			dom = xml.dom.minidom.parse("./config.xml")
			#~ print "shimconfig::loadXml " + str(dom.toxml())
			#~ print "shimconfig::loadXml" + str(inspect.getfile(
			direc=dom.getElementsByTagName('directory')
			for d in direc:
				self.ressourceDirectory=str(d.firstChild.data)
			s="/" + self.ressourceDirectory[0:1] + self.ressourceDirectory[2:]
			s=s.replace("\\","/")
			self.convDirectory=s
			
			usr=dom.getElementsByTagName('user')
			for u in usr:
				if u.firstChild!=None:
					self.user=str(u.firstChild.data)
				
			ip=dom.getElementsByTagName('ip')
			for i in ip:
				if i.firstChild!=None:
					self.ip=str(i.firstChild.data)
				
			ver=dom.getElementsByTagName('version')
			for v in ver:
				if v.firstChild!=None:
					self.version=str(v.firstChild.data)
			
			pwd=dom.getElementsByTagName('password')
			for p in pwd:
				if p.firstChild!=None:
					self.pwd=str(p.firstChild.data)
				
	def getConvRessourceDirectory(self):
		return self.convDirectory
				
	def getRessourceDirectory(self):
		return self.ressourceDirectory
		
	def getAudio3DManager(self):
		return self.audio3Manager
		
	def getUser(self):
		return self.user
		
	def getPwd(self):
		return self.pwd
		
	def setUser(self,usr):
		self.user=usr
		
	def setPwd(self,pwd):
		self.pwd=pwd
		
	def getIp(self):
		return self.ip
		
	def saveConfig(self):
		docXml = xml.dom.minidom.Document()
		confXml=docXml.createElement("config")
		versionXml=docXml.createElement("version")
		dirXml=docXml.createElement("directory")
		userXml=docXml.createElement("user")
		passwordXml=docXml.createElement("password")
		ipXml=docXml.createElement("ip")
		versionXml.appendChild(docXml.createTextNode(str(self.version)))
		dirXml.appendChild(docXml.createTextNode(str(self.ressourceDirectory)))
		userXml.appendChild(docXml.createTextNode(str(self.user)))
		ipXml.appendChild(docXml.createTextNode(str(self.ip)))
		passwordXml.appendChild(docXml.createTextNode(str(self.pwd)))
		confXml.appendChild(passwordXml)
		confXml.appendChild(userXml)
		confXml.appendChild(versionXml)
		confXml.appendChild(dirXml)
		confXml.appendChild(ipXml)
		docXml.appendChild(confXml)
		fileHandle = open ( self.getRessourceDirectory() + "/config.xml", 'w' ) 
		fileHandle.write(docXml.toxml())
		fileHandle.close()
		
		
	@staticmethod
	def getInstance():
		if shimConfig.instance==None:
			shimConfig.instance=shimConfig()
		
		return shimConfig.instance