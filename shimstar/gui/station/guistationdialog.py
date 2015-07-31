__author__ = 'ogilp'
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from shimstar.npc.npcinstation import *
from shimstar.gui.shimcegui import *
from shimstar.user.user import *
from shimstar.gui.core.iteminfo import *
from shimstar.items.templates.itemtemplate import *

class GuiStationDialog(DirectObject):
    instance = None
    def __init__(self):
        self.npc = None
        self.CEGUI = ShimCEGUI.getInstance()
        self.root = None
        self.setupUI()

    def event(self,task):
        toUpdate=False
        tempMsg = NetworkMainServer.getInstance().getListOfMessageById(C_NETWORK_CHARACTER_BUY_ITEM)
        inv = 1
        if len(tempMsg) > 0:
            for msg in tempMsg:
                netMsg = msg.getMessage()
                typeItem = int(netMsg[0])

                NetworkMainServer.getInstance().removeMessage(msg)
                toUpdate=True


        if toUpdate == True :
            self.emptyInvWindow()
            if inv == 1:
                self.initInvWindow()
            else:
                self.initInvWindow(False)
            self.initAchatWindow()
            self.OutTransAnimationInstance.start()
        return task.cont


    def emptyInvWindow(self, wndName=""):
        if wndName == "":
            wndName = "Station/Dialog/Keywords"
        if self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount() > 0:
            for itChild in range(self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildCount()):
                wnd = self.CEGUI.WindowManager.getWindow(wndName).getContentPane().getChildAtIdx(0)
                for itImg in range(wnd.getChildCount()):
                    imgWnd = wnd.getChildAtIdx(0)
                    wnd.removeChildWindow(imgWnd)
                    self.CEGUI.WindowManager.destroyWindow(imgWnd)
                self.CEGUI.WindowManager.getWindow(wndName).getContentPane().removeChildWindow(wnd)
                self.CEGUI.WindowManager.destroyWindow(wnd)
                wnd.destroy()

    def loadKeywords(self, npcChoosed):
        self.emptyKeywordsWindow()
        i = 0
        listOfReadDialogs = User.getInstance().getCurrentCharacter().getReadDialogs()
        for k in npcChoosed.getListOfKeywords():
            dialog = npcChoosed.getDialogueFromKeyword(k)
            showKeyword = True
            if dialog.getParent() > 0:
                if (dialog.getParent() in listOfReadDialogs) != True:
                    showKeyword = False
            if dialog.getReadOnce() == 1:
                if (dialog.getId() in listOfReadDialogs) == True:
                    showKeyword = False
            if showKeyword == True:
                label = self.CEGUI.WindowManager.createWindow("Shimstar/Button",
                                                              "Station/Dialog/Keywords/keyword" + k + str(i))
                label.setProperty("UnifiedAreaRect",
                                  "{{-0.060259,0},{" + str(0.0237858 + 0.06 * i) + ",0},{0.919381,0},{" + str(
                                      0.0926617 + 0.06 * i) + ",0}}");
                label.setFont("Brassiere-s")
                #~ if dialog.getTypeDialog()==C_DIALOG_TYPE_MISSION:
                #~ label.setText("[colour='FF00FF00']" + k)
                #~ else:
                if dialog.getId() in listOfReadDialogs:
                    label.setText(k)
                else:
                    label.setText("[colour='FFFFAA00']" + k)

                label.setUserData(npcChoosed)
                label.setUserString("keyword", k)
                label.setUserString("idnpc", str(npcChoosed.getId()))
                self.CEGUI.WindowManager.getWindow("Station/Dialog/Keywords").addChildWindow(label)
                label.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'onChooseKeywords')
                i += 1

        for m in npcChoosed.getMissions():
            charMissions = User.getInstance().getCurrentCharacter().getMissions()
            found = False
            statusMission = C_STATEMISSION_DONTHAVE
            for mc in charMissions:
                if mc.getId() == m.getId():
                    found = True
                    statusMission = User.getInstance().getCurrentCharacter().evaluateMission(m.getId(),
                        npcChoosed.getId())
                    break
            dial = m.getPreDialog()
            if dial != None:
                keywords = dial.getKeywords()
                for k in keywords:
                    if statusMission != C_STATEMISSION_FINISHED:
                        label = self.CEGUI.WindowManager.createWindow("Shimstar/Button",
                                                                      "Station/Dialog/Keywords/keyword" + str(k) + str(
                                                                          i))
                        label.setProperty("UnifiedAreaRect",
                                          "{{-0.060259,0},{" + str(0.0237858 + 0.06 * i) + ",0},{0.919381,0},{" + str(
                                              0.0926617 + 0.06 * i) + ",0}}");
                        label.setFont("Brassiere-s")
                        if statusMission == C_STATEMISSION_SUCCESS:
                            label.setText("[colour='FFFFFF00']" + str(keywords[k]))
                        elif statusMission == C_STATEMISSION_INPROGRESS:
                            label.setText("[colour='FFFFAA00']" + str(keywords[k]))
                        else:
                            label.setText("[colour='FF00FF00']" + str(keywords[k]))
                        label.setUserData(npcChoosed)
                        label.setUserString("keyword", "-1")
                        label.setUserString("idnpc", str(npcChoosed.getId()))
                        label.setUserString("mission", str(m.getId()))
                        self.CEGUI.WindowManager.getWindow("Station/Dialog/Keywords").addChildWindow(label)
                        label.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'onChooseKeywords')
                        i += 1

    def onChooseKeywords(self, args):
        npcChoosed = NPCInStation.getNPCById(int(args.window.getUserString("idnpc")))
        keyword = args.window.getUserString("keyword")
        if keyword != "-1":
            dialog = npcChoosed.getDialogueFromKeyword(keyword)
            if dialog != None:
                if User.getInstance().getCurrentCharacter().appendDialogs(dialog.getId()) == True:
                    nm = netMessage(C_NETWORK_APPEND_READ_DIALOG)
                    nm.addUInt(User.getInstance().getId())
                    nm.addUInt(User.getInstance().getCurrentCharacter().getId())
                    nm.addUInt(dialog.getId())
                    NetworkMainServer.getInstance().sendMessage(nm)
                dial = dialog.getText().replace('\\r', '\n')
                dial = dialog.getText().replace('\\n', '\n')
                dial = dialog.getText().replace('\\2n', '\n \n')
                self.CEGUI.WindowManager.getWindow("Station/Dialog/Text").show()
                self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionText").hide()
                self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionRecompense").hide()
                self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionObjectif").hide()
                self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionAccept").hide()
                self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionCancel").hide()
                self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").hide()
                self.CEGUI.WindowManager.getWindow("Station/Dialog/Text").setText(dial)

        else:
            missionId = args.window.getUserString("mission")
            m = npcChoosed.getMission(missionId)
            if m != None:
                self.CEGUI.WindowManager.getWindow("Station/Dialog/Text").hide()
                self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionText").show()
                self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionObjectif").show()
                self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionRecompense").show()
                charMissions = User.getInstance().getCurrentCharacter().getMissions()
                found = False
                statusMission = C_STATEMISSION_DONTHAVE
                for mc in charMissions:
                    if mc.getId() == int(missionId):
                        found = True
                        statusMission = User.getInstance().getCurrentCharacter().evaluateMission(mc.getId(),
                            npcChoosed.getId())
                        break

                if statusMission == C_STATEMISSION_SUCCESS:
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionAccept").hide()
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionCancel").show()
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").show()
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").enable()
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").setText("Terminer")
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").setUserData(npcChoosed)
                    dialog = m.getPostDialog()
                    if dialog != None:
                        dial = dialog.getText().replace('\\2n', '\n \n')
                        dial = dialog.getText().replace('\\1n', '\n')
                        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionText").setText(dial)
                elif found == True:
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionAccept").hide()
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionCancel").show()
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").show()
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").disable()
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").setText(
                        "[colour='FFFF0000']Terminer")
                    dialog = m.getCurrentDialog()
                    if dialog != None:
                        dial = dialog.getText().replace('\\2n', '\n \n')
                        dial = dialog.getText().replace('\\1n', '\n')
                        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionText").setText(dial)
                else:
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionAccept").show()
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionCancel").hide()
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").hide()
                    dialog = m.getPreDialog()
                    if dialog != None:
                        dial = dialog.getText().replace('\2n', '\n \n')
                        dial = dialog.getText().replace('\\1n', '\n')
                        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionText").setText(dial)

                objectifs = m.getObjectifs()

                for o in objectifs:
                    textObj = o.getText()
                    if o.getIdType() == C_OBJECTIF_DESTROY:
                        idItem = o.getIdItem()
                        it = ShimstarItem(idItem)
                        textObj += " : " + str(o.getNbItemCharacter()) + " / " + str(o.getNbItem()) + " " + it.getName()
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionObjectif").setText(textObj)

                self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionAccept").setUserString("mission", missionId)
                self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionCancel").setUserString("mission", missionId)
                self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").setUserString("mission", missionId)

                idEndingNPC = m.getEndingNPC()
                endingNPC = NPCInStation(idEndingNPC)
                stationNpc = Zone(endingNPC.getLocation())
                textRecompense = "Voir pour votre recompense : " + str(
                    endingNPC.getName()) + " a la station " + stationNpc.getName()
                rewards = m.getRewards()
                for r in rewards:
                    if r.getTypeReward() == C_REWARD_COIN:
                        textRecompense += "\n\n           " + str(r.getNb()) + " Credits imperiaux"
                self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionRecompense").setText(textRecompense)

        self.loadKeywords(npcChoosed)

    def hideMissionPanel(self):
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionText").hide()
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionObjectif").hide()
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionRecompense").hide()
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionAccept").hide()
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionCancel").hide()
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").hide()

    def acceptMission(self, windowEventArgs):
        missionId = windowEventArgs.window.getUserString("mission")
        msg = netMessage(C_NETWORK_CHARACTER_ACCEPT_MISSION)
        msg.addUInt(User.getInstance().getId())
        msg.addUInt(int(missionId))
        NetworkMainServer.getInstance().sendMessage(msg)
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionAccept").hide()
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionCancel").show()
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").show()

    def cancelMission(self, windowEventArgs):
        missionId = windowEventArgs.window.getUserString("mission")
        msg = netMessage(C_NETWORK_CHARACTER_CANCEL_MISSION)
        msg.addUInt(User.getInstance().getId())
        msg.addUInt(int(missionId))
        NetworkMainServer.getInstance().sendMessage(msg)
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionAccept").show()
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionCancel").hide()
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").hide()

    def endMission(self, windowEventArgs):
        missionId = windowEventArgs.window.getUserString("mission")
        msg = netMessage(C_NETWORK_CHARACTER_END_MISSION)
        msg.addUInt(User.getInstance().getId())
        msg.addUInt(int(missionId))
        NetworkMainServer.getInstance().sendMessage(msg)
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionAccept").hide()
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionCancel").hide()
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").hide()


    @staticmethod
    def getInstance(root):
        if GuiStationDialog.instance is None:
            GuiStationDialog.instance=GuiStationDialog()
            GuiStationDialog.instance.root = root

        return GuiStationDialog.instance

    @staticmethod
    def isInstantiated():
        if GuiStationDialog.instance is not None:
            return True
        return False

    def buttonSwitch(self,windowArgs):
        if windowArgs.window.getText() == "Inventaire station":
            windowArgs.window.setText("Soute Vaisseau")
            self.emptyInvWindow()
            self.initInvWindow(False)
            self.initAchatWindow()
        else:
            windowArgs.window.setText("Inventaire station")
            self.emptyInvWindow()
            self.initInvWindow(True)
            self.initAchatWindow()

    def setupUI(self):
        self.OutAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Shop"))
        self.InAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Shop"))
        self.OutDialogAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InDialogAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutDialogAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Dialog"))
        self.InDialogAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Dialog"))

        self.CEGUI.WindowManager.getWindow("Station/Shop").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                              self, 'onCloseClicked')
        self.CEGUI.WindowManager.getWindow("Station/Shop/switch").subscribeEvent(PyCEGUI.PushButton.EventClicked,
                                                                                   self, 'buttonSwitch')

    def hide(self):
        self.OutDialogAnimationInstance.start()
        taskMgr.remove("event guishop")

    def destroy(self):
        taskMgr.remove("event guishop")
        GuiStationDialog.instance = None

    def show(self):
        self.InDialogAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("Station/Shop").moveToFront()
        self.emptyInvWindow()
        taskMgr.add(self.event,"event guishop",-40)

    def onCloseClicked(self,args):
        self.hide()