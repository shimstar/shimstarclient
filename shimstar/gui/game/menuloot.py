from shimstar.items.junk import *
from shimstar.gui.shimcegui import *
from shimstar.core.constantes import *
from shimstar.gui.core.iteminfo import *
from shimstar.network.netmessage import *
from shimstar.network.networkzoneserver import *
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task

class MenuLoot(DirectObject):
    instance = None
    def __init__(self):
        self.junk = None
        self.CEGUI = ShimCEGUI.getInstance()
        self.items = []
        self.parent = None
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Loots").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                              self, 'onCloseClicked')
        self.OutLootAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InLootAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutLootAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Loots"))
        self.InLootAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Loots"))
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Loots/TakeButton").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                           'onTakeClicked')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Loots/DestroyButton").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                           'onDestroyClicked')


    def onTakeClicked(self,wnd):
        for idIt in self.items:
            nm = netMessage(C_NETWORK_CHARACTER_ADD_TO_INVENTORY_FROM_JUNK)
            nm.addInt(User.getInstance().getId())
            nm.addInt(self.junk.getId())
            nm.addInt(idIt)
            NetworkZoneServer.getInstance().sendMessage(nm)

    def onDestroyClicked(self,wnd):
        nm = netMessage(C_NETWORK_DESTROY_JUNK)
        nm.addInt(User.getInstance().getId())
        nm.addInt(self.junk.getId())
        NetworkZoneServer.getInstance().sendMessage(nm)
        self.OutLootAnimationInstance.start()

    def setParent(self,parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def setJunk(self,junk):
        self.junk = junk
        self.items = self.junk.getItems()
        self.setItems()

    def refresh(self):
        print "MenuLoot :: refresh " + str(self.junk.getItems())
        self.items = self.junk.getItems()
        self.setItems()
        self.show()

    def getJunk(self):
        return self.junk

    def show(self):
        # self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Loots").show()
        self.InLootAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Loots").moveToFront()
        taskMgr.add(self.event,"event loot",-40)

    def event(self,task):
        temp=NetworkZoneServer.getInstance().getListOfMessageById(C_NETWORK_CHARACTER_ADD_TO_INVENTORY_FROM_JUNK)
        if(len(temp)>0):
            msg=temp[0]
            netMsg=msg.getMessage()
            usrID=int(netMsg[0])
            junkId=int(netMsg[1])
            itId=int(netMsg[2])
            itemToTransfert = self.junk.removeItemById(itId)
            if itemToTransfert is not None :
                char = User.getInstance().getCurrentCharacter()
                if char.getShip() is not None:
                    char.getShip().addItemInInventory(itemToTransfert)
                self.refresh()
            NetworkZoneServer.getInstance().removeMessage(msg)

        return task.cont

    @staticmethod
    def getInstance():
        if MenuLoot.instance is None:
            MenuLoot.instance = MenuLoot()

        return MenuLoot.instance

    @staticmethod
    def isInstantiated():
        if MenuLoot.instance is not None:
            return True
        return False

    def emptyLootsWindow(self, wndName=""):
        if wndName == "":
            wndName = "HUD/Cockpit/Loots/Panel"
        if self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount() > 0:
            for itChild in range(self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount()):
                wnd = self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildAtIdx(0)
                self.CEGUI.WindowManager.getWindow(wndName).getContentPane().removeChildWindow(wnd)
                wnd.destroy()

    def onCloseClicked(self, args):
        self.emptyLootsWindow()
        self.OutLootAnimationInstance.start()
        taskMgr.remove("event loot")

    def destroy(self):
        taskMgr.remove("event loot")
        MenuLoot.instance = None


    def setItems(self):
        self.emptyLootsWindow()
        i = 0
        j = 0
        listOfImageSet = {}

        for sl in range(40):
            wnd = self.CEGUI.WindowManager.createWindow("DragContainer",
                                                        "HUD/Cockpit/Loots/Panel/DragDropSlot" + str(i) + "-" + str(j))
            wnd.setProperty("UnifiedAreaRect", "{{0," + str(10 + 70 * i) + "},{0," + str(10 + 70 * j) + "},{0," + str(
                10 + 64 + 70 * i) + "},{0," + str(10 + 64 + 70 * j) + "}}")
            wnd.subscribeEvent(PyCEGUI.Window.EventDragDropItemDropped, self.parent, 'itemDropped')
            wnd.setUserString('i', str(i))
            wnd.setUserString('j', str(j))
            self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Loots/Panel").getContentPane().addChildWindow(wnd)
            i += 1
            if i > 6:
                i = 0
                j += 1
        numItemI = 0
        numItemJ = 0
        for it in self.items:

            locI = numItemI % 7
            locJ = int(numItemI / 7)
            panel = self.CEGUI.WindowManager.getWindow("Inventaire/Panel")
            wnd = self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Loots/Panel/DragDropSlot" + str(locI) + "-" + str(locJ))
            img = self.CEGUI.WindowManager.createWindow("Shimstar/BackgroundImage",
                                                        "HUD/Cockpit/Loots/Panel/DragDropSlot" + str(locI) + "-" + str(
                                                            locJ) + "/img" + str(locI) + "-" + str(locJ))
            img.setProperty("BackgroundImage", "set:ShimstarImageset image:" + str(self.items[it].getImg()))

            img.setMousePassThroughEnabled(True)
            img.setUserData(self.items[it])
            wnd.subscribeEvent(PyCEGUI.Window.EventMouseEnters, self, 'showInfo')
            wnd.subscribeEvent(PyCEGUI.Window.EventMouseLeaves, self, 'hideInfo')
            wnd.subscribeEvent(PyCEGUI.Window.EventMouseDoubleClick,self,'dblClick')
            wnd.addChildWindow(img)
            if self.items[it].getTypeItem() == C_ITEM_MINERAL:
                label = self.CEGUI.WindowManager.createWindow("Shimstar/Button",
                                                              "HUD/Cockpit/Loots/Panel/label" + str(self.items[i].getId()))
                label.setProperty("UnifiedAreaRect", "{{" + str(0.025 + 0.115 * locI) + ",0},{0.2,0},{" + str(
                    0.125 + 0.115 * locI) + ",0},{0.3,0}}")
                label.setProperty("Font", "Brassiere-s")
                label.setText(str(self.items[it].getQuantity()))
                panel.addChildWindow(label)
            numItemI += 1

    def dblClick(self,args):
       if args.window.getChildCount() > 0:
            img = args.window.getChildAtIdx(0)
            item = img.getUserData()
            if item is not None:
                nm = netMessage(C_NETWORK_CHARACTER_ADD_TO_INVENTORY_FROM_JUNK)
                nm.addInt(User.getInstance().getId())
                nm.addInt(self.junk.getId())
                nm.addInt(item.getId())
                NetworkZoneServer.getInstance().sendMessage(nm)

    def showInfo(self, args):
        if args.window.getChildCount() > 0:
            img = args.window.getChildAtIdx(0)
            item = img.getUserData()
            menuItemInfo.getInstance().setObj(item)
            posX = 0
            if args.window.getPosition().d_x.d_offset < 300:
                posX = args.window.getPosition().d_x.d_offset + 100
            else:
                posX = args.window.getPosition().d_x.d_offset - 100
            posY = args.window.getPosition().d_y.d_offset

            offsetX = posX / base.win.getXSize()
            offsetY = posY / base.win.getYSize()

            self.CEGUI.WindowManager.getWindow("InfoItem").setPosition(PyCEGUI.UVector2(PyCEGUI.UDim(offsetX,0), PyCEGUI.UDim(offsetY,0)))

    def hideInfo(self, args):
        menuItemInfo.getInstance().hide()