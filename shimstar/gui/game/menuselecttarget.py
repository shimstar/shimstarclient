__author__ = 'ogilp'
from shimstar.gui.shimcegui import *
from shimstar.npc.npc import *
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task

class MenuSelectTarget(DirectObject):
    instance = None
    def __init__(self):
        self.junk = None
        self.CEGUI = ShimCEGUI.getInstance()
        self.items = []
        self.parent = None
        self.listOfUser = []
        self.lastTicks = 0
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/TargetSelect").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                              self, 'onCloseClicked')
        self.OutAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/TargetSelect"))
        self.InAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/TargetSelect"))

    def emptyLootsWindow(self, wndName=""):
        if wndName == "":
            wndName = "HUD/Cockpit/TargetSelect/Panel"
        if self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount() > 0:
            for itChild in range(self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount()):
                wnd = self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildAtIdx(0)
                self.CEGUI.WindowManager.getWindow(wndName).getContentPane().removeChildWindow(wnd)
                wnd.destroy()

    def event(self,task):
        self.panel = self.CEGUI.WindowManager.getWindow("HUD/Cockpit/TargetSelect/Panel")
        dt = globalClock.getRealTime() - self.lastTicks
        if dt > 1:
            self.emptyLootsWindow()
            self.lastTicks = globalClock.getRealTime()
            for n in NPC.getListOfNpc():
                label = self.CEGUI.WindowManager.createWindow("Shimstar/Button",
                                                          "HUD/Cockpit/TargetSelect/Panel/labeltgt=" + str(n.getName()))
                label.setProperty("UnifiedAreaRect",
                              "{{" + str(0.10 + 0.15) + ",0},{0.20,0},{" + str(0.21 + 0.15) + ",0},{0.36,0}}");
                self.panel.addChildWindow(label)
        return task.cont

    def show(self):
        # self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Loots").show()
        self.InAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/TargetSelect").moveToFront()
        taskMgr.add(self.event,"event selecttarget",-40)

    def onCloseClicked(self, args):
        # self.emptyLootsWindow()
        # self.wndCegui.WindowManager.getWindow("HUD/Cockpit/Loots").hide()
        self.OutAnimationInstance.start()
        taskMgr.remove("event selecttarget")

    def hide(self):
        self.OutAnimationInstance.start()
        taskMgr.remove("event selecttarget")

    def setParent(self,parent):
        self.parent = parent

    def destroy(self):
        taskMgr.remove("event selecttarget")

    def getParent(self):
        return self.parent

    @staticmethod
    def getInstance():
        if MenuSelectTarget.instance is None:
            MenuSelectTarget.instance = MenuSelectTarget()

        return MenuSelectTarget.instance
