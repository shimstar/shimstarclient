import sys,os
from string import *
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.task import Task
from direct.showbase.ShowBase import ShowBase 
from shimstar.user.user import *
import PyCEGUI
from shimstar.gui.shimcegui import * 

C_MENU_TUTO_SPACE = 5

class MenuTuto():
	instance=None
	def __init__(self):
		self.focuson=0
		#~ self.CEGUI=ShimCEGUI.getInstance()
		#~ self.CEGUI.System.setDefaultFont("Brassiere-m")
		
		#~ self.tutoMenu = self.CEGUI.WindowManager.loadWindowLayout("tuto.layout")
		#~ self.CEGUI.System.setGUISheet(self.tutoMenu) 		
		
		#~ self.CEGUI.enable() 
		self.CEGUI=None
		self.tuto={}
		self.activ=False
		self.tutoRead={}
		self.loadXml()

		
	def loadXml(self):
		dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() +"config\\tutos.xml")
		tutos=dom.getElementsByTagName('tuto')
		for t in tutos:
			id=int(t.getElementsByTagName('id')[0].firstChild.data)
			message=str(t.getElementsByTagName('msg')[0].firstChild.data)
			self.tuto[id]=message
	
	@staticmethod
	def getInstance():
		if MenuTuto.instance==None:
			MenuTuto.instance=MenuTuto()
		return MenuTuto.instance
		
	def setCeguiManager(self,cg):
		self.CEGUI=cg
		self.CEGUI.WindowManager.getWindow("root/tuto").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,self,'closeClicked')
		
	def closeClicked(self,args):
		self.CEGUI.WindowManager.getWindow("root/tuto").hide()
		self.activ=False
		
	def displayTuto(self,id):
		tutoMenu=self.CEGUI.WindowManager.getWindow("root/tuto")
		tutoMenu.setMouseInputPropagationEnabled(False)
		tutoMenu.setMouseInputPropagationEnabled(False)
		tutoMenu.show()
		tutoMenu.moveToFront()
		self.CEGUI.WindowManager.getWindow("root/tuto/text").setText(self.tuto[id])
		self.activ=True
		
	def destroy(self):
		self.CEGUI.WindowManager.destroyWindow(self.tutoMenu)
	
	def isActiv(self):
		return self.activ
	