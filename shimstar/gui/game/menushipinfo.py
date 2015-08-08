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

class MenuShipInfo(DirectObject):
    instance=None
    def __init__(self):
        self.getImg = None
        self.CEGUI = ShimCEGUI.getInstance()
        self.parent = None
        self.lastTicks = 0
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                                         self, 'onCloseClicked')
        self.OutAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship"))
        self.InAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship"))


    def event(self,task):
        dt = globalClock.getRealTime() - self.lastTicks
        if dt > 0.5:
            self.lastTicks = globalClock.getRealTime()

            ship = User.getInstance().getCurrentCharacter().getShip()
            if ship is not None:
                ship.lock.acquire()
                if self.ship.getNode().isEmpty() != True and ship.getNode().isEmpty() != True:
                    distance = calcDistance(self.ship.getNode(),ship.getNode())
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Distance").setText("distance : "+ str(distance))

                ship.lock.release()

            prctHull, currentHull, maxHull = self.ship.getPrcentHull()
            self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Hullpoints").setProgress(prctHull)
            self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Hullpoints").setTooltipText(
                str(currentHull) + "/" + str(maxHull))

            prctShield, currentShield, maxShield = self.ship.getPrcentShield()
            if maxShield > 0:
                self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Shield").show()
                self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Shield").setProgress(prctShield)
                self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Shield").setTooltipText(
                    str(currentShield) + "/" + str(maxShield))
            else:
                self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Shield").hide()

        return task.cont

    def setParent(self,parent):
        self.parent=parent

    def setTarget(self,ship):
        self.ship=ship
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Name").setText(self.ship.getName() + str(self.ship.getId()))
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Img").setProperty("BackgroundImage", "set:ShimstarImageset image:" + str(self.ship.getImg()))

    def onCloseClicked(self, args):
        self.hide()

    def hide(self):
        self.OutAnimationInstance.start()
        taskMgr.remove("event ship Info")

    def show(self):
        self.InAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship").moveToFront()
        taskMgr.add(self.event,"event ship Info",-40)

    def destroy(self):
        taskMgr.remove("event ship Info")
        self.ship = None
        MenuShipInfo.instance = None

    @staticmethod
    def getInstance():
        if MenuShipInfo.instance is None:
            MenuShipInfo.instance = MenuShipInfo()
        return MenuShipInfo.instance

    @staticmethod
    def isInstantiated():
        if MenuShipInfo.instance is not None:
            return True
        return False