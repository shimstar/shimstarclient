# -*- coding: utf-8 -*- 
import sys,os

import PyCEGUI
from shimstar.gui.shimcegui import *
from shimstar.user.user import *
#from shimstar.gui.core.inventory import *

class chooseItemShip():
	#~ def __init__(self,slotType,location,ship):
	def __init__(self,pslot,ship):
		self.ship=ship
		self.location=pslot.getLocation()
		self.listOfImageSet={'titi':'toto'}
		self.listOfImageSet.clear()
		self.CEGUI=PandaCEGUI.getInstance()
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
		print "types = " + str(types) + "/" + str(self.slot.getId())
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

class menuShip():
	instance=None
	def __init__(self):
		self.CEGUI=PandaCEGUI.getInstance()
		self.obj=None
		self.slots=[]
		self.ship=None
		self.listOfImageSet={'titi':'toto'}
		self.listOfImageSet.clear()
		self.slotsFront=[]
		self.slotsRear=[]
		self.slotsMiddle=[]
		self.choix=None
		self.OutAddSuppressAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
		self.InAddSuppressAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
		self.OutAddSuppressAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Addsuppressitem"))
		self.InAddSuppressAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Addsuppressitem"))
		self.CEGUI.WindowManager.getWindow("Station/Addsuppress/Suppress").subscribeEvent(PyCEGUI.PushButton.EventClicked,self,'suppressItem')
		self.CEGUI.WindowManager.getWindow("Station/Addsuppress/Modify").subscribeEvent(PyCEGUI.PushButton.EventClicked,self,'modifyItem')
		self.CEGUI.WindowManager.getWindow("Station/ChoixItem").subscribeEvent(PyCEGUI.Window.EventHidden,self,'refresh')
		self.slotsButton=[]
	
	def refresh(self,winArgs):
		self.emptyWindow("Station/Vaisseau/bckground/Front")
		self.emptyWindow("Station/Vaisseau/bckground/Rear")
		self.emptyWindow("Station/Vaisseau/bckground/Middle")
		menuInventory.getInstance('soute').setObj(self.ship)
		self.setShip(self.ship)
		
	def modifyItem(self,winArgs):
		self.OutAddSuppressAnimationInstance.start()
		self.choix=chooseItemShip(winArgs.window.getUserData(),self.ship)
		
	def suppressItem(self,winArgs):
		self.ship.uninstallItemByPos(int(winArgs.window.getUserString("nb")),int(winArgs.window.getUserString("slot")))
		self.OutAddSuppressAnimationInstance.start()
		#~ self.loadActualItems()
		self.emptyWindow("Station/Vaisseau/bckground/Front")
		self.emptyWindow("Station/Vaisseau/bckground/Rear")
		self.emptyWindow("Station/Vaisseau/bckground/Middle")
		menuInventory.getInstance('soute').setObj(self.ship)
		self.setShip(self.ship)

	def emptyWindow(self,wndName):
		if self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount()>0:
				for itChild in range( self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount()):
					wnd=self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildAtIdx (0)
					self.CEGUI.WindowManager.getWindow(wndName).getContentPane().removeChildWindow(wnd)
					wnd.destroy()

	def setShip(self,ship):
		self.slotsFront=[]
		self.slotsRear=[]
		self.slotsMiddle=[]
		self.slotsButton=[]
		self.ship=ship
		self.slots=self.ship.getSlots()
		iter=[0,0,0,0,0,0]
		for s in self.slots:
			if s.getLocation()==C_SLOT_FRONT:
				button=self.CEGUI.WindowManager.createWindow("Shimstar/ImageButton","Station/Vaisseau/bckground/Front/button=FRONT" + str(iter[C_SLOT_FRONT]) )
				img="windows/slot1.png"
				self.loadImage(img)
				button.setProperty("NormalImage", "set:" + img  +" image:full_image")
				button.setProperty("HoverImage", "set:" + img +" image:full_image")
				button.setProperty("PushedImage", "set:" + img +" image:full_image")
				button.setArea(PyCEGUI.UDim(0, 10 + 80 * iter[C_SLOT_FRONT]), PyCEGUI.UDim(0, 10), PyCEGUI.UDim(0, 64), PyCEGUI.UDim(0, 64))
				button.setUserString("slot",str(C_SLOT_FRONT))
				button.setUserString("nb",str(iter[C_SLOT_FRONT]+1))
				button.setUserData(s)
				self.CEGUI.WindowManager.getWindow("Station/Vaisseau/bckground/Front").getContentPane().addChildWindow(button)
				button.subscribeEvent(PyCEGUI.PushButton.EventClicked,self,'slotClicked')
				self.slotsFront.append(button)
				self.slotsButton.append(button)
				iter[C_SLOT_FRONT]+=1
			elif s.getLocation()==C_SLOT_REAR:
				slot=self.slots[C_SLOT_REAR]
				button=self.CEGUI.WindowManager.createWindow("Shimstar/ImageButton","Station/Vaisseau/bckground/Rear/button=REAR" + str(iter[C_SLOT_REAR]) )
				img="windows/slot1.png"
				self.loadImage(img)
				button.setProperty("NormalImage", "set:" +img +" image:full_image")
				button.setProperty("HoverImage", "set:" + img +" image:full_image")
				button.setProperty("PushedImage", "set:" + img + " image:full_image")
				button.setArea(PyCEGUI.UDim(0, 10 + 80 * iter[C_SLOT_REAR]), PyCEGUI.UDim(0, 10), PyCEGUI.UDim(0, 64), PyCEGUI.UDim(0, 64))
				button.setUserString("slot",str(C_SLOT_REAR))
				button.setUserString("nb",str(iter[C_SLOT_REAR]+1))
				button.setUserData(s)
				button.subscribeEvent(PyCEGUI.PushButton.EventClicked,self,'slotClicked')
				self.CEGUI.WindowManager.getWindow("Station/Vaisseau/bckground/Rear").getContentPane().addChildWindow(button)
				self.slotsRear.append(button)
				self.slotsButton.append(button)
				iter[C_SLOT_REAR]+=1
			elif s.getLocation()==C_SLOT_MIDDLE:
				button=self.CEGUI.WindowManager.createWindow("Shimstar/ImageButton","Station/Vaisseau/bckground/Middle/button=MIDDLE" + str(iter[C_SLOT_MIDDLE]) )
				img="windows/slot1.png"
				self.loadImage(img)
				button.setProperty("NormalImage", "set:" + img +" image:full_image")
				button.setProperty("HoverImage", "set:" + img +" image:full_image")
				button.setProperty("PushedImage", "set:" + img+" image:full_image")
				button.setArea(PyCEGUI.UDim(0, 10 + 80 * iter[C_SLOT_MIDDLE]), PyCEGUI.UDim(0, 10), PyCEGUI.UDim(0, 64), PyCEGUI.UDim(0, 64))
				button.setUserString("slot",str(C_SLOT_MIDDLE))
				button.setUserString("nb",str(iter[C_SLOT_MIDDLE]+1))
				button.setUserData(s)
				button.subscribeEvent(PyCEGUI.PushButton.EventClicked,self,'slotClicked')
				self.CEGUI.WindowManager.getWindow("Station/Vaisseau/bckground/Middle").getContentPane().addChildWindow(button)
				self.slotsMiddle.append(button)
				self.slotsButton.append(button)
				iter[C_SLOT_MIDDLE]+=1
				
		self.loadActualItems()
		self.energyState()
		
	def slotClicked(self,winArgs):
		if self.choix!=None:
			self.choix.destroy()
		self.InAddSuppressAnimationInstance.start()
		winArgs.window.getUserString("slot"),winArgs.window.getUserString("nb")
		self.CEGUI.WindowManager.getWindow("Station/Addsuppressitem").moveToFront()
		self.CEGUI.WindowManager.getWindow("Station/Addsuppress/Suppress").setUserString("slot",winArgs.window.getUserString("slot"))
		self.CEGUI.WindowManager.getWindow("Station/Addsuppress/Suppress").setUserString("nb",winArgs.window.getUserString("nb"))
		self.CEGUI.WindowManager.getWindow("Station/Addsuppress/Modify").setUserString("slot",winArgs.window.getUserString("slot"))
		self.CEGUI.WindowManager.getWindow("Station/Addsuppress/Modify").setUserString("nb",winArgs.window.getUserString("nb"))
		self.CEGUI.WindowManager.getWindow("Station/Addsuppress/Modify").setUserData(winArgs.window.getUserData())
	
	def loadImage(self,img):
		if self.listOfImageSet.has_key(img)==False:
			customImageset = self.CEGUI.ImageSetManager.createFromImageFile(img , img, "images")
			customImageset.setNativeResolution(PyCEGUI.Size(32,32))
			customImageset.setAutoScalingEnabled(False)
			self.listOfImageSet[img]=customImageset
		
		#~ return customImageset
		
	def energyState(self):
		nrj=0
		nrjMax=0
		for it in self.ship.getItems():
			if it.getTypeItem() == C_ITEM_ENERGY:
				nrjMax+=it.getEnergy()
			else:
				nrj+=it.getEnergyCost()
		if int(nrj)<=int(nrjMax):
			msg="Energie : " + str(nrj) + "/" + str(nrjMax)
		else:
			msg="Energie : [colour='FFFF0000']" + str(nrj) + "[colour='FFFFFFFF']/" + str(nrjMax)
		self.CEGUI.WindowManager.getWindow("Station/Vaisseau/Energie").setText(msg)

	def showInfo(self,args):
		item=args.window.getUserData().getItem()
		menuItemInfo.getInstance().setObj(item)
		self.CEGUI.WindowManager.getWindow("InfoItem").setPosition(args.window.getPosition())
		
	def hideInfo(self,args):
		menuItemInfo.getInstance().hide()
		#~ self.CEGUI.WindowManager.getWindow("InfoItem").hide()

	def loadActualItems(self):
		for sb in self.slotsButton:
			item=sb.getUserData().getItem()
			if item!=None:
				img="items/" + item.getImg() + ".png"
				self.loadImage(img)
				sb.setProperty("NormalImage", "set:" + img +" image:full_image")
				sb.setProperty("HoverImage", "set:" + img +" image:full_image")
				sb.setProperty("PushedImage", "set:" + img+" image:full_image")
				sb.subscribeEvent(PyCEGUI.Window.EventMouseEnters,self,'showInfo')
				sb.subscribeEvent(PyCEGUI.Window.EventMouseLeaves,self,'hideInfo')
		
	def hideChoice(self):
		if self.choix!=None:
			self.choix.destroy()

	@staticmethod
	def getInstance():
		if menuShip.instance==None:
			menuShip.instance=menuShip()
		return menuShip.instance
		