import sys,os

import PyCEGUI
from shimstar.gui.shimcegui import *
from shimstar.user.user import *
from shimstar.gui.core.iteminfo import *

class chooseItemShip():
	#~ def __init__(self,slotType,location,ship):
	def __init__(self,pslot,ship):
		self.ship=ship
		self.location=pslot.getLocation()
		self.listOfImageSet={}
		self.CEGUI=ShimCEGUI.getInstance()
		self.OutShipAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
		self.InShipAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
		self.OutShipAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/ChoixItem"))
		self.CEGUI.WindowManager.getWindow("Station/ChoixItem").moveToFront()
		self.InShipAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/ChoixItem"))
		self.CEGUI.WindowManager.getWindow("Station/ChoixItem").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,self,'closeClicked')
	
		self.InShipAnimationInstance.start()
		inventory=ship.getItemInInventory()
		self.slot=pslot
		types=self.slot.getTypes()
		i=0
		j=0
		#~ print "types = " + str(types) + "/" + str(self.slot.getId())
		for inv in inventory:
			suitable=False
			for ty in types:
				if inv.getTypeItem()==int(ty):
					suitable=True
			if suitable==True:
				img="items/" + inv.getImg() + ".png"
				self.loadImage(img )
				button=self.CEGUI.WindowManager.createWindow("Shimstar/ImageButton","Station/Vaisseau/ChoixItem/button" + str(i)  + "-" + str(j))
				button.setProperty("NormalImage", "set:" +img +" image:full_image")
				button.setProperty("HoverImage", "set:" + img +" image:full_image")
				button.setProperty("PushedImage", "set:" + img + " image:full_image")
				button.setArea(PyCEGUI.UDim(0, 10 + 80 * i), PyCEGUI.UDim(0, 10), PyCEGUI.UDim(0, 64), PyCEGUI.UDim(0, 64))
				button.setUserString("slot",str(C_SLOT_FRONT))
				button.setUserString("nb",str(i))
				button.setUserData(inv)
				button.subscribeEvent(PyCEGUI.Window.EventMouseEnters,self,'showInfo')
				button.subscribeEvent(PyCEGUI.Window.EventMouseLeaves,self,'hideInfo')
				button.subscribeEvent(PyCEGUI.PushButton.EventClicked,self,'chooseItem')
				self.CEGUI.WindowManager.getWindow("Station/ChoixItem/Panel").getContentPane().addChildWindow(button)
				
				i+=1
				if i > 3:
					i=0
					j+=1
					
	def closeClicked(self,windowEventArgs):
		if (windowEventArgs.window.getName() == "Station/ChoixItem"):
			self.OutShipAnimationInstance.start()
					
	def chooseItem(self,windowArg):
		if windowArg.window.getUserData()==None:
			self.ship.uninstallItemByPos(self.location,self.slot.getLocation())
		else:
			self.ship.installItem(windowArg.window.getUserData(),self.slot)
		self.destroy()
					
	def loadImage(self,img):
		if self.listOfImageSet.has_key(img)==False:
			customImageset = self.CEGUI.ImageSetManager.createFromImageFile(img , img, "images")
			customImageset.setNativeResolution(PyCEGUI.Size(64,64))
			customImageset.setAutoScalingEnabled(False)
			self.listOfImageSet[img]=customImageset
		
	def destroy(self):
		self.emptyInvWindow()
		self.OutShipAnimationInstance.start()
		
	def emptyInvWindow(self):
		if self.CEGUI.WindowManager.getWindow("Station/ChoixItem/Panel").getContentPane().getChildCount()>0:
				for itChild in range( self.CEGUI.WindowManager.getWindow("Station/ChoixItem/Panel").getContentPane().getChildCount()):
					wnd=self.CEGUI.WindowManager.getWindow("Station/ChoixItem/Panel").getContentPane().getChildAtIdx (0)
					self.CEGUI.WindowManager.getWindow("Station/ChoixItem/Panel").getContentPane().removeChildWindow(wnd)
					wnd.destroy()

	def showInfo(self,args):
		#~ item=args.window.getUserData().getItem()
		item=args.window.getUserData()
		menuItemInfo.getInstance().setObj(item)
		self.CEGUI.WindowManager.getWindow("InfoItem").setPosition(args.window.getPosition())
		
	def hideInfo(self,args):
		menuItemInfo.getInstance().hide()