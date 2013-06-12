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

class menuconnectRocket(DirectObject):
	instance=None
	def __init__(self):
		menuconnectRocket.instance=self
		self.context = shimRocket.getInstance().getContext()

		self.back=self.context.LoadDocument('windows/background.rml')
		self.back.Show()
		self.doc = self.context.LoadDocument('windows/connect.rml')
		self.accept("CLOSEF4",self.quit)
		self.doc.Show()

		taskMgr.add(self.event,"event reader menu connect",-40)  
		
	@staticmethod
	def getInstance():
		if menuconnectRocket.instance==None:
			menuconnectRocket()
		return menuconnectRocket.instance

	def getWindow(self):
		return self.doc

	def quit(self,):
		GameState.getInstance().setState(C_QUIT)

	def destroy(self):
		self.context.UnloadDocument(self.back)
		self.context.UnloadDocument(self.doc)
		self.ignore("CLOSEF4")
		taskMgr.remove("event reader menu connect")
		
	def event(self,arg):
		temp=NetworkMainServer.getInstance().getListOfMessageById(C_NETWORK_CONNECT)
		#~ print temp
		if(len(temp)>0):
			for msg in temp:
				netMsg=msg.getMessage()
				state=int(netMsg[0])
				print state
				diag=self.doc.GetElementById("error")
				diag.SetAttribute("style","display:Block;")
				### Connexion accepted
				if state==0:
					diag.inner_rml="<span style='color:#00ff00;'>Connexion OK.</span>"
					fileHandle = open ("test.xml", 'w' ) 
					fileHandle.write(netMsg[1])
					fileHandle.close()
					User(netMsg[1])
					GameState.getInstance().setState(C_CHOOSE_HERO)
					usr=self.doc.GetElementById('name').value
					pwd=self.doc.GetElementById('pwd').value
					shimConfig.getInstance().setUser(usr)
					shimConfig.getInstance().setPwd(pwd)
					shimConfig.getInstance().saveConfig()
					return Task.done
				### Connexion refused
				else:
					if state==1:
						diag.inner_rml="<span style='color:#ff0000;'>Ce compte n'existe pas</span>"
					elif state==2:
						diag.inner_rml="<span style='color:#ff0000;'>Mauvais password</span>"
					elif state==3:
						diag.inner_rml="<span style='color:#ff0000;'>Compte deja en utilisation</span>"
					
				NetworkMainServer.getInstance().removeMessage(msg)
					
		return Task.cont