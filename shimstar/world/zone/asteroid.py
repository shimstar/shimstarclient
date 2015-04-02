import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import CollisionTraverser,CollisionNode
import xml.dom.minidom
import os, sys

from shimstar.game.gamestate import *
from shimstar.world.zone.asteroidtemplate import *
from shimstar.core.shimconfig import *

class Asteroid(DirectObject):
	listOfAsteroid={}
	def __init__(self,xmlPart):
		self.pos=(0,0,0)
		self.hpr=(0,0,0)
		self.name=""
		self.id=0
		self.className="asteroid"
		self.scale=1
		self.node=None
		self.text=""
		self.wiredBox=None
		self.mass=0
		self.minerals={'id':0}
		self.loadXml(xmlPart)
		Asteroid.listOfAsteroid[self.id]=self
		
	@staticmethod
	def getAsteroidById(id):
		if Asteroid.listOfAsteroid.has_key(id)!=-1:
			return Asteroid.listOfAsteroid[id]
		return None
		
	def loadXml(self,xmlPart):
		self.id=int(xmlPart.getElementsByTagName('id')[0].firstChild.data)
		self.idTemplate=int(xmlPart.getElementsByTagName('idtemplate')[0].firstChild.data)
		posx=float(xmlPart.getElementsByTagName('posx')[0].firstChild.data)
		posy=float(xmlPart.getElementsByTagName('posy')[0].firstChild.data)
		posz=float(xmlPart.getElementsByTagName('posz')[0].firstChild.data)
		hprh=float(xmlPart.getElementsByTagName('hprh')[0].firstChild.data)
		hprr=float(xmlPart.getElementsByTagName('hprp')[0].firstChild.data)
		hprp=float(xmlPart.getElementsByTagName('hprr')[0].firstChild.data)
		templateAst=asteroidTemplate.getTemplate(self.idTemplate)
		self.pos=(posx,posy,posz)
		if templateAst!=None:
			self.name,self.egg,self.mass,self.text=templateAst.getInfos()
			self.node=loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() +self.egg)
			self.node.reparentTo(render)
			self.node.setName("asteroid_" + str(self.id))
			self.node.setPos(self.pos)
			self.node.setHpr(self.hpr)
			self.node.setTag("asteroid",str(self.id))
			self.name="asteroid" + str(self.id)
			self.node.setShaderAuto()
			self.node.setTag("name",self.name +" kk ")
			self.node.setTag("classname","asteroid")
			self.node.setTag("id",str(self.id))
			self.minerals=templateAst.getMinerals()
			
	def getMinerals(self):
		return self.minerals
		
	def collect(self,id,nb):
		if self.minerals.has_key(id):
			self.minerals[id]-=nb
	
	def getId(self):
		return self.id
		
	def getNode(self):
		return self.node
	
	def destroy(self):
		self.node.detachNode()
		self.node.removeNode()
		if Asteroid.listOfAsteroid.has_key(self.id)!=-1:
			del Asteroid.listOfAsteroid[self.id]
		
	def getPos(self):
		return self.node.getPos()

	def getObj(self):
		return self.node
		
	def getName(self):
		return self.name

	def getText(self):
		return self.text
		
