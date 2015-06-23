import sys, os
from string import *
import direct.directbase.DirectStart
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from shimstar.user.user import *
from shimstar.world.zone.zone import *
from shimstar.game.gamestate import *
import PyCEGUI
from shimstar.gui.shimcegui import *
from shimstar.core.shimconfig import *


class MenuChooseHeroCegui(DirectObject):
    def __init__(self):
        self.text = []
        self.faces = []
        self.btns = []
        self.currentFace = 0
        self.listOfImageSet = {}
        self.CEGUI = ShimCEGUI.getInstance()
        self.CEGUI.System.setDefaultFont("Brassiere-m")
        self.connectMenu = self.CEGUI.WindowManager.loadWindowLayout("choosecharact.layout")
        self.CEGUI.System.setGUISheet(self.connectMenu)
        taskMgr.add(self.event, "event reader menu choosehero", -40)
        customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImageset",
                                                                        "background/backmenuconnect.jpg", "images")
        self.CEGUI.WindowManager.getWindow("ConnexionBg").setProperty("BackgroundImage",
                                                                      "set:TempImageset image:full_image")
        self.root = self.CEGUI.WindowManager.getWindow("Root")
        self.panel = self.CEGUI.WindowManager.getWindow("ConnexionBg/Panel")
        self.CEGUI.WindowManager.getWindow("ConnexionBg/Previous").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                                  'onPrevious')
        self.CEGUI.WindowManager.getWindow("ConnexionBg/Next").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                              'onNext')
        self.CEGUI.WindowManager.getWindow("ConnexionBg/Create").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                                'onCreateNewHero')
        self.btnNew = self.CEGUI.WindowManager.getWindow("ConnexionBg/new")
        self.btnNew.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'newhero')
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Cancel").subscribeEvent(
            PyCEGUI.PushButton.EventClicked, self, 'closeClicked')
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                                  self, 'closeClicked')
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Play").subscribeEvent(PyCEGUI.PushButton.EventClicked,
                                                                                       self, 'onPlay')
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Delete").subscribeEvent(
            PyCEGUI.PushButton.EventClicked, self, 'onDelete')
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Confirm/Yes").subscribeEvent(
            PyCEGUI.PushButton.EventClicked, self, 'onDeleteConfirmed')
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Confirm/No").subscribeEvent(
            PyCEGUI.PushButton.EventClicked, self, 'onCancelDelete')
        self.OutChooseHeroAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InChooseHeroAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutChooseHeroAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero"))
        self.InChooseHeroAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero"))
        self.OutDeleteAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InDeleteAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutDeleteAnimationInstance.setTargetWindow(
            self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Confirm"))
        self.InDeleteAnimationInstance.setTargetWindow(
            self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Confirm"))
        self.OutFadeChooseHeroAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("FadeOut")
        self.InFadeChooseHeroAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("FadeIn")
        self.OutFadeChooseHeroAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("ConnexionBg/group"))
        self.InFadeChooseHeroAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("ConnexionBg/group"))
        self.OutFadeNewHeroAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("FadeOut")
        self.InFadeNewHeroAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("FadeIn")
        self.OutFadeNewHeroAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("ConnexionBg/new"))
        self.InFadeNewHeroAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("ConnexionBg/new"))
        self.buttonSound = base.loader.loadSfx(
            shimConfig.getInstance().getConvRessourceDirectory() + "sounds/Button_press3.ogg")
        self.buttonSound2 = base.loader.loadSfx(
            shimConfig.getInstance().getConvRessourceDirectory() + "sounds/Button_press1.ogg")
        self.buttonSound.setVolume(shimConfig.getInstance().getSoundVolume())
        self.buttonSound2.setVolume(shimConfig.getInstance().getSoundVolume())
        self.accept("escape", self.quitGame)

        self.loadCharacters()
        self.CEGUI.enable()

    def closeClicked(self, winArgs):
        self.buttonSound.play()
        # ~ self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero").hide()
        self.OutChooseHeroAnimationInstance.start()
        self.InFadeChooseHeroAnimationInstance.start()
        self.InFadeNewHeroAnimationInstance.start()

    def loadImage(self, img):
        if self.listOfImageSet.has_key(img) == False:
            customImageset = self.CEGUI.ImageSetManager.createFromImageFile(img, img, "images")
            customImageset.setNativeResolution(PyCEGUI.Size(32, 32))
            customImageset.setAutoScalingEnabled(False)
            self.listOfImageSet[img] = customImageset

    def loadCharacters(self):
        i = 0
        listOfImageSet = {'titi': 'toto'}
        listOfImageSet.clear()
        self.emptyGroupWindow()

        listOfChar = User.getInstance().getCharacters()
        for ch in listOfChar:
            button = self.CEGUI.WindowManager.createWindow("Shimstar/ImageButton",
                                                           "ConnexionBg/group/btnPersohero=" + str(ch.getId()))
            if listOfImageSet.has_key("TempImageset" + str(ch.getFace())) == False:
                customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImageset" + str(ch.getFace()),
                                                                                "/faces/" + str(ch.getFace()) + ".png",
                                                                                "images")
                customImageset.setNativeResolution(PyCEGUI.Size(64, 64))
                customImageset.setAutoScalingEnabled(False)
                listOfImageSet["TempImageset" + str(ch.getFace())] = customImageset

            button.setProperty("NormalImage", "set:TempImageset" + str(ch.getFace()) + " image:full_image")
            button.setProperty("HoverImage", "set:TempImageset" + str(ch.getFace()) + " image:full_image")
            button.setProperty("PushedImage", "set:TempImageset" + str(ch.getFace()) + " image:full_image")
            button.setProperty("UnifiedAreaRect", "{{" + str(0.10 + 0.15 * i) + ",0},{0.14,0},{" + str(
                0.218 + 0.15 * i) + ",0},{0.268,0}}");
            button.setProperty("UnifiedSize", "{{0,128},{0,128}}")
            button.setUserString("name", ch.getName())
            button.setUserString("face", ch.getFace())
            button.setUserString("id", str(ch.getId()))
            button.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'onChooseHero')
            self.panel.addChildWindow(button)
            label = self.CEGUI.WindowManager.createWindow("Shimstar/Button",
                                                          "ConnexionBg/group/labelPersohero=" + str(ch.getName()))
            label.setProperty("UnifiedAreaRect",
                              "{{" + str(0.10 + 0.15 * i) + ",0},{0.80,0},{" + str(0.21 + 0.15 * i) + ",0},{0.96,0}}");
            label.setText(ch.getName())
            label.setUserString("name", ch.getName())
            label.setUserString("id", str(ch.getId()))
            label.setUserString("face", ch.getFace())
            label.subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'onChooseHero')
            self.panel.addChildWindow(label)
            i += 1


    def quitGame(self, ):
        GameState.getInstance().setState(C_QUIT)

    def emptyGroupWindow(self):
        if self.panel.getContentPane().getChildCount() > 0:
            for itChild in range(self.panel.getContentPane().getChildCount()):
                wnd = self.panel.getContentPane().getChildAtIdx(0)
                if wnd != None:
                    self.panel.getContentPane().removeChildWindow(wnd)
                    wnd.destroy()

                    # ~ @todo

    ### Ajouter la gestion d'un nouveau perso
    def event(self, task):
        temp = NetworkMainServer.getInstance().getListOfMessageById(C_USER_ADD_CHAR)
        if (len(temp) > 0):
            msg = temp[0]
            netMsg = msg.getMessage()
            id = int(netMsg[0])
            name = netMsg[1]
            face = netMsg[2]
            idZone = int(netMsg[3])
            User.getInstance().addCharacter(id, name, face, idZone)
            NetworkMainServer.getInstance().removeMessage(msg)
            self.CEGUI.WindowManager.getWindow("ConnexionBg/Group1").hide()
            self.loadCharacters()

        temp = NetworkMainServer.getInstance().getListOfMessageById(C_USER_DELETE_CHAR)
        if (len(temp) > 0):
            msg = temp[0]
            netMsg = msg.getMessage()
            User.getInstance().deleteCharacter(int(netMsg[0]))
            NetworkMainServer.getInstance().removeMessage(msg)
            self.loadCharacters()
        return task.cont

    def onChooseHero(self, arg):
        self.buttonSound2.play()
        #~ index=find(arg.window.getName(),"hero=")
        #~ idHero=arg.window.getName()[index+5:]
        idHero = arg.window.getUserString("id")
        tempChar = User.getInstance().getCharacterById(int(idHero))
        self.OutFadeChooseHeroAnimationInstance.start()
        self.InChooseHeroAnimationInstance.start()
        self.OutFadeNewHeroAnimationInstance.start()
        #~ self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero").show()
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero").moveToFront()
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero").setText(tempChar.getName())
        #~ tempZone=zone(tempChar.getZone())
        zoneName, zoneType = Zone.getTinyInfosFromZone(int(tempChar.getIdZone()))
        text=""
        if zoneType == 1:
            text = "Zone : " + zoneName
        else:
            if zoneName != None:
                text = "Station : " + zoneName
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Localisation").setText(text)
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Name").setText(tempChar.getName())
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Name").setUserString("id", arg.window.getUserString("id"))

        face = arg.window.getUserString("face")
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Play").setUserString("id", idHero)
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Delete").setUserString("name", idHero)
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Delete").setUserString("id",
                                                                                        arg.window.getUserString("id"))
        img = "faces/" + face + ".png"
        self.loadImage(img)
        s = self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Face")
        s.setProperty("BackgroundImage", "set:" + img + " image:full_image")


    def onPlay(self, winArgs):
        self.buttonSound.play()
        User.getInstance().chooseCharacter(int(winArgs.window.getUserString("id")))
        msg = netMessage(C_NETWORK_USER_CHOOSE_HERO)
        msg.addUInt(User.getInstance().getId())
        msg.addUInt(int(winArgs.window.getUserString("id")))
        NetworkMainServer.getInstance().sendMessage(msg)
        User.getInstance().getCurrentCharacter().changeZone()


    def newhero(self, arg):
        self.buttonSound.play()
        self.CEGUI.WindowManager.getWindow("ConnexionBg/Group1").show()
        directory = shimConfig.getInstance().getRessourceDirectory() + 'datafiles/images/faces'
        for files in os.listdir(directory):
            if files[0] != '.':
                self.faces.append(files)

        if len(self.faces) > 0:
            img = "faces/" + self.faces[0]
            self.loadImage(img)
            s = self.CEGUI.WindowManager.getWindow("ConnexionBg/Face")
            s.setProperty("BackgroundImage", "set:" + img + " image:full_image")
            s.setUserString("file", self.faces[0])


    def onNext(self, args):
        self.buttonSound.play()
        self.currentFace += 1
        if self.currentFace >= len(self.faces):
            self.currentFace = 0
        img = "faces/" + self.faces[self.currentFace]
        self.loadImage(img)
        s = self.CEGUI.WindowManager.getWindow("ConnexionBg/Face")
        s.setProperty("BackgroundImage", "set:" + img + " image:full_image")
        s.setUserString("file", self.faces[self.currentFace])


    def onPrevious(self, args):
        self.buttonSound.play()
        self.currentFace -= 1
        if self.currentFace < 0:
            self.currentFace = len(self.faces) - 1
        img = "faces/" + self.faces[self.currentFace]
        self.loadImage(img)
        s = self.CEGUI.WindowManager.getWindow("ConnexionBg/Face")
        s.setProperty("BackgroundImage", "set:" + img + " image:full_image")
        s.setUserString("file", self.faces[self.currentFace])


    def onCreateNewHero(self, arg):
        self.buttonSound.play()
        face = self.CEGUI.WindowManager.getWindow("ConnexionBg/Face").getUserString('file').split('.')
        name = self.CEGUI.WindowManager.getWindow("ConnexionBg/NameEdit").getText()
        # ~ user.instance.addCharacter(name,face[0])

        msg = netMessage(C_USER_ADD_CHAR)
        msg.addUInt(User.getInstance().getId())
        msg.addString(name)
        msg.addString(face[0])
        #~ print "name" + name + "/" + str(face) + "/" + str(face[0])
        NetworkMainServer.getInstance().sendMessage(msg)
        GameState.getInstance().setState(C_CHOOSE_HERO)
        #~ self.CEGUI.WindowManager.getWindow("ConnexionBg/Group1").hide()
        self.OutChooseHeroAnimationInstance.start()


    def onDelete(self, winArgs):
        self.buttonSound.play()
        self.InDeleteAnimationInstance.start()
        # ~ self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Confirm").show()
        self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Confirm").moveToFront()


    def onCancelDelete(self, winArgs):
        self.buttonSound.play()
        # ~ self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Confirm").hide()
        self.OutDeleteAnimationInstance.start()


    def onDeleteConfirmed(self, winArgs):
        self.buttonSound2.play()
        usrId = User.getInstance().getId()
        heroId = self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Name").getUserString("id")
        msg = netMessage(C_USER_DELETE_CHAR)
        msg.addUInt(User.getInstance().getId())
        msg.addUInt(int(heroId))
        NetworkMainServer.getInstance().sendMessage(msg)
        # ~ network.reference.sendMessage(C_USER_DELETE_CHAR,str(usrId)+"/"+heroId)
        #~ self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero/Confirm").hide()
        self.OutDeleteAnimationInstance.start()
        #~ self.CEGUI.WindowManager.getWindow("ConnexionBg/InfoHero").hide()
        self.OutChooseHeroAnimationInstance.start()
        self.InFadeChooseHeroAnimationInstance.start()
        self.InFadeNewHeroAnimationInstance.start()
        self.loadCharacters()


    def destroy(self):
        self.CEGUI.WindowManager.destroyWindow(self.CEGUI.WindowManager.getWindow("Root"))
        self.ignore("escape")
