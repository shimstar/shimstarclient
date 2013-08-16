### TODO

# -*- coding:cp1252 -*-
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

class MenuCreateAccountRocket(DirectObject):
	instance=None
	def __init__(self):
		MenuCreateAccountRocket.instance=self
		self.context = shimRocket.getInstance().getContext()

		self.back=self.context.LoadDocument('windows/background.rml')
		self.back.Show()
		self.doc = self.context.LoadDocument('windows/newaccount.rml')
		self.accept("CLOSEF4",self.quit)
		self.doc.Show()

		taskMgr.add(self.event,"event reader menu create account",-40)  
		
	@staticmethod
	def getInstance():
		if MenuCreateAccountRocket.instance==None:
			MenuCreateAccountRocket()
		return MenuCreateAccountRocket.instance

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
		temp=NetworkMainServer.getInstance().getListOfMessageById(C_CREATE_USER)
		if(len(temp)>0):
			for msg in temp:
				netMsg=msg.getMessage()
				state=int(netMsg[0])
				diag=self.doc.GetElementById("errorcreate")
				diag.SetAttribute("style","display:Block;")

				if state==1:
					diag.inner_rml="<span style='color:#ff0000;'>Compte cree</span>"
					GameState().setState(C_INIT)
					return Task.done
				else:
					diag.inner_rml="<span style='color:#ff0000;'>Ce compte existe deja</span>"
				NetworkMainServer.getInstance().removeMessage(msg)
					
		return Task.cont