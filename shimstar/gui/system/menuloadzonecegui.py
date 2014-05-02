# -*- coding: utf-8 -*- 
import sys,os
from string import *
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.distributed.PyDatagram import PyDatagram 
from direct.distributed.PyDatagramIterator import PyDatagramIterator 
from direct.gui.DirectFrame import DirectFrame
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from direct.task import Task
from direct.showbase.ShowBase import ShowBase 
from shimstar.network.networkmainserver import *
import PyCEGUI
from shimstar.gui.shimcegui import * 
from shimstar.game.gamestate import *
from shimstar.user.user import *
from shimstar.network.netmessage import *
from shimstar.core.shimconfig import *
from shimstar.world.zone.zone import *

C_MENUCONNECT_WAITING=1

def setText(textEntered):
	textObject.setText(textEntered)

class MenuLoadZoneCegui(ShowBase):
	def __init__(self):
		self.focuson=0
		self.CEGUI=ShimCEGUI.getInstance()
		self.setupUI()
		self.labelZone=self.CEGUI.WindowManager.getWindow("LabelStatusZone")
		self.labelNpc=self.CEGUI.WindowManager.getWindow("LabelStatusEnnemis")

		self.labelPlayers=self.CEGUI.WindowManager.getWindow("LabelStatusPlayer")
		self.btnPlay=self.CEGUI.WindowManager.getWindow("Jouer")
		
		taskMgr.add(self.event,"event reader menu loadzone",-40)  
		self.stateConnexion=0
		self.btnPlay.setText("[colour='FFFF0000']Chargement...")
		self.btnPlay.disable()
		self.accept("escape",self.quitGame)
		
		self.CEGUI.enable() 
		
	def setupUI(self):
		#  Chargement des sch?s
		self.CEGUI.SchemeManager.create("TaharezLook.scheme") 
		self.CEGUI.SchemeManager.create("shimstar.scheme") 
		self.CEGUI.System.setDefaultMouseCursor("ShimstarImageset", "MouseArrow") 
		self.CEGUI.System.setDefaultFont("Brassiere-m")
		self.root = self.CEGUI.WindowManager.loadWindowLayout("loadzone.layout") 
		#~ self.CEGUI.ImageSetManager.createFromImageFile("MenuConnect/Background", "backmenuconnect.jpg", "imagesets")
		customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImageset", "background/backmenuconnect.jpg", "images")
		self.CEGUI.WindowManager.getWindow("background").setProperty("BackgroundImage", "set:TempImageset image:full_image")
		self.CEGUI.System.setGUISheet(self.root) 
		#  Ev?ments
		self.CEGUI.WindowManager.getWindow("Jouer").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'play')
	
		# ------------
		#  Animations
		# ------------
		#  Chargement du XML
		#~ self.CEGUI.AnimationManager.loadAnimationsFromXML("shimstar.anim.xml", "animations")
		
		#  Cr?ion des instances
		self.InZoneAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
		self.InNPCAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
		self.InPlayerAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
		self.InPlayAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
		
		#  Affectation des instances ?eurs fen?es respectives
		self.InZoneAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("LabelStatusZone"))
		self.InNPCAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("LabelStatusEnnemis"))
		self.InPlayerAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("LabelStatusPlayer"))
		#~ self.InPlayAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Jouer"))
		
		
	def quitGame(self,):
		GameState.getInstance().setState(C_QUIT)

	def event(self,arg):
		if GameState.getInstance().getState()==C_WAITING_LOADINGZONE:
			self.InZoneAnimationInstance.start()
			Zone(User.instance.getCurrentCharacter().getIdZone())
			Zone.getInstance().start()
			GameState.getInstance().setState(C_WAITING_ASKING_INFO_NPC)
			msg=netMessage(C_NETWORK_ASKING_NPC)
			msg.addUInt(User.getInstance().getId())
			NetworkZoneServer.getInstance().sendMessage(msg)
			self.InNPCAnimationInstance.start()
			self.labelZone.setText("[colour='FF00FF00']OK")
		elif GameState.getInstance().getState()==C_NETWORK_NPC_SENT:
			msg=netMessage(C_NETWORK_ASKING_CHAR)
			msg.addUInt(User.getInstance().getId())
			NetworkZoneServer.getInstance().sendMessage(msg)
			GameState.getInstance().setState(C_WAITING_ASKING_INFO_CHARACTER)
			self.InPlayerAnimationInstance.start()
			self.labelNpc.setText("[colour='FF00FF00']OK")
		elif GameState.getInstance().getState()==C_WAITING_CHARACTER_RECEIVED:	
			self.labelPlayers.setText("[colour='FF00FF00']OK")
			self.btnPlay.setText("[colour='FF00FF00']Jouer")
			self.btnPlay.enable()
		return Task.cont
		

		
	def play(self,windowEventArgs):
		GameState.getInstance().setState(C_GOPLAY)
			
	def destroy(self):
		taskMgr.remove("event reader menu loadzone")
		self.CEGUI.WindowManager.destroyWindow(self.root)
		self.ignore("enter")
		self.ignore("escape")
	
    