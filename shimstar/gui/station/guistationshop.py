__author__ = 'ogilp'
from shimstar.npc.npcinstation import *
from shimstar.gui.shimcegui import *
from shimstar.user.user import *
from shimstar.gui.core.iteminfo import *
from shimstar.items.templates.itemtemplate import *

class GuiStationShop:
    instance = None
    def __init__(self):
        self.npc = None
        self.CEGUI = ShimCEGUI.getInstance()
        self.root = None
        self.setupUI()


    def emptyInvWindow(self, wndName=""):
        if wndName == "":
            wndName = "Station/Shop/gpachatpanel"
        if self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount() > 0:
            for itChild in range(self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount()):
                wnd = self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildAtIdx(0)
                self.CEGUI.WindowManager.getWindow(wndName).getContentPane().removeChildWindow(wnd)
                wnd.destroy()

        wndName = "Station/Shop/gpventepanel"
        if self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount() > 0:
            for itChild in range(self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount()):
                wnd = self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildAtIdx(0)
                self.CEGUI.WindowManager.getWindow(wndName).getContentPane().removeChildWindow(wnd)
                wnd.destroy()


    def itemDropped(self,args):
        if args.dragDropItem.getChildCount()>0:
            item = args.dragDropItem.getChildAtIdx(0).getUserData()
            # print "itemDropped " + str(item)
            if "achat" in args.window.getName():
                nm = netMessage(C_NETWORK_CHARACTER_SELL_ITEM)
                nm.addUInt(User.getInstance().getId())
                nm.addUInt(item.getId())
                NetworkMainServer.getInstance().sendMessage(nm)
                args.dragDropItem.removeChildWindow(args.dragDropItem.getChildAtIdx(0))
            elif "vente" in args.window.getName():
                nm = netMessage(C_NETWORK_CHARACTER_BUY_ITEM)
                nm.addUInt(User.getInstance().getId())
                nm.addUInt(item.getTemplateId())
                NetworkMainServer.getInstance().sendMessage(nm)

    def initAchatWindow(self):
        i = 0
        j = 0
        listOfImageSet = {}

        for sl in range(40):
            wnd = self.CEGUI.WindowManager.createWindow("DragContainer",
                                                        "Station/Shop/gpachatpanel/DragDropSlot" + str(i) + "-" + str(j))
            wnd.setProperty("UnifiedAreaRect", "{{0," + str(10 + 70 * i) + "},{0," + str(10 + 70 * j) + "},{0," + str(
                10 + 64 + 70 * i) + "},{0," + str(10 + 64 + 70 * j) + "}}")
            wnd.subscribeEvent(PyCEGUI.Window.EventDragDropItemDropped, self, 'itemDropped')
            wnd.setUserString('i', str(i))
            wnd.setUserString('j', str(j))
            self.CEGUI.WindowManager.getWindow("Station/Shop/gpachatpanel").getContentPane().addChildWindow(wnd)
            i += 1
            if i > 6:
                i = 0
                j += 1
                # ~ print self.items
        numItemI = 0
        numItemJ = 0

        listOfTemplate=ItemTemplate.getListOfTemplate()
        for itId in listOfTemplate:
            it=listOfTemplate[itId]
            locI = numItemI % 7
            locJ = int(numItemI / 7)
            panel = self.CEGUI.WindowManager.getWindow("Station/Shop/gpachatpanel")
            wnd = self.CEGUI.WindowManager.getWindow("Station/Shop/gpachatpanel/DragDropSlot" + str(locI) + "-" + str(locJ))
            img = self.CEGUI.WindowManager.createWindow("Shimstar/BackgroundImage",
                                                        "Station/Shop/gpachatpanel/DragDropSlot" + str(locI) + "-" + str(
                                                            locJ) + "/img" + str(locI) + "-" + str(locJ))
            img.setProperty("BackgroundImage", "set:ShimstarImageset image:" + str(it.getImg()))

            img.setMousePassThroughEnabled(True)
            img.setUserData(it)
            wnd.subscribeEvent(PyCEGUI.Window.EventMouseEnters, self, 'showInfo')
            wnd.subscribeEvent(PyCEGUI.Window.EventMouseLeaves, self, 'hideInfo')
            wnd.addChildWindow(img)
            if it.getTypeItem() == C_ITEM_MINERAL:
                label = self.CEGUI.WindowManager.createWindow("Shimstar/Button",
                                                              "Station/Shop/gpachatpanel/label" + str(it.getId()))
                label.setProperty("UnifiedAreaRect", "{{" + str(0.025 + 0.115 * locI) + ",0},{0.2,0},{" + str(
                    0.125 + 0.115 * locI) + ",0},{0.3,0}}");
                label.setProperty("Font", "Brassiere-s")
                label.setText(str(it.getQuantity()))
                panel.addChildWindow(label)
            numItemI += 1

    def initInvWindow(self):
        ship=User.getInstance().getCurrentCharacter().getShip()
        if ship is not None:
            inv=ship.getItemInInventory()
            i = 0
            j = 0
            listOfImageSet = {}
            print inv
            for sl in range(40):
                wnd = self.CEGUI.WindowManager.createWindow("DragContainer",
                                                            "Station/Shop/gpventepanel/DragDropSlot" + str(i) + "-" + str(j))
                wnd.setProperty("UnifiedAreaRect", "{{0," + str(10 + 70 * i) + "},{0," + str(10 + 70 * j) + "},{0," + str(
                    10 + 64 + 70 * i) + "},{0," + str(10 + 64 + 70 * j) + "}}")
                wnd.subscribeEvent(PyCEGUI.Window.EventDragDropItemDropped, self, 'itemDropped')
                wnd.setUserString('i', str(i))
                wnd.setUserString('j', str(j))
                self.CEGUI.WindowManager.getWindow("Station/Shop/gpventepanel").getContentPane().addChildWindow(wnd)
                i += 1
                if i > 6:
                    i = 0
                    j += 1
            numItemI = 0
            numItemJ = 0
            for it in inv:
                locI = numItemI % 7
                locJ = int(numItemI / 7)
                panel = self.CEGUI.WindowManager.getWindow("Station/Shop/gpventepanel")
                wnd = self.CEGUI.WindowManager.getWindow("Station/Shop/gpventepanel/DragDropSlot" + str(locI) + "-" + str(locJ))

                img = self.CEGUI.WindowManager.createWindow("Shimstar/BackgroundImage",
                                                            "Station/Shop/gpventepanel/DragDropSlot" + str(locI) + "-" + str(
                                                                locJ) + "/img" + str(locI) + "-" + str(locJ))
                img.setProperty("BackgroundImage", "set:ShimstarImageset image:" + str(it.getImg()))

                img.setMousePassThroughEnabled(True)
                img.setUserData(it)
                wnd.subscribeEvent(PyCEGUI.Window.EventMouseEnters, self, 'showInfo')
                wnd.subscribeEvent(PyCEGUI.Window.EventMouseLeaves, self, 'hideInfo')
                wnd.addChildWindow(img)
                if it.getTypeItem() == C_ITEM_MINERAL:
                    label = self.CEGUI.WindowManager.createWindow("Shimstar/Button",
                                                                  "Station/Shop/gpventepanel/label" + str(it.getId()))
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

    @staticmethod
    def getInstance(root):
        if GuiStationShop.instance is None:
            GuiStationShop.instance=GuiStationShop()
            GuiStationShop.instance.root = root

        return GuiStationShop.instance

    def setupUI(self):
        self.OutAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Shop"))
        self.InAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Shop"))

        self.CEGUI.WindowManager.getWindow("Station/Shop").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                              self, 'onCloseClicked')

    def hide(self):
        self.OutAnimationInstance.start()

    def show(self):
        self.InAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("Station/Shop").moveToFront()
        self.emptyInvWindow()
        self.initInvWindow()
        self.initAchatWindow()

    def onCloseClicked(self,args):
        self.hide()