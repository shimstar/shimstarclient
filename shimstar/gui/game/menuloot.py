from shimstar.items.junk import *
from shimstar.gui.shimcegui import *
from shimstar.core.constantes import *

class MenuLoot:
    instance = None
    def __init__(self):
        self.junk = None
        self.CEGUI = ShimCEGUI.getInstance()
        self.items = []
        self.parent = None

    def setParent(self,parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def setJunk(self,junk):
        self.junk = junk
        self.items = self.junk.getItems()
        self.setItems()

    def refresh(self):
        self.items = self.junk.getItems()
        self.setItems()
        self.show()

    def getJunk(self):
        return self.junk

    def show(self):
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Loots").show()
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Loots").moveToFront()

    @staticmethod
    def getInstance():
        if MenuLoot.instance is None:
            MenuLoot.instance = MenuLoot()

        return MenuLoot.instance

    def emptyLootsWindow(self, wndName=""):
        if wndName == "":
            wndName = "HUD/Cockpit/Loots/Panel"
        if self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount() > 0:
            for itChild in range(self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount()):
                wnd = self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildAtIdx(0)
                self.CEGUI.WindowManager.getWindow(wndName).getContentPane().removeChildWindow(wnd)
                wnd.destroy()

    def closeClicked(self, args):
        self.emptyLootsWindow()
        self.wndCegui.WindowManager.getWindow("HUD/Cockpit/Loots").hide()

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
                # ~ print self.items
        numItemI = 0
        numItemJ = 0
        print self.items
        for it in self.items:
            #~ print it
            #~ loc=it.getLocation()
            locI = numItemI % 7
            locJ = int(numItemI / 7)
            panel = self.CEGUI.WindowManager.getWindow("Inventaire/Panel")
            wnd = self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Loots/Panel/DragDropSlot" + str(locI) + "-" + str(locJ))
            #~ if listOfImageSet.has_key("TempImageset" + str(it.getImg()) )==False:
            #~ customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImageset" + str(it.getImg()) , "items/" + str(it.getImg()) + ".png", "images")
            #~ customImageset.setNativeResolution(PyCEGUI.Size(64,64))
            #~ customImageset.setAutoScalingEnabled(False)
            #~ listOfImageSet["TempImageset" + str(it.getImg()) ]=customImageset
            img = self.CEGUI.WindowManager.createWindow("Shimstar/BackgroundImage",
                                                        "HUD/Cockpit/Loots/Panel/DragDropSlot" + str(locI) + "-" + str(
                                                            locJ) + "/img" + str(locI) + "-" + str(locJ))
            img.setProperty("BackgroundImage", "set:ShimstarImageset image:" + str(self.items[it].getImg()))

            img.setMousePassThroughEnabled(True)
            img.setUserData(self.items[it])
            wnd.subscribeEvent(PyCEGUI.Window.EventMouseEnters, self, 'showInfo')
            wnd.subscribeEvent(PyCEGUI.Window.EventMouseLeaves, self, 'hideInfo')
            wnd.addChildWindow(img)
            if self.items[it].getTypeItem() == C_ITEM_MINERAL:
                label = self.CEGUI.WindowManager.createWindow("Shimstar/Button",
                                                              "HUD/Cockpit/Loots/Panel/label" + str(self.items[i].getId()))
                label.setProperty("UnifiedAreaRect", "{{" + str(0.025 + 0.115 * locI) + ",0},{0.2,0},{" + str(
                    0.125 + 0.115 * locI) + ",0},{0.3,0}}");
                label.setProperty("Font", "Brassiere-s")
                label.setText(str(self.items[it].getQuantity()))
                panel.addChildWindow(label)
            numItemI += 1