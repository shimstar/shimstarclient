### TODO

# -*- coding: utf-8 -*- 
import sys,os
from panda3d.rocket import *
from direct.directbase import DirectStart
from direct.task import Task
from direct.showbase.DirectObject import DirectObject

from shimstar.gui.shimrocket import *
from shimstar.game.gamestate import *
from shimstar.core.shimconfig import *
from shimstar.core.constantes import *
from shimstar.network.networkmainserver import *
from shimstar.user.user import *
from shimstar.world.zone.zone import *

class menuLoadZoneRocket(DirectObject):
	instance=None
	def __init__(self):
		menuLoadZoneRocket.instance=self
		self.context = shimRocket.getInstance().getContext()

		self.back=self.context.LoadDocument('windows/backgroundloadzone.rml')
		self.back.Show()
	
		self.accept("CLOSEF4",self.quit)

		taskMgr.add(self.event,"event reader menu loadzone",-40)  
		
	@staticmethod
	def getInstance():
		if menuLoadZoneRocket.instance==None:
			menuLoadZoneRocket()
		return menuLoadZoneRocket.instance

	def getWindow(self):
		return self.doc

	def quit(self,):
		GameState.getInstance().setState(C_QUIT)

	def destroy(self):
		self.context.UnloadDocument(self.back)
		self.ignore("CLOSEF4")
		taskMgr.remove("event reader menu loadzone")
		
	def event(self,arg):
		if GameState.getInstance().getState()==C_WAITING_LOADINGZONE:
			Zone(User.instance.getCurrentCharacter().getIdZone())
			Zone.getInstance().start()
			self.back.GetElementById("btnzone").inner_rml="<span style='color:#00ff00;'>Chargement de la zone</span>"
			self.back.GetElementById("btnnpc").inner_rml="<span style='color:#0000ff;'>Chargement des ennemis</span>"
			self.back.GetElementById("npc").SetAttribute("style","position:absolute; top:130px; left:750px;width:250px;tab-index:none;Display:Block;")
			GameState.getInstance().setState(C_WAITING_ASKING_INFO_NPC)
			msg=netMessage(C_NETWORK_ASKING_NPC)
			msg.addInt(User.getInstance().getId())
			NetworkZoneServer.getInstance().sendMessage(msg)
		elif GameState.getInstance().getState()==C_NETWORK_NPC_SENT:
			self.back.GetElementById("btnnpc").inner_rml="<span style='color:#00ff00;'>Chargement des ennemis</span>"
			self.back.GetElementById("btnjoueur").inner_rml="<span style='color:#0000ff;'>Chargement des Joueurs</span>"
			self.back.GetElementById("joueur").SetAttribute("style","position:absolute; top:350px; left:250px;width:250px;tab-index:none;Display:Block;")
			msg=netMessage(C_NETWORK_ASKING_CHAR)
			msg.addInt(User.getInstance().getId())
			NetworkZoneServer.getInstance().sendMessage(msg)
			GameState.getInstance().setState(C_WAITING_ASKING_INFO_CHARACTER)
		elif GameState.getInstance().getState()==C_WAITING_CHARACTER_RECEIVED:	
			self.back.GetElementById("btnjoueur").inner_rml="<span style='color:#00ff00;'>Chargement des Joueurs</span>"
			self.back.GetElementById("play").SetAttribute("style","position:absolute; top:250px; left:500px;tab-index:none;Display:Block;")
		return Task.cont