__author__ = 'ogilp'
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from shimstar.npc.npcinstation import *
from shimstar.gui.shimcegui import *
from shimstar.user.user import *
from shimstar.gui.core.iteminfo import *
from shimstar.items.templates.itemtemplate import *
from shimstar.gui.station.guistationship import *

class GuiStationFitting(DirectObject):
    instance = None
    def __init__(self):
        self.CEGUI = ShimCEGUI.getInstance()
        self.root = None
        self.listOfImageSet={}
        self.setupUI()

    def event(self,task):
        toUpdate=False
        tempMsg = NetworkMainServer.getInstance().getListOfMessageById(C_NETWORK_CHARACTER_ITEM_ENABLED)
        if len(tempMsg) > 0:
            for msg in tempMsg:
                netMsg = msg.getMessage()
                nbItem = int(netMsg[0])
                compteur=1
                for iterateur in range(nbItem):
                    idItem=int(netMsg[compteur])
                    compteur+=1
                    status = True if int(netMsg[compteur])==1 else False
                    compteur+=1
                    ship=User.getInstance().getCurrentCharacter().getShip()
                    if ship is not None:
                        for s in ship.getSlots():
                            it = s.getItem()
                            if it is not None:
                                if it.getId() == idItem:
                                    it.setEnabled(status)
                                    toUpdate=True
                                    break
                NetworkMainServer.getInstance().removeMessage(msg)

        if toUpdate == True :
            self.emptyWindowSlot()
        return task.cont

    def modifyItem(self, winArgs):
        self.OutAddSuppressAnimationInstance.start()
        # self.choix = chooseItemShip(winArgs.window.getUserData(), User.getInstance().getCurrentCharacter().getShip())
        self.choix = chooseItemShip.getInstance(winArgs.window.getUserData(), User.getInstance().getCurrentCharacter().getShip())


    def emptyWindowSlot(self, winArgs=None):
        wndName = "Station/Vaisseau/bckground/Front"
        if self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount() > 0:
            for itChild in range(self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount()):
                wnd = self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildAtIdx(0)
                self.CEGUI.WindowManager.getWindow(wndName).getContentPane().removeChildWindow(wnd)
                wnd.destroy()
        ship = User.getInstance().getCurrentCharacter().getShip()
        # menuInventory.getInstance('soute').setObj(ship)
        self.showFitting()

    def suppressItem(self, winArgs):
        sl = winArgs.window.getUserData()
        User.getInstance().getCurrentCharacter().getShip().uninstallItem(sl)
        self.OutAddSuppressAnimationInstance.start()
        self.emptyWindowSlot()

    def showFitting(self):
        ship = User.getInstance().getCurrentCharacter().getShip()
        i = 0
        slots = ship.getSlots()
        itemSlotted = []

        for s in slots:
            button = self.CEGUI.WindowManager.createWindow("Shimstar/ImageButton",
                                                           "Station/Vaisseau/bckground/Front/slot" + str(s.getId()))

            if self.listOfImageSet.has_key("TempImagesetslot1") == False:
                customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImagesetslot1",
                                                                                "/windows/slot1.png", "images")
                customImageset.setNativeResolution(PyCEGUI.Size(64, 64))
                customImageset.setAutoScalingEnabled(False)
                self.listOfImageSet["TempImagesetslot1"] = customImageset

            if s.getItem() != None:
                itemSlotted.append(s.getItem())
                ko = "" if s.getItem().isEnabled() else "ko"
                button.setProperty("NormalImage", "set:ShimstarImageset image:" + s.getItem().getImg() + ko )
                button.setProperty("HoverImage", "set:ShimstarImageset image:" + s.getItem().getImg() + ko )
                button.setProperty("PushedImage", "set:ShimstarImageset image:" + s.getItem().getImg() + ko )
                button.subscribeEvent(PyCEGUI.Window.EventMouseEnters, self, 'showInfo')
                button.subscribeEvent(PyCEGUI.Window.EventMouseLeaves, self, 'hideInfo')
            else:
                button.setProperty("NormalImage", "set:TempImagesetslot1 image:full_image")
                button.setProperty("HoverImage", "set:TempImagesetslot1 image:full_image")
                button.setProperty("PushedImage", "set:TempImagesetslot1 image:full_image")

            button.setProperty("UnifiedAreaRect", "{{" + str(0.10 + 0.15 * i) + ",0},{0.14,0},{" + str(
                0.218 + 0.15 * i) + ",0},{0.268,0}}");
            button.setProperty("UnifiedSize", "{{0,64},{0,64}}")
            button.setUserData(s)
            button.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'slotClicked')

            self.CEGUI.WindowManager.getWindow("Station/Vaisseau/bckground/Front").addChildWindow(button)

            tp = s.getTypes()

            lblType = ""
            for t in tp:
                if t == C_ITEM_ENGINE:
                    lblType += "M"
                elif t == C_ITEM_WEAPON:
                    lblType += "A"
                elif t == C_ITEM_ENERGY:
                    lblType += "J"
                elif t == C_ITEM_CONTAINER:
                    lblType += "C"
                elif t == C_ITEM_ELECTRO:
                    lblType += "E"
                elif t == C_ITEM_RADAR:
                    lblType += "R"
                elif t == C_ITEM_MINING:
                    lblType += "G"
            label = self.CEGUI.WindowManager.createWindow("Shimstar/Button",
                                                          "Station/Vaisseau/bckground/Front/slotlabel" + str(s.getId()))
            #~ label.setProperty("UnifiedAreaRect", "{{" + str(0.10+0.15*i) + ",0},{0.30,0},{" + str(0.31+0.15*i) + ",0},{0.65,0}}");
            label.setProperty("UnifiedAreaRect",
                              "{{" + str(0.08 + 0.15 * i) + ",0},{0.28,0},{" + str(0.2 + 0.15 * i) + ",0},{0.35,0}}");
            label.setText(lblType)
            label.setUserData(s)
            label.setFont("Brassiere-s")
            #~ label.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'onChooseNpc')
            self.CEGUI.WindowManager.getWindow("Station/Vaisseau/bckground/Front").addChildWindow(label)
            i += 1
            energyCost = 0
            energy = 0
            for it in itemSlotted:
                if it.getTypeItem() == C_ITEM_ENERGY:
                    energy += it.getEnergy()
                else:
                    energyCost += it.getEnergyCost()
            textEnergy = str(energyCost)
            if energy < energyCost:
                textEnergy = "[colour='FFFF0000']" + str(energyCost)
            self.CEGUI.WindowManager.getWindow("Station/Vaisseau/Energie").setText("Consommation Energie :      " + textEnergy + " / " + str(energy))

    def slotClicked(self, e):
        self.InAddSuppressAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("Station/Addsuppressitem").moveToFront()
        self.CEGUI.WindowManager.getWindow("Station/Addsuppress/Suppress").setUserData(e.window.getUserData())
        self.CEGUI.WindowManager.getWindow("Station/Addsuppress/Modify").setUserData(e.window.getUserData())


    def showInfo(self, args):
        item = args.window.getUserData().getItem()
        pos = args.window.getPosition()
        pos.d_x.d_scale = pos.d_x.d_scale + 0.1
        menuItemInfo.getInstance().setObj(item)
        self.CEGUI.WindowManager.getWindow("InfoItem").setPosition(pos)

    def hideInfo(self, args):
        menuItemInfo.getInstance().hide()

    @staticmethod
    def getInstance(root):
        if GuiStationFitting.instance is None:
            GuiStationFitting.instance=GuiStationFitting()
            GuiStationFitting.instance.root = root

        return GuiStationFitting.instance

    @staticmethod
    def isInstantiated():
        if GuiStationFitting.instance is not None:
            return True
        return False


    def setupUI(self):
        self.OutShipAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InShipAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutShipAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Vaisseau"))
        self.InShipAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Vaisseau"))

        self.CEGUI.WindowManager.getWindow("Station/Vaisseau").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                              self, 'onCloseClicked')
        self.CEGUI.WindowManager.getWindow("Station/Vaisseau").subscribeEvent(PyCEGUI.PushButton.EventClicked,
                                                                                   self, 'buttonSwitch')
        self.CEGUI.WindowManager.getWindow("Station/Addsuppress/Suppress").subscribeEvent(
            PyCEGUI.PushButton.EventClicked, self, 'suppressItem')
        self.CEGUI.WindowManager.getWindow("Station/Addsuppress/Modify").subscribeEvent(PyCEGUI.PushButton.EventClicked,
                                                                                        self, 'modifyItem')
        self.CEGUI.WindowManager.getWindow("Station/ChoixItem").subscribeEvent(PyCEGUI.Window.EventHidden, self,
                                                                               'emptyWindowSlot')
        self.OutAddSuppressAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InAddSuppressAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutAddSuppressAnimationInstance.setTargetWindow(
            self.CEGUI.WindowManager.getWindow("Station/Addsuppressitem"))
        self.InAddSuppressAnimationInstance.setTargetWindow(
            self.CEGUI.WindowManager.getWindow("Station/Addsuppressitem"))

    def hide(self):
        self.OutShipAnimationInstance.start()
        self.OutAddSuppressAnimationInstance.start()
        taskMgr.remove("event guifitting")

    def destroy(self):
        taskMgr.remove("event guifitting")
        GuiStationFitting.instance = None

    def show(self):
        self.InShipAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("Station/Vaisseau").moveToFront()
        self.emptyWindowSlot()
        taskMgr.add(self.event,"event guifitting",-40)

    def onCloseClicked(self,args):
        self.hide()