# -*- coding: utf-8 -*- 
import sys,os
from panda3d.rocket import *
from direct.directbase import DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task

from shimstar.gui.shimrocket import *
from shimstar.network.networkmainserver import *
from shimstar.network.message import *
from shimstar.game.gamestate import *
from shimstar.user.user import *
from shimstar.core.shimconfig import *

class menuchooseHeroRocket(DirectObject):
	def __init__(self):
		self.context = shimRocket.getInstance().getContext()

		self.back=self.context.LoadDocument('windows/background.rml')
		self.back.Show()
		self.doc = self.context.LoadDocument('windows/herochoice.rml')
		self.populateCharacters()
		
		self.doc.Show()
		self.accept("CLOSEF4",self.quit)
		self.doc2=self.context.LoadDocument("windows/herochoosen.rml")
		self.doc3=self.context.LoadDocument("windows/newhero.rml")
		self.doc4=self.context.LoadDocument("windows/herodelete.rml")
		taskMgr.add(self.event,"event reader menu connect",-40)  

	def quit(self,):
		GameState.getInstance().setState(C_QUIT)
		
	def populateCharacters(self):
		listOfChar=User.getInstance().getCharacters()
		content=self.doc.GetElementById("contentHero")
		
		listOfActualImg=content.GetElementsByTagName("div")
		for img in listOfActualImg:
			content.RemoveChild(img)
		i=0
		for ch in listOfChar:
			div=self.doc.CreateElement("div")
			div.SetAttribute("style","position:absolute;top:100px;left:" + str((50+i*150)) + "px;width:150px;")
			el=self.doc.CreateElement("img")
			face=ch.getFace()
			face=shimConfig.getInstance().getRessourceDirectory() + "images\\faces\\" + face + ".png"
			el.SetAttribute("src",str(face))
			el.SetAttribute("id",str(ch.getId()))
			div.AddEventListener("click","onHeroChoice(document," + str(ch.getId()) + ")")
		
			div.AppendChild(el)
			content.AppendChild(div)
			i+=1

	def event(self,arg):
		temp=NetworkMainServer.getInstance().getListOfMessageById(C_USER_ADD_CHAR)
		if(len(temp)>0):
				msg=temp[0]
				user.instance.addCharacterFromXml(msg.getMessage())
				self.populateCharacters()
				NetworkMainServer.getInstance().removeMessage(msg)
		temp=NetworkMainServer.getInstance().getListOfMessageById(C_USER_DELETE_CHAR)
		if(len(temp)>0):
				msg=temp[0]
				user.instance.deleteCharacter(int(msg.getMessage()))
				NetworkMainServer.getInstance().removeMessage(msg)
				self.populateCharacters()
		return Task.cont

	def destroy(self):
		self.context.UnloadDocument(self.back)
		self.context.UnloadDocument(self.doc)
		self.context.UnloadDocument(self.doc2)
		self.context.UnloadDocument(self.doc3)
		self.context.UnloadDocument(self.doc4)
		self.ignore("CLOSEF4")
		taskMgr.remove("event reader menu connect")
		

