__author__ = 'ogilp'
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from shimstar.gui.shimcegui import *
from shimstar.core.functions import *
from shimstar.user.user import *
from shimstar.network.netmessage import *
from shimstar.network.networkzoneserver import *
from shimstar.items.junk import *

class MenuLootsInfo(DirectObject):
    instance=None
    def __init__(self):
        self.junk = None
        self.CEGUI = ShimCEGUI.getInstance()
        self.parent = None
        self.lastTicks = 0
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/LootsWindow").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                                         self, 'onCloseClicked')
        self.OutAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/LootsWindow"))
        self.InAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/LootsWindow"))
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/LootsWindow/Open").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                            'onOpen')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/LootsWindow/Destroy").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                            'onDestroy')

    def event(self,task):
        dt = globalClock.getRealTime() - self.lastTicks
        if dt > 1:
            self.lastTicks = globalClock.getRealTime()
            if self.junk in Junk.junkList:
                if self.junk is not None:
                    ship = User.getInstance().getCurrentCharacter().getShip()
                    if ship is not None:
                        ship.lock.acquire()
                        if self.junk.getNode().isEmpty() != True and ship.getNode().isEmpty() != True:
                            distance = calcDistance(self.junk.getNode(),ship.getNode())
                            self.CEGUI.WindowManager.getWindow("HUD/Cockpit/LootsWindow/Distance").setText(str(distance))
                        ship.lock.release()
            else:
                self.junk=None
                self.hide()
        return task.cont

    def onOpen(self,args):
        self.parent.onClickInfo(args)

    def onDestroy(self,args):
        nm = netMessage(C_NETWORK_DESTROY_JUNK)
        nm.addInt(User.getInstance().getId())
        nm.addInt(self.junk.getId())
        NetworkZoneServer.getInstance().sendMessage(nm)

    def setParent(self,parent):
        self.parent=parent

    def setTarget(self,junk):
        self.junk=junk
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/LootsWindow/Name").setText(self.junk.getName() + str(self.junk.getId()))

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
        taskMgr.remove("event loot Info")
        self.junk = None
        MenuLootsInfo.instance = None

    @staticmethod
    def getInstance():
        if MenuLootsInfo.instance is None:
            MenuLootsInfo.instance = MenuLootsInfo()
        return MenuLootsInfo.instance

    @staticmethod
    def isInstantiated():
        if MenuLootsInfo.instance is not None:
            return True
        return False