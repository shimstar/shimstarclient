# -*- coding: utf-8 -*- 
import sys,os

import PyCEGUI
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from pandac.PandaModules import * 
from shimstar.gui.shimcegui import * 
from shimstar.core.shimconfig import *
from shimstar.user.user import *
from shimstar.world.zone.zone import *
from shimstar.game.gamestate import *

class GuiStation(DirectObject):
	def __init__(self):
		idZone=User.getInstance().getCurrentCharacter().getIdZone()
		self.zone=Zone(idZone)
		self.listOfImageSet={}
		self.CEGUI=ShimCEGUI.getInstance()
		self.name=""
		self.back=self.zone.getEgg()
		self.setupUI()
		taskMgr.add(self.event,"event reader",-40)  
		self.accept("escape",self.quitGame,)
		self.CEGUI.enable() 
		GameState.getInstance().setState(C_PLAYING)
		
	def event(self,arg):
		return Task.cont
		
	def quitGame(self,):
		self.InQuitAnimationInstance.start()
		self.CEGUI.WindowManager.getWindow("root/Quit").moveToFront()
		
	def onCancelQuitGame(self,args):
		self.OutQuitAnimationInstance.start()
		
	def onQuiGameConfirmed(self,args):
		GameState.getInstance().setState(C_QUIT)
		
	def ButtonClicked(self,windowEventArgs):
		if (windowEventArgs.window.getName() == "Station/Menus/Sortir"):
			print "guistation::buttonclicked :: sortir de la station"
			GameState.getInstance().setNewZone(self.zone.getExitZone())
			#~ GameState.getInstance().setState(C_CHANGEZONE)
			User.getInstance().getCurrentCharacter().changeZone()

	def destroy(self):
		self.ignore("escape")
		taskMgr.remove("event reader")
		self.CEGUI.WindowManager.destroyWindow(self.root)
		
	def setupUI(self):
		#  Chargement des sch?s
		self.CEGUI.SchemeManager.create("TaharezLook.scheme") 
		self.CEGUI.SchemeManager.create("shimstar.scheme") 

		self.CEGUI.System.setDefaultMouseCursor("ShimstarImageset", "MouseArrow") 
		self.CEGUI.System.setDefaultFont("Brassiere-m")
		self.root = self.CEGUI.WindowManager.loadWindowLayout("ingame.layout") 
		customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImagesetBckStation", "background/" + self.back  , "images")
		self.CEGUI.WindowManager.getWindow("Station/Background").setProperty("BackgroundImage", "set:TempImagesetBckStation image:full_image")
		self.CEGUI.WindowManager.getWindow("HUD/Cockpit").hide()
		self.CEGUI.WindowManager.getWindow("Station").show()
		self.CEGUI.WindowManager.getWindow("Station/Name").setText(self.name)
		self.CEGUI.System.setGUISheet(self.root) 
		self.CEGUI.WindowManager.getWindow("Station/Menus/Sortir").subscribeEvent(PyCEGUI.PushButton.EventClicked,self,'ButtonClicked')
		
		self.CEGUI.WindowManager.getWindow("root/Quit/CancelQuit").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'onCancelQuitGame')
		self.CEGUI.WindowManager.getWindow("root/Quit/Quit").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'onQuiGameConfirmed')
		self.OutQuitAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
		self.InQuitAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
		self.OutQuitAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("root/Quit"))
		self.InQuitAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("root/Quit"))
	
	