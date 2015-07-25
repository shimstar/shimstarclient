import os, sys

from shimstar.core.constantes import *
from shimstar.items.templates.weapontemplate import *
from shimstar.items.item import *
from shimstar.items.bullet import *

class Weapon(ShimstarItem):
	def __init__(self,templateId=None,xmlPart=None):
		#~ print "Weapon::init " + str(xmlPart.toxml())
		self.typeItem=C_ITEM_WEAPON
		super(Weapon,self).__init__(templateId,C_ITEM_WEAPON,xmlPart)	
		
		self.range=0
		self.damage=0
		self.bullets=[]
		self.cadence=0
		self.lastShot=0
		self.speed=0
		self.ship=None
		self.bulletSound=""
		self.lastShot=0
		self.idTemplate=templateId
		

		if xmlPart!=None:
			self.loadXml(xmlPart)
		else:
			self.template=WeaponTemplate.getTemplate(templateId)
			self.name,self.egg,self.damage,self.range,self.cadence,self.speed,self.sell,self.energyCost,self.space,self.img,self.cost,self.bulletSound,self.skillsItem=self.template.getInfos()
		
	def loadXml(self,xmlPart):
		self.id=int(xmlPart.getElementsByTagName('iditem')[0].firstChild.data)
		self.idTemplate=int(xmlPart.getElementsByTagName('template')[0].firstChild.data)
		temp=WeaponTemplate.getTemplate(self.idTemplate)
		self.name,self.egg,self.damage,self.range,self.cadence,self.speed,self.sell,self.energyCost,self.space,self.img,self.cost,self.bulletSound,self.skillsItem=temp.getInfos()
		if len(xmlPart.getElementsByTagName('place'))>0:
			self.place=int(xmlPart.getElementsByTagName('place')[0].firstChild.data)
		if len(xmlPart.getElementsByTagName('location'))>0:
			self.location=int(xmlPart.getElementsByTagName('location')[0].firstChild.data)
			
	def setShip(self,ship):
		self.ship=ship
		
	def getShip(self):
		return self.ship
			
	def getDamage(self):
		return self.damage
		
	def getFrequency(self):
		return self.cadence
	
	def getRange(self):
		return self.range
	
	def getSpeed(self):
		return self.speed
		
	def shot(self,pos,quat):
		if globalClock.getRealTime()-self.lastShot>self.cadence:
			self.lastShot=globalClock.getRealTime()
			return True
		return False
		
	def addBullet(self,bulId,pos,quat):
		b=Bullet(bulId,pos,quat,self.egg,self.range,self.speed,self,self.bulletSound)
		