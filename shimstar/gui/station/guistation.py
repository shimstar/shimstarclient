# -*- coding: utf-8 -*- 
import sys, os

import PyCEGUI
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from pandac.PandaModules import *
from shimstar.gui.shimcegui import *
# import shimstar.gui.core.iteminfo
# from shimstar.gui.core.inventory import *
from shimstar.gui.station.guistationship import *
from shimstar.core.shimconfig import *
from shimstar.user.user import *
from shimstar.world.zone.zone import *
from shimstar.game.gamestate import *
# from shimstar.npc.npcinstation import *
from shimstar.items.itemfactory import *
from shimstar.npc.npcinstation import *
from shimstar.gui.station.guistationshop import *
from shimstar.gui.station.guistationinventory import *
from shimstar.gui.station.guistationfitting import *

class GuiStation(DirectObject):
    def __init__(self):
        self.usrLoaded = False
        msg = netMessage(C_NETWORK_ASKING_CHAR)
        msg.addUInt(User.getInstance().getId())
        NetworkMainServer.getInstance().sendMessage(msg)
        self.idZone = User.getInstance().getCurrentCharacter().getIdZone()
        self.zone = Zone(self.idZone)
        self.ambientSound = base.loader.loadSfx(
            shimConfig.getInstance().getConvRessourceDirectory() + self.zone.getMusic())
        self.ambientSound.setLoop(True)
        self.ambientSound.setVolume(shimConfig.getInstance().getAmbientVolume())
        self.ambientSound.play()
        self.listOfImageSet = {}
        self.CEGUI = ShimCEGUI.getInstance()
        self.name = self.zone.getName()
        self.back = self.zone.getEgg()
        self.resolutionList = []
        self.setupUI()
        taskMgr.add(self.event, "event reader", -40)
        self.accept("escape", self.quitGame, )
        self.CEGUI.enable()
        GameState.getInstance().setState(C_PLAYING)
        self.buttonSound = base.loader.loadSfx(
            shimConfig.getInstance().getConvRessourceDirectory() + "sounds/Button_press3.ogg")
        self.buttonSound.setVolume(shimConfig.getInstance().getSoundVolume())
        self.buttonSound2 = base.loader.loadSfx(
            shimConfig.getInstance().getConvRessourceDirectory() + "sounds/Button_press1.ogg")
        self.buttonSound2.setVolume(shimConfig.getInstance().getSoundVolume())

    # def destroy(self):
    #     taskMgr.remove("event reader")
    #     self.ambientSound.stop()

    def event(self, arg):
        if self.usrLoaded == False:
            tempMsg = NetworkMainServer.getInstance().getListOfMessageById(C_NETWORK_CURRENT_CHAR_INFO)
            if len(tempMsg) > 0:
                for msg in tempMsg:
                    netMsg = msg.getMessage()
                    ch = User.getInstance().getCurrentCharacter()
                    ch.setShip(netMsg[0], netMsg[1], netMsg[2], False)
                    nbInv = netMsg[3]
                    ship = ch.getShip()
                    compteur = 4
                    for i in range(nbInv):
                        typeItem = netMsg[compteur]
                        compteur += 1
                        templateId = netMsg[compteur]
                        compteur += 1
                        idItem = netMsg[compteur]
                        compteur += 1
                        it = itemFactory.getItemFromTemplateType(templateId, typeItem)
                        it.setId(idItem)
                        quantity = netMsg[compteur]
                        compteur += 1
                        if typeItem == C_ITEM_MINERAL:
                            it.setQuantity(quantity)
                        ship.addItemInInventory(it)

                    nbSlot = netMsg[compteur]
                    ship.removeTemplateSlots()
                    compteur += 1
                    for n in range(nbSlot):
                        idSlot = netMsg[compteur]
                        tempSlot = Slot(None, idSlot)
                        compteur += 1
                        nbTypes = netMsg[compteur]
                        compteur += 1
                        for t in range(nbTypes):
                            idType = netMsg[compteur]
                            compteur += 1
                            tempSlot.appendTypes(idType)
                        typeItem = netMsg[compteur]
                        compteur += 1
                        templateItem = netMsg[compteur]
                        compteur += 1
                        idItem = netMsg[compteur]
                        compteur += 1
                        enabledItem = True if netMsg[compteur]==1 else False
                        compteur += 1
                        if idItem != 0:
                            it = itemFactory.getItemFromTemplateType(templateItem, typeItem)
                            it.setId(idItem)
                            it.setEnabled(enabledItem)
                            tempSlot.setItem(it)
                        ship.addSlot(tempSlot)
                    nbDialog = netMsg[compteur]
                    compteur += 1
                    for i in range(nbDialog):
                        ch.appendDialogs(netMsg[compteur])
                        compteur += 1

                    nbMission = netMsg[compteur]
                    compteur += 1
                    for i in range(nbMission):
                        idMission = netMsg[compteur]
                        compteur += 1
                        statusMission = netMsg[compteur]
                        compteur += 1
                    # tempMission=Mission(idMission)
                    # tempMission.setStatus(statusMission)
                    # ch=User.getInstance().getCurrentCharacter().addMission(tempMission)

                    nbItemInvStation = netMsg[compteur]
                    compteur += 1
                    ch.setInvStation([])
                    for invS in range(nbItemInvStation):
                        typeItem=netMsg[compteur]
                        template=netMsg[compteur+1]
                        idItem=netMsg[compteur+2]
                        nb=netMsg[compteur+3]
                        compteur += 4
                        it = itemFactory.getItemFromTemplateType(template, typeItem)
                        it.setId(idItem)
                        it.setNb(nb)
                        # self.inventory.append(it)
                        ch.appendInvStation(it)
                    coin = netMsg[compteur]
                    ch.setCoin(coin)
                    NetworkMainServer.getInstance().removeMessage(msg)
                    self.usrLoaded = True
                # menuInventory.getInstance('soute').setObj(User.getInstance().getCurrentCharacter().getShip())
        return Task.cont

    def quitGame(self, ):
        self.InQuitAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("root/Quit").moveToFront()

    def onCancelQuitGame(self, args):
        self.OutQuitAnimationInstance.start()

    def onQuiGameConfirmed(self, args):
        GameState.getInstance().setState(C_QUIT_MENU)

    def loadResolution(self):
        if len(self.resolutionList) == 0:
            info = base.pipe.getDisplayInformation()
            listB = self.CEGUI.WindowManager.getWindow("Options/OptionVideo/Resolution")
            listOfResolution=[]
            for idx in range(info.getTotalDisplayModes()):
                width = info.getDisplayModeWidth(idx)
                height = info.getDisplayModeHeight(idx)
                bits = info.getDisplayModeBitsPerPixel(idx)

                if bits == 32:
                    if (str(width) + "*" + str(height)) not in listOfResolution:
                        item = PyCEGUI.ListboxTextItem(str(width) + "*" + str(height))
                        self.resolutionList.append(item)
                        item.setSelectionColours(PyCEGUI.colour(1, 1, 1, 1))
                        item.setSelectionBrushImage("TaharezLook", "ListboxSelectionBrush")
                        listB.addItem(item)
                        listOfResolution.append(str(width) + "*" + str(height))

    def chooseResolution(self):
        listB = self.CEGUI.WindowManager.getWindow("Options/OptionVideo/Resolution")
        item = listB.getFirstSelectedItem()
        if item is not None:
            shimConfig.getInstance().setResolution(item.getText())
            shimConfig.getInstance().saveConfig()
            resolution=item.getText().split("*")
            wp = WindowProperties()
            wp.setSize(int(resolution[0]), int(resolution[1])) # there will be more resolutions
            wp.setFullscreen(True)
            base.win.requestProperties(wp)

    def ButtonClicked(self, windowEventArgs):
        self.buttonSound.play()
        if (windowEventArgs.window.getName() == "Station/Menus/Sortir"):
            GameState.getInstance().setNewZone(self.zone.getExitZone())
            User.getInstance().getCurrentCharacter().changeZone()
        elif (windowEventArgs.window.getName() == "Station/Menus/Options"):
            self.InOptionsAnimationInstance.start()
            self.CEGUI.WindowManager.getWindow("Options").moveToFront()
        elif (windowEventArgs.window.getName() == "Options/Video"):
            self.OutOptionsAnimationInstance.start()
            self.loadResolution()
            self.InOptionsVideoAnimationInstance.start()
            self.CEGUI.WindowManager.getWindow("Options/OptionVideo").moveToFront()
        elif (windowEventArgs.window.getName() == "Options/OptionVideo/Choose"):
            self.chooseResolution()
            self.OutOptionsVideoAnimationInstance.start()
        elif (windowEventArgs.window.getName() == "Station/Menus/Personnel"):
            self.InNPCAnimationInstance.start()
            self.showNPC()
            self.OutDialogAnimationInstance.start()
            self.CEGUI.WindowManager.getWindow("Station/Personnel").moveToFront()
        elif (windowEventArgs.window.getName() == "Station/Menus/Vaisseau"):
            GuiStationFitting.getInstance(self.root).show()
        elif (windowEventArgs.window.getName() == "Station/Menus/Inventaire"):
            GuiStationInventory.getInstance(self.root).show()

    def destroy(self):
        self.ignore("escape")
        taskMgr.remove("event reader")
        if GuiStationInventory.isInstantiated():
            GuiStationInventory.getInstance(self.root).destroy()
        if chooseItemShip.isInstantiated():
            chooseItemShip.getInstance(None,None).destroy()
        if GuiStationShop.isInstantiated():
            GuiStationShop.getInstance(self.root).destroy()
        if GuiStationFitting.isInstantiated():
            GuiStationFitting.getInstance(self.root).destroy()
        self.CEGUI.WindowManager.destroyWindow(self.root)
        self.ambientSound.stop()
        # GuiStationShop.getInstance().hide()

    def setupUI(self):
        #  Chargement des sch?s
        self.CEGUI.SchemeManager.create("TaharezLook.scheme")
        self.CEGUI.SchemeManager.create("shimstar.scheme")

        self.CEGUI.System.setDefaultMouseCursor("ShimstarImageset", "MouseArrow")
        self.CEGUI.System.setDefaultFont("Brassiere-m")
        self.root = self.CEGUI.WindowManager.loadWindowLayout("ingame.layout")
        customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImagesetBckStation",
                                                                        "background/" + self.back, "images")
        self.CEGUI.WindowManager.getWindow("Station/Background").setProperty("BackgroundImage",
                                                                             "set:TempImagesetBckStation image:full_image")
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit").hide()
        self.CEGUI.WindowManager.getWindow("Station").show()
        self.CEGUI.WindowManager.getWindow("Station/Name").setText(self.name)
        self.CEGUI.System.setGUISheet(self.root)
        self.CEGUI.WindowManager.getWindow("Station/Menus/Sortir").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                                  'ButtonClicked')
        self.CEGUI.WindowManager.getWindow("Station/Menus/Personnel").subscribeEvent(PyCEGUI.PushButton.EventClicked,
                                                                                     self, 'ButtonClicked')
        self.CEGUI.WindowManager.getWindow("Station/Menus/Vaisseau").subscribeEvent(PyCEGUI.PushButton.EventClicked,
                                                                                    self, 'ButtonClicked')
        self.CEGUI.WindowManager.getWindow("Station/Menus/Inventaire").subscribeEvent(PyCEGUI.PushButton.EventClicked,
                                                                                      self, 'ButtonClicked')
        self.CEGUI.WindowManager.getWindow("Station/Menus/Options").subscribeEvent(PyCEGUI.PushButton.EventClicked,
                                                                                   self, 'ButtonClicked')

        self.CEGUI.WindowManager.getWindow("Options/Video").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                           'ButtonClicked')
        self.CEGUI.WindowManager.getWindow("Options/OptionVideo/Choose").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                           'ButtonClicked')



        self.CEGUI.WindowManager.getWindow("root/Quit/CancelQuit").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                                  'onCancelQuitGame')
        self.CEGUI.WindowManager.getWindow("root/Quit/Quit").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                            'onQuiGameConfirmed')

        self.CEGUI.WindowManager.getWindow("Station/Personnel").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                               self, 'closeClicked')
        self.CEGUI.WindowManager.getWindow("Inventaire").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked, self,
                                                                        'closeClicked')

        self.CEGUI.WindowManager.getWindow("Station/Dialog").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked, self,
                                                                            'closeClicked')
        self.CEGUI.WindowManager.getWindow("Options/OptionVideo").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked, self,
                                                                            'closeClicked')

        self.CEGUI.WindowManager.getWindow("Station/Background").subscribeEvent(PyCEGUI.FrameWindow.EventMouseClick,
                                                                                self, 'backgroundClicked')

        self.CEGUI.WindowManager.getWindow("root/Skills").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked, self,
                                                                         'closeClicked')

        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionAccept").subscribeEvent(
            PyCEGUI.PushButton.EventClicked, self, 'acceptMission')
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionCancel").subscribeEvent(
            PyCEGUI.PushButton.EventClicked, self, 'cancelMission')
        self.CEGUI.WindowManager.getWindow("Station/Dialog/MissionEnd").subscribeEvent(PyCEGUI.PushButton.EventClicked,
                                                                                       self, 'endMission')

        self.OutQuitAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InQuitAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutQuitAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("root/Quit"))
        self.InQuitAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("root/Quit"))

        self.OutNPCAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InNPCAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutNPCAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Personnel"))
        self.InNPCAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Personnel"))



        self.OutDialogAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InDialogAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutDialogAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Dialog"))
        self.InDialogAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Station/Dialog"))

        self.OutOptionsAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InOptionsAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutOptionsAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Options"))
        self.InOptionsAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Options"))

        self.OutOptionsVideoAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InOptionsVideoAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutOptionsVideoAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Options/OptionVideo"))
        self.InOptionsVideoAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Options/OptionVideo"))


    def backgroundClicked(self, evt):
        self.CEGUI.WindowManager.getWindow("Station/Background").moveToBack()


    def closeClicked(self, windowEventArgs):
        if windowEventArgs.window.getName() == "Station/Personnel":
            self.OutNPCAnimationInstance.start()
        elif windowEventArgs.window.getName() == "Station/Dialog":
            self.OutDialogAnimationInstance.start()
        elif windowEventArgs.window.getName() == "Options/OptionVideo":
            self.OutOptionsVideoAnimationInstance.start()

    def emptyNPCWindow(self):
        if self.CEGUI.WindowManager.getWindow("Station/Personnel/Container").getContentPane().getChildCount() > 0:
            for itChild in range(
                    self.CEGUI.WindowManager.getWindow("Station/Personnel/Container").getContentPane().getChildCount()):
                wnd = self.CEGUI.WindowManager.getWindow("Station/Personnel/Container").getContentPane().getChildAtIdx(
                    0)
                self.CEGUI.WindowManager.getWindow("Station/Personnel/Container").getContentPane().removeChildWindow(
                    wnd)
                wnd.destroy()

    def showNPC(self):
        self.emptyNPCWindow()
        listOfNpc = NPCInStation.getListOfNPCByStation(self.idZone)
        i = 0
        for n in listOfNpc:
            npc = NPCInStation.getNPCById(n)
            button = self.CEGUI.WindowManager.createWindow("Shimstar/ImageButton",
                                                           "Station/Personnel/npc=" + str(npc.getName()))

            if self.listOfImageSet.has_key("TempImageset" + str(npc.getFace())) == False:
                customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImageset" + str(npc.getFace()),
                                                                                "/faces/" + str(npc.getFace()) + ".png",
                                                                                "images")
                customImageset.setNativeResolution(PyCEGUI.Size(64, 64))
                customImageset.setAutoScalingEnabled(False)
                self.listOfImageSet["TempImageset" + str(npc.getFace())] = customImageset

            button.setProperty("NormalImage", "set:TempImageset" + str(npc.getFace()) + " image:full_image")
            button.setProperty("HoverImage", "set:TempImageset" + str(npc.getFace()) + " image:full_image")
            button.setProperty("PushedImage", "set:TempImageset" + str(npc.getFace()) + " image:full_image")
            button.setProperty("UnifiedAreaRect", "{{" + str(0.10 + 0.25 * i) + ",0},{0.14,0},{" + str(
                0.218 + 0.25 * i) + ",0},{0.268,0}}");
            button.setProperty("UnifiedSize", "{{0,128},{0,128}}")
            button.setUserData(npc)
            button.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'onChooseNpc')
            self.CEGUI.WindowManager.getWindow("Station/Personnel/Container").addChildWindow(button)

            label = self.CEGUI.WindowManager.createWindow("Shimstar/Button",
                                                          "Station/Personnel/labelnpc=" + str(npc.getName()))
            label.setProperty("UnifiedAreaRect",
                              "{{" + str(0.10 + 0.25 * i) + ",0},{0.50,0},{" + str(0.31 + 0.25 * i) + ",0},{0.65,0}}");
            label.setText(npc.getName())
            label.setUserData(npc)
            label.setFont("Brassiere-m")
            label.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'onChooseNpc')
            self.CEGUI.WindowManager.getWindow("Station/Personnel/Container").addChildWindow(label)
            i += 1

    def onChooseNpc(self, args):
        self.buttonSound2.play()
        # self.InDialogAnimationInstance.start()
        # TODO  :: here is commented load of npc dialog
        # self.CEGUI.WindowManager.getWindow("Station/Dialog").moveToFront()
        npcChoosed = args.window.getUserData()
        # self.CEGUI.WindowManager.getWindow("Station/Dialog/Face").setProperty("NormalImage", "set:TempImageset" + str(
        #     npcChoosed.getFace()) + " image:full_image")
        # self.CEGUI.WindowManager.getWindow("Station/Dialog/Face").setProperty("HoverImage", "set:TempImageset" + str(
        #     npcChoosed.getFace()) + " image:full_image")
        # self.CEGUI.WindowManager.getWindow("Station/Dialog/Face").setProperty("PushedImage", "set:TempImageset" + str(
        #     npcChoosed.getFace()) + " image:full_image")
        # self.CEGUI.WindowManager.getWindow("Station/Dialog/Face").setUserData(npcChoosed)
        self.OutNPCAnimationInstance.start()
        # self.loadKeywords(npcChoosed)
        if npcChoosed.getTypeNpc()==C_TYPE_NPC_SHOP:
            # GuiStationShop.getInstance(self.root).setItemInStation(self.inventory)
            GuiStationShop.getInstance(self.root).show()


    def emptyKeywordsWindow(self):
        if self.CEGUI.WindowManager.getWindow("Station/Dialog/Keywords").getContentPane().getChildCount() > 0:
            for itChild in range(
                    self.CEGUI.WindowManager.getWindow("Station/Dialog/Keywords").getContentPane().getChildCount()):
                wnd = self.CEGUI.WindowManager.getWindow("Station/Dialog/Keywords").getContentPane().getChildAtIdx(0)
                self.CEGUI.WindowManager.getWindow("Station/Dialog/Keywords").getContentPane().removeChildWindow(wnd)
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
