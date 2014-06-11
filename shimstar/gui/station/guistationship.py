# -*- coding: utf-8 -*- 
import sys,os

import PyCEGUI
from shimstar.gui.shimcegui import *
from shimstar.user.user import *

class GuiFittingShip(DirectObject):
	instance=None
	def __init__(self):
		self.CEGUI=ShimCEGUI.getInstance()
		self.buttonSound= base.loader.loadSfx(shimConfig.getInstance().getConvRessourceDirectory() + "sounds/Button_press3.ogg")
		self.buttonSound2= base.loader.loadSfx(shimConfig.getInstance().getConvRessourceDirectory() + "sounds/Button_press1.ogg")
		
	@staticmethod
	def getInstance():
		if GuiFittingShip.instance==None:
			GuiFittingShip.instance=GuiFittingShip()
		return GuiFittingShip.instance
		
	