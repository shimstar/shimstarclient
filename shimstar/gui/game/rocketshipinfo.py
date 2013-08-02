# -*- coding: utf-8 -*- 
import sys,os
from panda3d.rocket import *
from shimstar.gui.shimrocket import *
from shimstar.user.user import *
from shimstar.core.shimconfig import *
from shimstar.core.functions import *
from shimstar.gui.core.configuration import *


class rocketShipInfo():
	instance=None
	def __init__(self):
		rocketShipInfo.instance=self
		self.context = shimRocket.getInstance().getContext()
		self.window=None
		for l in self.context.documents:
			if l.title=="backgroundgame":
				self.window=l
		#~ self.window = self.context.LoadDocument('windows/infoshipgame.rml')
		self.obj=None
		self.hp=0
		
	@staticmethod
	def getInstance():
		if rocketShipInfo.instance==None:
			rocketShipInfo()
		return rocketShipInfo.instance
		
	def showWindow(self):
		if self.window!=None:
			self.window.Show()
		return self.window
		
	def render(self):
		if self.window!=None:
			ship=User.getInstance().getCurrentCharacter().ship
			hp=ship.getHullPoints()
			if self.hp!=hp:
				hpmax=ship.getMaxHullPoints()
				
				prcent=int(100*round(float(hp)/float(hpmax),1))
				img=self.window.GetElementById("lifeimg")
				img.SetAttribute("src",shimConfig.getInstance().getRessourceDirectory() + "images\\gui\\pgb" + str(prcent) + ".png")
				self.hp=hp
		
	def hideWindow(self):
		self.window.Hide()
		
	def destroy(self):
		self.context.UnloadDocument(self.window)
		