# -*- coding: utf-8 -*- 
import sys,os

import PyCEGUI
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from shimstar.gui.shimcegui import * 
from shimstar.core.shimconfig import *
from shimstar.user.user import *

class menuItemInfo(DirectObject):
	instance=None
	def __init__(self):
		self.CEGUI=ShimCEGUI.getInstance()
		self.obj=None
		self.OutMenuInfoAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("FadeOut")
		self.InMenuInfoAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("FadeIn")
		self.OutMenuInfoAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("InfoItem"))
		self.InMenuInfoAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("InfoItem"))
		self.startTicks=0
		taskMgr.add(self.event,"event hide item",-40)  

	def event(self,task):
		dt= globalClock.getRealTime()-self.startTicks
		if self.CEGUI.WindowManager.getWindow("InfoItem").isVisible():
			if dt>2:
				self.CEGUI.WindowManager.getWindow("InfoItem").hide()
		return task.cont
		
	def hideField(self):
		self.CEGUI.WindowManager.getWindow("InfoItem/Info1").hide()
		self.CEGUI.WindowManager.getWindow("InfoItem/Info2").hide()
		
	@staticmethod
	def getInstance():
		if menuItemInfo.instance==None:
			menuItemInfo.instance=menuItemInfo()
		return menuItemInfo.instance
		
	def setObj(self,obj):
		self.obj=obj
		self.hideField()
		self.startTicks=globalClock.getRealTime()
		self.showCommons()
		if obj.getTypeItem()==C_ITEM_ENERGY:
			self.showEnergy()
		elif obj.getTypeItem()==C_ITEM_WEAPON:
			self.showWeapon()
		elif obj.getTypeItem()==C_ITEM_ENGINE:
			self.showEngine()
		elif obj.getTypeItem()==C_ITEM_CONTAINER:
			self.showContainer()
		#~ self.CEGUI.WindowManager.getWindow("InfoItem").show()
		self.InMenuInfoAnimationInstance.start()
		self.CEGUI.WindowManager.getWindow("InfoItem").moveToFront()
			
	def showWeapon(self):
		self.CEGUI.WindowManager.getWindow("InfoItem/Info1").setText("Degats : " + str(self.obj.getDamage()))
		self.CEGUI.WindowManager.getWindow("InfoItem/Info2").setText("Frequence de tir : " + str(self.obj.getFrequency()) + " tir / sec")
		self.CEGUI.WindowManager.getWindow("InfoItem/Info1").show()
		self.CEGUI.WindowManager.getWindow("InfoItem/Info2").show()
		self.CEGUI.WindowManager.getWindow("InfoItem/Type").setText("Type : Arme" )

	def showContainer(self):
		self.CEGUI.WindowManager.getWindow("InfoItem/Type").setText("Type : Container" )
		self.CEGUI.WindowManager.getWindow("InfoItem/Encombrement").setText("Espace supplémentaire : " + str(self.obj.getSpace() ))

	def showEngine(self):
		self.CEGUI.WindowManager.getWindow("InfoItem/Type").setText("Type : Moteur" )
	
	def showEnergy(self):
		self.CEGUI.WindowManager.getWindow("InfoItem/Type").setText("Type : Generateur" )
		self.CEGUI.WindowManager.getWindow("InfoItem/Energie").setText("Energie produite : " + str(self.obj.getEnergy()))

	def showCommons(self):
		self.CEGUI.WindowManager.getWindow("InfoItem/Name").setText("Nom : " + self.obj.getName())
		self.CEGUI.WindowManager.getWindow("InfoItem/Energie").setText("Energie : " + str(self.obj.getEnergyCost() ))
		self.CEGUI.WindowManager.getWindow("InfoItem/Encombrement").setText("Encombrement : " + str(self.obj.getSpace() ))
		
	def hide(self):
		if globalClock.getRealTime()-self.startTicks>0.5:
			self.CEGUI.WindowManager.getWindow("InfoItem").hide()
			#~ self.OutMenuInfoAnimationInstance.start()
		
	
		