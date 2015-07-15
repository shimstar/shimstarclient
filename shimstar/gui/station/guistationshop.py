__author__ = 'ogilp'
from shimstar.npc.npcinstation import *
from shimstar.gui.shimcegui import *

class GuiStationShop:
    instance = None
    def __init__(self):
        self.npc = None
        self.CEGUI = ShimCEGUI.getInstance()
        self.root = None

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

    def onCloseClicked(self,args):
        self.hide()