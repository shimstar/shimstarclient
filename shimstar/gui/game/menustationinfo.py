__author__ = 'ogilp'
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from shimstar.gui.shimcegui import *
from shimstar.core.functions import *
from shimstar.user.user import *
from shimstar.network.netmessage import *
from shimstar.network.networkzoneserver import *
from shimstar.world.zone.station import *

class MenuStationInfo(DirectObject):
    instance=None
    def __init__(self):
        self.station = None
        self.CEGUI = ShimCEGUI.getInstance()
        self.parent = None
        self.lastTicks = 0
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                                         self, 'onCloseClicked')
        self.OutAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station"))
        self.InAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station"))
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station/Enter").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                            'onEnter')

    def event(self,task):
        dt = globalClock.getRealTime() - self.lastTicks
        if dt > 0.5:
            self.lastTicks = globalClock.getRealTime()
            maxDistance = 500
            ship = User.getInstance().getCurrentCharacter().getShip()
            if ship is not None:
                ship.lock.acquire()
                if self.station.getNode().isEmpty() != True and ship.getNode().isEmpty() != True:
                    distance = calcDistance(self.station.getNode(),ship.getNode())
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station/Distance").setText("distance : "+ str(distance))


                    if distance > maxDistance:
                        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station/Enter").setText("[colour='FFFF0000'] Entrer" )
                        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station/Enter").disable()
                    else:
                        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station/Enter").setText("Entrer")
                        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station/Enter").enable()
                ship.lock.release()

        return task.cont

    def onEnter(self,args):
        self.parent.onClickEnterStation(args)


    def setParent(self,parent):
        self.parent=parent

    def setTarget(self,sta):
        self.station=sta
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station/Name").setText(self.station.getName() + str(self.station.getId()))
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station/Img").setProperty("BackgroundImage", "set:ShimstarImageset image:" + str(self.station.getImage()))

    def onCloseClicked(self, args):
        self.hide()

    def hide(self):
        self.OutAnimationInstance.start()
        taskMgr.remove("event station Info")

    def show(self):
        self.InAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station").moveToFront()
        taskMgr.add(self.event,"event station Info",-40)

    def destroy(self):
        taskMgr.remove("event station Info")
        self.station = None
        MenuStationInfo.instance = None

    @staticmethod
    def getInstance():
        if MenuStationInfo.instance is None:
            MenuStationInfo.instance = MenuStationInfo()
        return MenuStationInfo.instance

    @staticmethod
    def isInstantiated():
        if MenuStationInfo.instance is not None:
            return True
        return False