from shimstar.core.decorators import *
import xml.dom.minidom
from shimstar.items.templates.itemtemplate import *
from shimstar.items.templates.weapontemplate import *
from shimstar.items.templates.enginetemplate import *
from shimstar.core.constantes import *

class ShimstarItem(object):
	def __init__(self,id=None,typeItem=0,xmlPart=None):
		self.container=0
		self.owner=0
		self.typeItem=typeItem
		self.name=""
		self.template=None
		self.idTemplate=0
		self.energy=0
		self.owner=0
		self.img=""
		self.cost=0
		self.sell=0
		self.location=0
		self.place=0
		self.space=0
		self.skillsItem={}
		self.id=id
		self.container=0
		self.typeContainer=""
		if xmlPart!=None:
			self.loadXml(xmlPart)
		else:
			print "///// " + str(self.template)
			if self.typeItem!=C_ITEM_WEAPON and self.typeItem!=C_ITEM_ENGINE:
			#~ if isinstance(self,Weapon)==False and isinstance(self,Engine)==False:
			#~ if True:
				self.template=ItemTemplate.getTemplate(id,self.typeItem)
				print "/////@@@ " + str(self.template)
				print self
				self.name,self.cost,self.sell,self.energyCost,self.space,self.img,self.location,self.typeItem=self.template.getInfos()		
			#~ print t
			#~ if isinstance(self.template,WeaponTemplate) or isinstance(self.template,EngineTemplate):
				#~ self.name,self.cost,self.sell,self.energyCost,self.space,self.img,self.location,self.typeItem=self.template.getInfos()		
			#~ else:
				#~ self.name,self.cost,self.sell,self.energyCost,self.space,self.img,self.location,self.typeItem=self.template.getInfos()		
				
		
	def loadXml(self,xmlPart):
		self.id=int(xmlPart.getElementsByTagName('iditem')[0].firstChild.data)
		self.idTemplate=int(xmlPart.getElementsByTagName('template')[0].firstChild.data)
		temp=ItemTemplate.getTemplate(self.idTemplate)
		self.name,self.cost,self.sell,self.energyCost,self.space,self.img,self.location,self.typeItem=temp.getInfos()		
		if len(xmlPart.getElementsByTagName('place'))>0:
			self.place=int(xmlPart.getElementsByTagName('place')[0].firstChild.data)
		if len(xmlPart.getElementsByTagName('location'))>0:
			self.location=int(xmlPart.getElementsByTagName('location')[0].firstChild.data)
		
	def getSkillsItem(self):
		return self.skillsItem
		
	def getTemplate(self):
		return self.idTemplate
		
	def getOwner(self):
		return self.owner
		
	def setContainer(self,id):
		self.container=id
		
	def getContainerType(self):
		return self.typeContainer
		
	def setContainerType(self,tc):
		self.typeContainer=tc
		
	def getContainer(self):
		return self.container
		
	def setOwner(self,id):
		self.owner=id
		
	def getId(self):
		return self.id
		
	def setId(self,id):
		self.id=id
		
	def getTypeItem(self):
		return self.typeItem
		
	def getSpace(self):
		return self.space
	
	def getLocation(self):
		return self.location
		
	def setPlace(self,place):
		self.place=place
		
	def setLocation(self,location):
		self.location=location
		
	def getName(self):
		return self.name
		
	def getImg(self):
		return self.img
		
	def getEnergyCost(self):
		return self.energy
		
	def getCost(self):
		return self.cost
		
	def getSell(self):
		return self.sell
	
