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

class MenuAsteroidInfo(DirectObject):
    instance=None
    def __init__(self):
        self.asteroid = None
        self.CEGUI = ShimCEGUI.getInstance()
        self.parent = None
        self.lastTicks = 0
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                                         self, 'onCloseClicked')
        self.OutAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid"))
        self.InAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid"))
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid/Miner").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                            'onMining')

    def event(self,task):
        dt = globalClock.getRealTime() - self.lastTicks
        if dt > 0.5:
            self.lastTicks = globalClock.getRealTime()

            ship = User.getInstance().getCurrentCharacter().getShip()
            if ship is not None:
                ship.lock.acquire()
                if self.asteroid.getNode().isEmpty() != True and ship.getNode().isEmpty() != True:
                    distance = calcDistance(self.asteroid.getNode(),ship.getNode())
                    maxDistance = -1
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid/Distance").setText("distance : "+ str(distance))
                    if ship is not None :
                        listOfMining = ship.hasItems(C_ITEM_MINING)
                        for min in listOfMining:
                            maxDistance = min.getDistance()

                    if distance > maxDistance:
                        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid/Miner").setText("[colour='FFFF0000'] Miner" )
                        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid/Miner").disable()
                    else:
                        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid/Miner").setText("Miner")
                        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid/Miner").enable()
                ship.lock.release()

        return task.cont

    def onMining(self,args):
        self.parent.onClickMining(args)


    def setParent(self,parent):
        self.parent=parent

    def setTarget(self,ast):
        self.asteroid=ast
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid/Name").setText(self.asteroid.getName() + str(self.asteroid.getId()))
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid/Img").setProperty("BackgroundImage", "set:ShimstarImageset image:" + str(self.asteroid.getTemplateName()))

    def onCloseClicked(self, args):
        self.hide()

    def hide(self):
        self.OutAnimationInstance.start()
        taskMgr.remove("event asteroid Info")

    def show(self):
        self.InAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid").moveToFront()
        taskMgr.add(self.event,"event asteroid Info",-40)

    def destroy(self):
        taskMgr.remove("event asteroid Info")
        self.asteroid = None
        MenuAsteroidInfo.instance = None

    @staticmethod
    def getInstance():
        if MenuAsteroidInfo.instance is None:
            MenuAsteroidInfo.instance = MenuAsteroidInfo()
        return MenuAsteroidInfo.instance

    @staticmethod
    def isInstantiated():
        if MenuAsteroidInfo.instance is not None:
            return True
        return False