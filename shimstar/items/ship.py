import xml.dom.minidom
from math import sin, cos, pi
from math import sqrt

from pandac.PandaModules import *

from shimstar.items.slot import *
from shimstar.items.engine import *
from shimstar.items.weapon import *
from shimstar.items.item import *
from shimstar.items.itemfactory import *
from shimstar.user.user import *
from shimstar.core.shimconfig import *
from shimstar.items.templates.shiptemplate import *

DEG_TO_RAD = pi / 180

class Ship:
	#~ def __init__(self,id,xmlPart):
	def __init__(self,id,idTemplate):
		self.name = ""
		self.id=id
		self.template=idTemplate
		self.shipTemplate=None
		self.mainShip = False
		self.weapons=None
		self.engine = None
		self.actualSpeed = 0
		self.node = None
		self.img = ""
		self.owner=None  # owner obj (npc or character)
		self.group = 0
		self.mass = 0
		self.engineSound=None
		self.egg = ""
		self.lastMove=globalClock.getRealTime()
		self.hullpoints = 0
		self.maxhull = 0
		self.maxTorque = 30
		self.currentTorqueX = 0
		self.currentTorqueY = 0
		self.itemInInventory = []
		self.lastDiffQuat=Quat(0,0,0,0)
		self.oldQuat=Quat(0,0,0,0)
		self.pointerToGo = loader.loadModelCopy(shimConfig.getInstance().getConvRessourceDirectory() +  "models/arrow")
		self.pointerToGo.reparentTo(render)
		self.pointerToGo.hide()
		self.pointerToGoOld = loader.loadModelCopy(shimConfig.getInstance().getConvRessourceDirectory() + "models/arrow")
		self.pointerToGoOld.reparentTo(render)
		self.pointerToGoOld.hide()
		self.oldPos=(0,0,0)
		self.newPosition = False
		self.firstMove=False
		self.renderCounter = 0
		self.slots=[]
		self.itemInInventory= []
		self.pyr = {'p':0, 'y':0, 'r':0, 'a':0}
		self.loadTemplate()
		print "ship init" + str(self.id)
		
	def setOwner(self,owner):
		self.owner=owner
		
	def getOwner(self):
		return self.owner
		
	def setPosToGo(self, pos):
		self.pointerToGoOld.setPos(Vec3(self.pointerToGo.getPos()))
		self.pointerToGo.setPos(pos)
		self.newPosition = True
		self.renderCounter = 0
		
	def setHprToGo(self, hpr):
		self.pointerToGoOld.setQuat(Quat(self.pointerToGo.getQuat()))
		self.pointerToGo.setQuat(hpr)
		
	def getQuat(self):
		return self.node.getQuat()
		
	def move(self):
		dt=globalClock.getRealTime()-self.lastMove
		if dt>0.01:
			if True:
				if self.firstMove==True:
					self.node.setPos(self.pointerToGo.getPos())
					self.node.setQuat(self.pointerToGo.getQuat())
					self.pointerToGoOld.setPos(self.pointerToGo.getPos())
					self.pointerToGoOld.setQuat(self.pointerToGo.getQuat())
					self.firstMove=False
				else:
					self.renderCounter += 1
					lastPosServer = self.pointerToGo.getPos()
					oldPosServer = self.pointerToGoOld.getPos()
					targetPos = lastPosServer + (lastPosServer - oldPosServer) * self.renderCounter * 1 / C_SENDTICKS * dt
					currentPos = self.node.getPos()
					ratioPos = currentPos * 0.95 + targetPos * 0.05                               # ensure pseudo-continuous position
					oldLinearVel = currentPos - self.oldPos
					newLinearVel = oldLinearVel * 0.9 + (ratioPos - currentPos) * 0.1             # ensure pseudo-continuous linear velocity
					
					self.node.setPos(currentPos + newLinearVel)
					self.oldPos = Vec3(currentPos)
					
					lastQuatServer = self.pointerToGo.getQuat()
					oldQuatServer = self.pointerToGoOld.getQuat()
					diffQuat=Quat(lastQuatServer - oldQuatServer) 

					if diffQuat.getR()>0.6 or diffQuat.getR()<-0.6 or diffQuat.getI()>0.6 or diffQuat.getI()<-0.6 or diffQuat.getJ()>0.6 or diffQuat.getJ()<-0.6 or diffQuat.getK()>0.6 or diffQuat.getK()<-0.6:
						lastQuatServer.setR(-lastQuatServer.getR())
						lastQuatServer.setI(-lastQuatServer.getI())
						lastQuatServer.setJ(-lastQuatServer.getJ())
						lastQuatServer.setK(-lastQuatServer.getK())
						
						self.pointerToGo.setQuat(lastQuatServer)
					
					diffQuat=Quat(lastQuatServer - oldQuatServer) 
					self.lastDiffQuat=diffQuat
					#~ if self.id==417:
						#~ print "########################"
						#~ print "ship::move " + str(self.node.getPos() ) + " / " + str(self.pointerToGo.getPos())
						#~ print "ship::move " + str(self.node.getQuat() ) + " / " + str(self.pointerToGo.getQuat())
						#~ print "##############################"
						#~ print "ship::move diffQuat " + str(diffQuat) + " / " + str(lastQuatServer) + "/" + str(oldQuatServer) + "/" + str(self.id) + "/" + str(oldQuatServer.getK()) + "/" + str(round(oldQuatServer.getK(),5))
						
					targetQuat = lastQuatServer + (lastQuatServer - oldQuatServer) * self.renderCounter * 1 / C_SENDTICKS * dt
					targetQuat.normalize()
					currentQuat = self.node.getQuat()
					ratioQuat = currentQuat * 0.9 + targetQuat * 0.1                            # ensure pseudo-continuous rotation
					oldAngularVel = currentQuat - self.oldQuat
					
					newAngularVel = oldAngularVel * 0.925 + (ratioQuat - currentQuat) * 0.025         # ensure pseudo-continuous angular velocity
					
					finalQuat = currentQuat + newAngularVel
					finalQuat.normalize()
					self.oldQuat = Quat(currentQuat)
				
					self.node.setQuat(finalQuat)
					#~ if self.id==417:
						
						#~ print "ship::move " + self.node.getQuat()
			
						
				#~ self.node.setPos(self.pointerToGo.getPos())
			self.lastMove=globalClock.getRealTime()
		
	def loadTemplate(self):
		self.shipTemplate=ShipTemplate.getTemplate(self.template)
		self.name,self.maxhull,self.egg,self.img,self.slots=self.shipTemplate.getInfos()
		for tempSlot in self.slots:
			if tempSlot.getItem()!=None:
				it=tempSlot.getItem()
				if it.getTypeItem()==C_ITEM_WEAPON:
					self.weapons=it
					it.setShip(self)
				if it.getTypeItem()==C_ITEM_ENGINE:
					self.engine=it
		#~ self.name=str(xmlPart.getElementsByTagName('name')[0].firstChild.data)
		#~ self.id=int(xmlPart.getElementsByTagName('idship')[0].firstChild.data)
		#~ self.hullpoints=int(xmlPart.getElementsByTagName('hullpoints')[0].firstChild.data)
		#~ self.maxhull=int(xmlPart.getElementsByTagName('maxhullpoints')[0].firstChild.data)
		#~ self.egg=str(xmlPart.getElementsByTagName('egg')[0].firstChild.data)
		#~ self.img=str(xmlPart.getElementsByTagName('img')[0].firstChild.data)
		#~ slotss=xmlPart.getElementsByTagName('slot')
		#~ for s in slotss:
			#~ tempSlot=Slot(s)
			#~ self.slots.append(tempSlot)
			#~ if tempSlot.getItem()!=None:
				#~ it=tempSlot.getItem()
				#~ if it.getTypeItem()==C_ITEM_WEAPON:
					#~ self.weapons=it
					#~ it.setShip(self)
				#~ if it.getTypeItem()==C_ITEM_ENGINE:
					#~ self.engine=it
		#~ inventory=xmlPart.getElementsByTagName('inventory')
		#~ for inv in inventory:
			#~ items=inv.getElementsByTagName('item')
			#~ for itXml in items:
				#~ typeItem=int(itXml.getElementsByTagName('typeitem')[0].firstChild.data)
				#~ idItem=int(itXml.getElementsByTagName('iditem')[0].firstChild.data)
				#~ item=itemFactory.getItemFromXml(itXml,typeItem)
				#~ self.itemInInventory.append(item)
		self.node = loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() + self.egg)
		self.node.reparentTo(render)
		self.node.setName(self.name)
		
	def getId(self):
		return self.id
		
	def getItemInInventory(self):
		return self.itemInInventory
		
	def addItemInInventory(self, item):
		self.itemInInventory.append(item)
		
	def removeItemInInventory(self, idItem):
		itFound=None
		for it in self.itemInInventory:
			if it.getId()==idItem:
				itFound=it
				break
		if itFound!=None:
			self.itemInInventory.remove(itFound)
		
	def getFirstPlaceFreeInInventory(self):
		"""
			return the first place free in the inventory. The item have each a number allowing to locate it when the inventory is shown.
			This function returns first place not allocated.
		"""
		places=[]
		max=0
		for i in self.itemInInventory:
			places.append(i.getLocation())
			if max<i.getLocation():
				max=i.getLocation()
		places.sort()
		returnValue=-1
		val=0
		for p in places:
			if (val)!=int(p):
				if(val)<int(p):
					returnValue=val
				else:
					returnValue=int(p)
				break
			val+=1
			
		if returnValue==-1:
			returnValue=max+1
		return returnValue

	def uninstallItemBySlotId(self, slotId):
		for s in self.slots:
			if s.getId()==int(slotId):
				self.uninstallItem(s)
				break

	def getItemInstalledByCategory(self, cat):
		items = []
		for it in self.items:
			if it.getTypeItem() == cat:
				items.append(it)
		return items

	def uninstallItem(self,slot):
		self.itemInInventory.append(slot.getItem())
		slot.setItem(None)
		network.reference.sendMessage(C_CHAR_UPDATE, str(self.character.getUserId()) + "/" + str(self.character.getId()) + "/uninstall=" + str(slot.getId()))

	def installItem(self, item,slot):
		slotToInstall=None
		for s in self.slots:
			if s.getId()==int(slot):
				slotToInstall=s
				break
		if slotToInstall!=None:
			if slotToInstall.getItem()!=None:
				self.uninstallItem(slotToInstall)
			
			itemToInstall=None
			for i in self.itemInInventory:
				if i.getId()==int(item):
					itemToInstall=i
					break
			if itemToInstall!=None:				
				slotToInstall.setItem(itemToInstall)
				network.reference.sendMessage(C_CHAR_UPDATE, str(self.character.getUserId()) + "/" + str(self.character.getId()) + "/install=" + str(itemToInstall.getId()) + "#" + str(slotToInstall.getId()))
				self.itemInInventory.remove(itemToInstall)
						
	def addMinerals(self, id,typeMineral, qt):
		alreadyGot = False
		for i in self.itemInInventory:
			if i.getTypeItem() == C_ITEM_MINERAL:
				if i.getId() == id:
					i.addMineral(qt)
					alreadyGot = True
					break
					
		if alreadyGot == False:
			newItem = mineral(typeMineral)
			newItem.addMineral(qt)
			newItem.setId(id)
			self.itemInInventory.append(newItem)
			
	def removeMinerals(self, id, qt):
		for i in self.itemInInventory:
			if i.getTypeItem() == C_ITEM_MINERAL:
				if i.getId() == id:
					i.removeMineral(qt)
					break
					
	def getSlots(self):
		return self.slots

	def getWeapon(self):
		return self.weapons

	def changeZone(self):
		self.actualSpeed = 0

	def getPos(self):
		return self.node.getPos()
		
	def setPos(self,pos):
		self.node.setPos(pos)
		
	def setQuat(self,quat):
		self.node.setQuat(quat)
		
	def getNode(self):
		return self.node
		
	def getName(self):
		return self.name
		
	def getImg(self):
		return self.img
		
	def setVisible(self):
		self.node.show()
		
	def setInvisible(self):
		self.node.hide()
		
	def isHidden(self):
		return self.node.isHidden()
				
	def getSpeed(self):
		return self.actualSpeed
		
	def getSpeedMax(self):
		return self.engine.getSpeedMax()
			
	def addBullet(self,bulId,pos,quat):
		self.weapons.addBullet(bulId,pos,quat)
			
	def shot(self):
		if self.weapons!=None:
			return self.weapons.shot( self.node.getPos(), self.node.getQuat())
		return None

	def destroy(self):
		self.node.detachNode()
		self.node.removeNode()		
				
	def getPrcentHull(self):
		prcent = float(self.hullpoints) / float(self.maxhull) 
		return float(prcent),self.hullpoints,self.maxhull
				
	def getMaxHullPoints(self):
		return self.maxhull
				
	## Return True if ship has hull>0
	## Return False if shup has hull<=0
	def takeDamage(self, hitpoints):
		#~ audio3d = shimConfig.getInstance().getAudio3DManager()
		#~ exploSound= audio3d.loadSfx(shimConfig.getInstance().getConvRessourceDirectory() + "sounds/enemy_explosion1.ogg")
		#~ audio3d.setSoundVelocityAuto( exploSound) 
		#~ audio3d.setListenerVelocityAuto() 
		#~ audio3d.attachSoundToObject(exploSound, self.node)
		#~ exploSound.setLoop(False)
		#~ exploSound.play()
		#~ audio3d.setDropOffFactor(0.1) 
		#~ self.explodeSound.append(exploSound)
		self.hullpoints -= hitpoints
		if self.hullpoints <= 0:
			#~ self.setVisible(False)
			return False
		return True
		
	def getHullPoints(self):
		return self.hullpoints
		
		