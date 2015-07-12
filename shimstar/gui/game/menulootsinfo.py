__author__ = 'ogilp'
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from shimstar.gui import *

class MenuLootsInfo(DirectObject):
    instance=None
    def __init__(self):
        self.junk = None
        self.CEGUI = ShimCEGUI.getInstance()
        self.parent = None
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/LootsWindow").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                              self, 'onCloseClicked')
        self.OutAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/LootsWindow"))
        self.InAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/LootsWindow"))

    def event(self,task):

        return task.cont

    def setParent(self,parent):
        self.parent=parent

    def setTarget(self,junk):
        self.junk=junk

    def onCloseClicked(self, args):
        self.hide()

    def hide(self):
        self.OutAnimationInstance.start()
        taskMgr.remove("event loot Info")

    def show(self):
        self.InAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/LootsWindow").moveToFront()
        taskMgr.add(self.event,"event loot Info",-40)

    def destroy(self):
        taskMgr.remove("event loot")

    @staticmethod
    def getInstance():
        if MenuLootsInfo.instance is None:
            MenuLootsInfo.instance = MenuLootsInfo()
        return MenuLootsInfo.instance