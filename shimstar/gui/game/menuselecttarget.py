__author__ = 'ogilp'
from shimstar.gui.shimcegui import *
from shimstar.npc.npc import *
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from shimstar.items.junk import *
from shimstar.user.user import *
from shimstar.gui.game.follower import *
from shimstar.user.character.character import *

class MenuSelectTarget(DirectObject):
    instance = None
    def __init__(self):
        self.junk = None
        self.CEGUI = ShimCEGUI.getInstance()
        self.checked = []
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

    def emptyWindow(self, wndName=""):
        if wndName == "":
            wndName = "HUD/Cockpit/TargetSelect/Panel"
        if self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount() > 0:
            for itChild in range(self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount()):
                wnd = self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildAtIdx(0)
                self.CEGUI.WindowManager.getWindow(wndName).getContentPane().removeChildWindow(wnd)
                wnd.destroy()

    def event(self,task):
        try:
            self.panel = self.CEGUI.WindowManager.getWindow("HUD/Cockpit/TargetSelect/Panel")
            dt = globalClock.getRealTime() - self.lastTicks
            if dt > 1:
                self.emptyWindow()
                self.lastTicks = globalClock.getRealTime()
                i=0
                listOfObj = []
                for n in NPC.getListOfNpc():
                    listOfObj.append(n)
                for j in Junk.junkList:
                    listOfObj.append(j)
                for u in User.listOfUser:
                    if User.getInstance().getId() != u:
                        listOfObj.append(User.listOfUser[u].getCurrentCharacter())
                for n in listOfObj:
                    label = self.CEGUI.WindowManager.createWindow("Shimstar/Button",
                                                              "HUD/Cockpit/TargetSelect/Panel/labeltgt=" + str(n.getName()+ str(n.getId())))
                    label.setProperty("UnifiedAreaRect",
                                  "{{0.1,0},{" + str(0.05 + 0.17*i )+ ",0},{1.0,0},{" + str(0.21+0.17*i) +",0}}")
                    label.setText(n.getName())
                    label.setFont("Brassiere-s")
                    if isinstance(n,Junk):
                        if len(n.getItems())==0:
                            label.setText("[colour='99999900']" + str(n.getName()))
                    self.panel.addChildWindow(label)
                    ck = self.CEGUI.WindowManager.createWindow("TaharezLook/Checkbox","HUD/Cockpit/TargetSelect/Panel/rb=" + str(n.getName() + str(n.getId())))
                    ck.setProperty("UnifiedAreaRect",
                                   "{{0.05,0},{" + str(0.05 + 0.17*i) +",0},{0.2,0},{" + str(0.21 + 0.17*i) +",0}}")
                    ck.setUserString("name", n.getName() + str(n.getId()))
                    ck.setUserData(n)
                    if (n.getName()+str(n.getId())) in self.checked:
                        ck.setSelected(True)
                    ck.subscribeEvent(PyCEGUI.Checkbox.EventCheckStateChanged, self,'onCheck')
                    self.panel.addChildWindow(ck)
                    i+=1
        except:
            print sys.exc_info()[0]

        return task.cont

    def setTarget(self,tgt):
        self.checked=[]
        self.checked.append(tgt.getName() + str(tgt.getId()))

    def onCheck(self,args):
        if args.window.isSelected():
            self.checked=[]
            self.checked.append(args.window.getUserString("name"))
            newTarget = args.window.getUserData()
            if isinstance(newTarget,NPC):
                self.parent.changeTarget(newTarget.getShip(),True,newTarget)
                Follower.getInstance().setTarget(newTarget.getShip().getNode())
            elif isinstance(newTarget,Character):
                self.parent.changeTarget(newTarget.getShip(),True,newTarget)
                Follower.getInstance().setTarget(newTarget.getShip().getNode())
            else:
                self.parent.changeTarget(newTarget,True,newTarget)
                Follower.getInstance().setTarget(newTarget.getNode())
        else:
            if args.window.getUserString("name") in self.checked:
                self.checked.remove(args.window.getUserString("name"))
                Follower.getInstance().setTarget(None)
                self.parent.changeTarget(None,True,None)

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
