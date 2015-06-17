# -*- coding: utf-8 -*- 
import sys, os

import PyCEGUI
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from shimstar.gui.shimcegui import *
from shimstar.user.user import *
# from shimstar.gui.core.iteminfo import *

class menuInventory(DirectObject):
    instances = {'soute': None, 'invstation': None}

    def __init__(self, typeInv):
        self.CEGUI = ShimCEGUI.getInstance()
        self.obj = None
        self.typeInv = typeInv
        self.items = []
        self.parent = None
        self.CEGUI.WindowManager.getWindow("InfoItem").setMouseInputPropagationEnabled(True)

    @staticmethod
    def getInstance(typeInv):
        if menuInventory.instances.has_key(typeInv) == False or menuInventory.instances[typeInv] == None:
            menuInventory.instances[typeInv] = menuInventory(typeInv)
        return menuInventory.instances[typeInv]

    def setObj(self, obj):
        self.obj = obj
        self.items = self.obj.getItemInInventory()
        self.setItems()

    def refresh(self):
        self.items = self.obj.getItemInInventory()
        self.setItems()

    def emptyInvWindow(self, wndName=""):
        if wndName == "":
            wndName = "Inventaire/Panel"
        if self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount() > 0:
            for itChild in range(self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount()):
                wnd = self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildAtIdx(0)
                self.CEGUI.WindowManager.getWindow(wndName).getContentPane().removeChildWindow(wnd)
                wnd.destroy()

    def setParent(self, parent):
        self.parent = parent

    def closeClicked(self, args):
        self.emptyLootsWindow()
        self.wndCegui.WindowManager.getWindow("HUD/Cockpit/Loots").hide()

    def setItems(self):
        self.emptyInvWindow()
        i = 0
        j = 0
        listOfImageSet = {}

        for sl in range(40):
            wnd = self.CEGUI.WindowManager.createWindow("DragContainer",
                                                        "Inventaire/Panel/DragDropSlot" + str(i) + "-" + str(j))
            wnd.setProperty("UnifiedAreaRect", "{{0," + str(10 + 70 * i) + "},{0," + str(10 + 70 * j) + "},{0," + str(
                10 + 64 + 70 * i) + "},{0," + str(10 + 64 + 70 * j) + "}}")
            wnd.subscribeEvent(PyCEGUI.Window.EventDragDropItemDropped, self.parent, 'itemDropped')
            wnd.setUserString('i', str(i))
            wnd.setUserString('j', str(j))
            self.CEGUI.WindowManager.getWindow("Inventaire/Panel").getContentPane().addChildWindow(wnd)
            i += 1
            if i > 6:
                i = 0
                j += 1
                # ~ print self.items
        numItemI = 0
        numItemJ = 0
        for it in self.items:
            #~ print it
            #~ loc=it.getLocation()
            locI = numItemI % 7
            locJ = int(numItemI / 7)
            panel = self.CEGUI.WindowManager.getWindow("Inventaire/Panel")
            wnd = self.CEGUI.WindowManager.getWindow("Inventaire/Panel/DragDropSlot" + str(locI) + "-" + str(locJ))
            #~ if listOfImageSet.has_key("TempImageset" + str(it.getImg()) )==False:
            #~ customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImageset" + str(it.getImg()) , "items/" + str(it.getImg()) + ".png", "images")
            #~ customImageset.setNativeResolution(PyCEGUI.Size(64,64))
            #~ customImageset.setAutoScalingEnabled(False)
            #~ listOfImageSet["TempImageset" + str(it.getImg()) ]=customImageset
            img = self.CEGUI.WindowManager.createWindow("Shimstar/BackgroundImage",
                                                        "Inventaire/Panel/DragDropSlot" + str(locI) + "-" + str(
                                                            locJ) + "/img" + str(locI) + "-" + str(locJ))
            img.setProperty("BackgroundImage", "set:ShimstarImageset image:" + str(it.getImg()))

            img.setMousePassThroughEnabled(True)
            img.setUserData(it)
            wnd.subscribeEvent(PyCEGUI.Window.EventMouseEnters, self, 'showInfo')
            wnd.subscribeEvent(PyCEGUI.Window.EventMouseLeaves, self, 'hideInfo')
            wnd.addChildWindow(img)
            if it.getTypeItem() == C_ITEM_MINERAL:
                label = self.CEGUI.WindowManager.createWindow("Shimstar/Button",
                                                              "Inventaire/Panel/label" + str(it.getId()))
                label.setProperty("UnifiedAreaRect", "{{" + str(0.025 + 0.115 * locI) + ",0},{0.2,0},{" + str(
                    0.125 + 0.115 * locI) + ",0},{0.3,0}}");
                label.setProperty("Font", "Brassiere-s")
                label.setText(str(it.getQuantity()))
                panel.addChildWindow(label)
            numItemI += 1

    def showInfo(self, args):
        if args.window.getChildCount() > 0:
            img = args.window.getChildAtIdx(0)
            item = img.getUserData()
            menuItemInfo.getInstance().setObj(item)

            self.CEGUI.WindowManager.getWindow("InfoItem").setPosition(args.window.getPosition())

    def hideInfo(self, args):
        menuItemInfo.getInstance().hide()
