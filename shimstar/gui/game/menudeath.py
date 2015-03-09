import sys,os
from string import *
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.task import Task
from direct.distributed.PyDatagram import PyDatagram 
from direct.distributed.PyDatagramIterator import PyDatagramIterator 
from direct.gui.DirectFrame import DirectFrame
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from direct.showbase.ShowBase import ShowBase 
from shimstar.game.gamestate import *
from shimstar.user.user import *
import PyCEGUI
from shimstar.gui.shimcegui import * 

class MenuDeath(ShowBase):
	def __init__(self):
		self.focuson=0
		self.CEGUI=ShimCEGUI.getInstance()
		self.CEGUI.System.setDefaultFont("Brassiere-m")
		
		self.connectMenu = self.CEGUI.WindowManager.loadWindowLayout("death.layout")
		self.CEGUI.System.setGUISheet(self.connectMenu) 		
		customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImageset", "background/backmenuconnect.jpg", "images")
		self.CEGUI.WindowManager.getWindow("ConnexionBg").setProperty("BackgroundImage", "set:TempImageset image:full_image")
		
		self.btnQuit=self.CEGUI.WindowManager.getWindow("Root/group/quit")
		self.btnQuit.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'quit')
		self.btnQuit.setText("[colour='FFFF0000']En attente du serveur")
		self.btnQuit.disable()
		taskMgr.add(self.event,"waiting xml from server",-40)  
		GameState.getInstance().setState(C_DEATH_WAITING)
		self.accept("escape",self.quitGame)
		
		self.CEGUI.enable() 
		
	def event(self,arg):
		if(GameState.getInstance().getState()==C_DEATH_WAITING):
			#~ print "waiting"
			temp=NetworkMainServer.getInstance().getListOfMessageById(C_NETWORK_DEATH_CHAR_STEP2)
			if(len(temp)>0):
				msg=temp[0]
				netMsg=msg.getMessage()
				idShip=int(netMsg[0])
				idTemplateShip=int(netMsg[1])
				hullpoints=int(netMsg[2])
				#~ USer.getInstance().getCurrentCharacter().removeShip()
				User.getInstance().getCurrentCharacter().setShip(idShip,idTemplateShip,hullpoints)
				GameState.getInstance().setState(C_DEATH_WAITING_VALIDATION)
				self.btnQuit.enable()
				self.btnQuit.setText("[colour='FF00FF00']Entrer dans la station")
				NetworkMainServer.getInstance().removeMessage(msg)
				return Task.done
		return Task.cont
	
	def quitGame(self,):
		GameState.getInstance().setState(C_QUIT)
	
	def quit(self,windowEventArgs):
		#~ GameState.getInstance().setNewZone(User.getInstance().getCurrentCharacter().getLastStation())
		GameState.getInstance().setState(C_CHANGEZONE)
		
	def destroy(self):
		taskMgr.remove("waiting xml from server")
		self.CEGUI.WindowManager.destroyWindow(self.connectMenu)
	
    