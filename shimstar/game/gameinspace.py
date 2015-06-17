import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.interval.LerpInterval import LerpPosInterval
from pandac.PandaModules import CollisionTraverser, CollisionNode
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import CollisionHandlerQueue, CollisionRay

from shimstar.core.shimconfig import *
from shimstar.core.functions import *
from shimstar.gui.core.configuration import *
from shimstar.world.zone.zone import *
from shimstar.user.user import *
from shimstar.game.gamestate import *
from shimstar.game.explosion import *
from shimstar.gui.game.follower import *
from shimstar.gui.core.menututo import *
# from shimstar.gui.core.inventory import *
import PyCEGUI
from shimstar.gui.shimcegui import *
# from shimstar.game.particleEngine import *


class GameInSpace(DirectObject, threading.Thread):
    instance = None

    def __init__(self):
        print "GameInSpace::__init__"
        threading.Thread.__init__(self)
        self.Terminated = False
        self.lock = threading.Lock()
        self.volume = 1
        self.CEGUI = ShimCEGUI.getInstance()
        self.ceGuiRootWindow = None
        self.stopThread = False
        self.currentZone = Zone.getInstance()
        GameInSpace.instance = None
        self.keysDown = {}
        self.historyKey = {}
        self.expTask = []
        self.doubleQTicks = 0
        self.doubleDTicks = 0
        self.doubleZTicks = 0
        self.doubleSTicks = 0
        self.target = None
        self.customIm = {}
        self.startQtyMineral = 0
        self.mousebtn = [0, 0, 0]
        self.enableKey(None)
        base.camera.setPos(0, -600, 50)
        GameState.getInstance().setState(C_PLAYING)
        self.ticksRenderUI = 0
        self.updateInput = 0
        self.isShooting = False
        self.listOfExplosion = []
        ship = User.getInstance().getCurrentCharacter().getShip()
        ship.setInvisible()
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.7, 0.7, 0.7, 1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)
        self.shooting = False
        self.mouseToUpdate = False
        self.speedup = 0
        self.pointerLookingAt = loader.loadModelCopy(
            shimConfig.getInstance().getConvRessourceDirectory() + "models/arrow")
        self.pointerLookingAt.reparentTo(render)
        self.pointerLookingAt.hide()
        self.picker = CollisionTraverser()  # Make a traverser
        base.cTrav = CollisionTraverser()
        self.hdlCollider = CollisionHandlerEvent()
        self.hdlCollider.addInPattern('into-%in')
        self.hdlCollider.addOutPattern('outof-%in')
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = base.camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pq = CollisionHandlerQueue()  # Make a handler
        self.pickerNode.addSolid(self.pickerRay)
        self.picker.addCollider(self.pickerNP, self.pq)
        taskMgr.add(self.pickmouse, "pickmouse")
        self.pointToLookAt = Vec3(0, 0, 0)

        # ~ self.textObject = OnscreenText(text = '0,0,0',pos =(0,0),fg=(1,1,1,1))


    def enableKey(self, args):
        self.accept("i", self.keyDown, ['i', 1])
        self.accept("m", self.keyDown, ['m', 1])
        self.accept("j", self.keyDown, ['j', 1])
        self.accept("v", self.keyDown, ['v', 1])
        self.accept("enter", self.keyDown, ['enter', 1])
        self.accept("z", self.keyDown, ['z', 1])
        self.accept("z-up", self.keyDown, ['z', 0])
        self.accept("q", self.keyDown, ['q', 1])
        self.accept("q-up", self.keyDown, ['q', 0])
        self.accept("s", self.keyDown, ['s', 1])
        self.accept("s-up", self.keyDown, ['s', 0])
        self.accept("d", self.keyDown, ['d', 1])
        self.accept("d-up", self.keyDown, ['d', 0])
        self.accept("a", self.keyDown, ['a', 1])
        self.accept("a-up", self.keyDown, ['a', 0])
        self.accept("x", self.keyDown, ['x', 1])
        self.accept("x-up", self.keyDown, ['x', 0])
        self.accept("g", self.keyDown, ['g', 1])
        self.accept("g-up", self.keyDown, ['g', 0])
        self.accept("v", self.keyDown, ['v', 1])
        self.accept("v-up", self.keyDown, ['v', 0])
        self.accept("w", self.keyDown, ['w', 1])
        self.accept("w-up", self.keyDown, ['w', 0])
        self.accept("c", self.keyDown, ['c', 1])
        self.accept("c-up", self.keyDown, ['c', 0])
        self.accept("lcontrol", self.keyDown, ['lcontrol', 1])
        self.accept("lcontrol-up", self.keyDown, ['lcontrol', 0])
        self.accept("t", self.keyDown, ['t', 1])
        self.accept("t-up", self.keyDown, ['t', 0])
        self.accept("n", self.keyDown, ['n', 1])
        self.accept("n-up", self.keyDown, ['n', 0])
        self.accept("k", self.keyDown, ['k', 1])
        self.accept("k-up", self.keyDown, ['k', 0])
        self.accept("f12", self.keyDown, ['f12', 1])
        self.accept("f12-up", self.keyDown, ['f12', 0])
        self.accept("escape", self.quitGame, )
        self.accept("CLOSEF4", self.quitGame, )
        self.accept("mouse1", self.setMouseBtn, [0, 1])
        self.accept("mouse1-up", self.setMouseBtn, [0, 0])
        self.accept("mouse2", self.setMouseBtn, [1, 1])
        self.accept("mouse2-up", self.setMouseBtn, [1, 0])
        self.accept("mouse3", self.setMouseBtn, [2, 1])
        self.accept("mouse3-up", self.setMouseBtn, [2, 0])
        self.accept("wheel_up", self.speedUp, [1])
        self.accept("wheel_down", self.speedUp, [-1])
        self.ambientSound = base.loader.loadSfx(
            shimConfig.getInstance().getConvRessourceDirectory() + self.currentZone.getMusic())
        self.ambientSound.setLoop(True)
        self.ambientSound.setVolume(shimConfig.getInstance().getAmbientVolume())
        self.ambientSound.play()
        #~ self.setupRocketUI()
        self.setupUI()
        self.CEGUI.enable()

    def speedUp(self, sp):
        ship = User.getInstance().getCurrentCharacter().getShip()
        if ship != None:
            ship.lock.acquire()
            if ship.engine != None:
                acc = ship.engine.getAcceleration()
                self.speedup += acc * sp
            ship.lock.release()

    def quitGame(self):
        #~ self.stopThread=True
        #~ GameState.getInstance().setState(C_QUIT)
        self.InQuitAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("root/Quit").moveToFront()

    def setMouseBtn(self, btn, value):
        self.mousebtn[btn] = value

    def ignoreKey(self, args):
        self.ignore("i")
        self.ignore("z")
        self.ignore("j")
        self.ignore("v")
        self.ignore("z-up")
        self.ignore("x")
        self.ignore("x-up")
        self.ignore("q")
        self.ignore("q-up")
        self.ignore("g")
        self.ignore("g-up")
        self.ignore("s")
        self.ignore("s-up")
        self.ignore("d")
        self.ignore("d-up")
        self.ignore("a")
        self.ignore("a-up")
        self.ignore("w")
        self.ignore("w-up")
        self.ignore("c")
        self.ignore("c-up")
        self.ignore("lcontrol")
        self.ignore("lcontrol-up")
        self.ignore("t")
        self.ignore("t-up")
        self.ignore("v")
        self.ignore("v-up")
        self.ignore("f12")
        self.ignore("f12-up")
        self.ignore("escape")
        self.ignore("enter")
        self.ignore("mouse1")
        self.ignore("mouse1-up")
        self.ignore("mouse2")
        self.ignore("mouse2-up")
        self.ignore("mouse3")
        self.ignore("mouse3-up")
        self.ignore("CLOSEF4")
        for key in self.keysDown.keys():
            del self.keysDown[key]
            self.historyKey[key] = 0

    def map3dToAspect2d(self, node, point):
        """Maps the indicated 3-d point (a Point3), which is relative to
        the indicated NodePath, to the corresponding point in the aspect2d
        scene graph. Returns the corresponding Point3 in aspect2d.
        Returns None if the point is not onscreen. """
        # Convert the point to the 3-d space of the camera
        p3 = base.cam.getRelativePoint(node, point)
        # Convert it through the lens to render2d coordinates
        p2 = Point2()

        if not base.camLens.project(p3, p2):
            return None

        r2d = Point3(p2[0], 0, p2[1])

        # And then convert it to aspect2d coordinates
        a2d = aspect2d.getRelativePoint(render2d, r2d)

        return a2d

    def setInvisibleInfoTarget(self):
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship").setVisible(False)
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid").setVisible(False)
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station").setVisible(False)

    def changeTarget(self, obj):
        #~ self.setInvisibleInfoTarget()
        #~ if isinstance(obj,Ship):
        #~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship").setVisible(True)
        #~ elif isinstance(obj,Station):
        #~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station").setVisible(True)
        #~ elif isinstance(obj,Asteroid):
        #~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid").setVisible(True)
        if isinstance(obj, Station):
            self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget/home").show()
            self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget/Mining").hide()
            self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Reticle/ennemyHullBar").hide()
        elif isinstance(obj, Ship):
            self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget/home").hide()
            self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget/Mining").hide()
            self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Reticle/ennemyHullBar").show()
        elif isinstance(obj, Asteroid):
            self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget/home").hide()
            self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Reticle/ennemyHullBar").hide()
            self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget/Mining").show()

    def renderTarget(self, dt):
        if self.target != None and self.target.getNode().isEmpty() != True:
            if isinstance(self.target, Ship):
                self.target.getLock().acquire()
                #~ print dt
                ###Ecran Info
                #~ if self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship").isVisible()!=True:
                #~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship").setVisible(True)
                if dt > 0.05:
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Name").setText(self.target.getName())
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Distance").setText(
                        str(self.calcDistance(self.target.node)))
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Img").setProperty("BackgroundImage",
                                                                                           "set:ShimstarImageset image:" + self.target.name)
                #~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Img").setProperty("HoverImage", "set:" + self.target.name + " image:full_image")
            ###Reticule de suivi de la cible ou point rouge sur le bord
            elif isinstance(self.target, Station):
                if self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship").isVisible() == True:
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship").setVisible(False)
            pos = self.map3dToAspect2d(render, self.target.getNode().getPos(render))
            if pos != None:
                if self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").isVisible() == False:
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").setVisible(True)
                pos2 = self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").getPosition()
                x2 = pos2.d_x.d_offset
                z2 = pos2.d_y.d_offset
                x = pos.getX()
                z = pos.getZ()
                height = base.win.getYSize()
                width = base.win.getXSize()
                ratio = float(width) / float(height)
                z = height / 2 * z * -1
                x = (x * width / (ratio * 2))
                vec = PyCEGUI.PyCEGUI.UVector2(PyCEGUI.PyCEGUI.UDim(0, x), PyCEGUI.PyCEGUI.UDim(0, z))
                pos = self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").setPosition(vec)
                if isinstance(self.target, Ship):
                    prctHull = 0
                    if self.target != None:
                        prctHull, currentHull, maxHull = self.target.getPrcentHull()
                    #~ print "gameinspace::rendertarget " + str(prctHull)
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Reticle/ennemyHullBar").setProgress(prctHull)
            else:
                if self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").isVisible() == True:
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").setVisible(False)

                #~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship/Img").setProperty("BackgroundImage", "set:TempImageset image:full_image")
            if isinstance(self.target, Ship):
                self.target.getLock().release()
        elif self.target != None and self.target.getNode().isEmpty() == True:
            self.target = None
        else:
            if self.CEGUI.WindowManager.getWindow(
                    "HUD/Cockpit/ReticleTarget") != None and self.CEGUI.WindowManager.getWindow(
                    "HUD/Cockpit/ReticleTarget").isVisible() == True:
                self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").setVisible(False)
            if self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship").isVisible() == True:
                self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship").setVisible(False)

    def pickmouse(self, task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())

            self.picker.traverse(render)
            self.pointToLookAt = None
            objPicked = None
            if self.pq.getNumEntries() > 0:
                self.pq.sortEntries()  #this is so we get the closest object
                for p in self.pq.getEntries():
                    nn = p.getIntoNodePath()
                    tabNode = str(nn).split("/")
                    objFromRender = None
                    try:
                        objFromRender = render.find(tabNode[1]).node()
                    except:
                        print "gameinspace::pickMouse : render seems to be empty"
                    if objFromRender != None:
                        className = objFromRender.getTag("classname")
                        if className == "asteroid":
                            objPicked = Asteroid.getAsteroidById(int(objFromRender.getTag("id")))
                            self.pointToLookAt = objPicked.getPos()
                            break
                        elif className == "ship":
                            objPicked = Ship.getShipById(int(objFromRender.getTag("id")))
                            ship = User.getInstance().getCurrentCharacter().getShip()
                            if ship != None and objPicked != None and objPicked.getId() != ship.getId():
                                self.pointToLookAt = objPicked.getPointerToGo().getPos()
                                break
                            else:
                                objPicked = None
                        elif className == "station":
                            objPicked = Station.getStationById(int(objFromRender.getTag("id")))
                            break
            if self.mousebtn[2] == 1:
                if objPicked != None:
                    Follower.getInstance().setTarget(objPicked.getNode())
                    #~ rocketTarget.getInstance().showWindow(newTarget.getShip())
                    self.target = objPicked
                    self.changeTarget(objPicked)
        return task.cont

    def showShipName(self):
        Ship.lock.acquire()
        for s in Ship.listOfShip:
            ship = Ship.listOfShip[s]
            nShip = ship.node
            if ship != None and nShip != None and nShip.isEmpty() != True:
                textObject = ship.getTextObject()
                distance = 0
                if ship != User.getInstance().getCurrentCharacter().ship:
                    distance = self.calcDistance(ship.node)
                if textObject == None:
                    textObject = OnscreenText(text=ship.owner.name, pos=(-0.95, 0.95), scale=0.03, fg=(1, 1, 1, 1))
                    ship.setTextObject(textObject)
                if abs(distance) < 2000:
                    if nShip != None and nShip.isEmpty() != True and isInView(nShip) != True:
                        textObject.hide()
                    else:
                        textObject.show()
                        pos = self.map3dToAspect2d(render, nShip.getPos(render))
                        if pos != None:
                            x = pos.getX()
                            z = pos.getZ()
                            distFactor = float(float(distance) / float(300))
                            if distFactor > 0:
                                z += float(float(0.1) / float(distFactor))
                            else:
                                z += 0.1
                            textObject.setPos(x, z)
                else:
                    textObject.hide()
            elif ship != None:
                textObject = ship.getTextObject()
                if textObject != None and textObject.isEmpty() != True:
                    textObject.hide()

        Ship.lock.release()

    def clickOnHUD(self, args):
        if args.button == PyCEGUI.MouseButton.LeftButton:
            self.shooting = True

    def releaseClickOnHUD(self, args):
        if args.button == PyCEGUI.MouseButton.LeftButton:
            self.shooting = False

    def setupUI(self):
        self.CEGUI.SchemeManager.create("TaharezLook.scheme")
        self.CEGUI.SchemeManager.create("shimstar.scheme")
        self.CEGUI.System.setDefaultTooltip("TaharezLook/Tooltip")
        self.CEGUI.System.setDefaultMouseCursor("ShimstarImageset", "MouseArrow")
        self.CEGUI.System.setDefaultFont("Brassiere-m")
        self.ceGuiRootWindow = self.CEGUI.WindowManager.loadWindowLayout("ingame.layout")
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Reticle").setMouseInputPropagationEnabled(True)
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit").subscribeEvent(PyCEGUI.Window.EventMouseButtonDown, self,
                                                                         'evtMouseRootClicked')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit").subscribeEvent(PyCEGUI.Window.EventMouseButtonUp, self,
                                                                         'evtMouseRootReleased')
        #~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Chat/NewMessage").subscribeEvent(PyCEGUI.Window.EventActivated,self,'ignoreKey')
        #~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Chat/NewMessage").subscribeEvent(PyCEGUI.Window.EventDeactivated,self,'enableKey')
        self.CEGUI.WindowManager.getWindow("root/Quit/CancelQuit").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                                  'onCancelQuitGame')
        self.CEGUI.WindowManager.getWindow("root/Quit/Quit").subscribeEvent(PyCEGUI.PushButton.EventClicked, self,
                                                                            'onQuiGameConfirmed')
        #~ self.CEGUI.WindowManager.getWindow("HUD/Menubar/Menu/AutoPopup/Inventaire").subscribeEvent(PyCEGUI.MenuItem.EventClicked, self, 'onMenuInventaire')
        #~ self.CEGUI.WindowManager.getWindow("HUD/Menubar/Menu/AutoPopup/Missions").subscribeEvent(PyCEGUI.MenuItem.EventClicked, self, 'onMenuMissions')
        self.CEGUI.WindowManager.getWindow("HUD/Menubar/Menu/AutoPopup/Quitter").subscribeEvent(
            PyCEGUI.MenuItem.EventClicked, self, 'onMenuQuitter')
        self.CEGUI.WindowManager.getWindow("HUD/Menubar/Menu/AutoPopup/Inventaire").subscribeEvent(
            PyCEGUI.MenuItem.EventClicked, self, 'onMenuInventaire')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Reticle").subscribeEvent(PyCEGUI.Window.EventMouseButtonDown,
                                                                                 self, 'clickOnHUD')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").subscribeEvent(
            PyCEGUI.Window.EventMouseButtonDown, self, 'clickOnHUD')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit").subscribeEvent(PyCEGUI.Window.EventMouseButtonDown, self,
                                                                         'clickOnHUD')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Reticle").subscribeEvent(PyCEGUI.Window.EventMouseButtonUp,
                                                                                 self, 'releaseClickOnHUD')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").subscribeEvent(
            PyCEGUI.Window.EventMouseButtonUp, self, 'releaseClickOnHUD')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit").subscribeEvent(PyCEGUI.Window.EventMouseButtonUp, self,
                                                                         'releaseClickOnHUD')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget/info").subscribeEvent(
            PyCEGUI.Window.EventMouseButtonUp, self, 'onClickInfo')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget/home").subscribeEvent(
            PyCEGUI.Window.EventMouseButtonUp, self, 'onClickEnterStation')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget/Mining").subscribeEvent(
            PyCEGUI.Window.EventMouseButtonUp, self, 'onClickMining')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Mining/Stop").subscribeEvent(PyCEGUI.Window.EventMouseButtonUp,
                                                                                     self, 'onClickStopMining')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Mining/Start").subscribeEvent(PyCEGUI.Window.EventMouseButtonUp,
                                                                                      self, 'onClickStartMining')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget/info").subscribeEvent(
            PyCEGUI.Window.EventMouseButtonUp, self, 'onClickInfo')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Asteroid").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                                  self, 'onCloseClicked')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Station").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                                 self, 'onCloseClicked')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Ship").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                              self, 'onCloseClicked')
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Mining").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,
                                                                                self, 'onCloseClicked')
        self.CEGUI.WindowManager.getWindow("Inventaire").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked, self,
                                                                        'onCloseClicked')
        #~ customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImageset", "background/backmenuconnect.jpg", "images")
        #~ self.customIm = self.CEGUI.ImageSetManager.createFromImageFile("TempImagesettgt", "/ships/ship1.png", "images")
        self.OutQuitAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InQuitAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutQuitAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("root/Quit"))
        self.InQuitAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("root/Quit"))

        self.OutMiningAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InMiningAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutMiningAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Mining"))
        self.InMiningAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Mining"))

        # menuInventory.getInstance('inventaire').setParent(self)
        # menuInventory.getInstance('inventaire').setObj(User.getInstance().getCurrentCharacter().getShip())

        self.OutInventaireAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
        self.InInventaireAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
        self.OutInventaireAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Inventaire"))
        self.InInventaireAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Inventaire"))

        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/hullLabel").setFont("Brassiere-s")
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit").show()
        self.CEGUI.WindowManager.getWindow("Station").hide()
        self.CEGUI.System.setGUISheet(self.ceGuiRootWindow)

        customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImagesetship1", "/ships/ship1.png",
                                                                        "images")
        customImageset.setNativeResolution(PyCEGUI.Size(64, 64))
        customImageset.setAutoScalingEnabled(False)
        self.customIm['ship1'] = customImageset
        customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImagesetspiderdrone",
                                                                        "/ships/spiderdrone.png", "images")
        customImageset.setNativeResolution(PyCEGUI.Size(64, 64))
        customImageset.setAutoScalingEnabled(False)
        self.customIm['spiderdrone'] = customImageset

    #~ self.OutInventaireAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
    #~ self.InInventaireAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
    #~ self.OutInventaireAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Inventaire"))
    #~ self.InInventaireAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Inventaire"))
    #~ self.CEGUI.WindowManager.getWindow("Inventaire").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,self,'inventoryCloseClicked')
    #~ menuInventory.getInstance('inventaire').setParent(self)
    #~ menuInventory.getInstance('inventaire').setObj(user.instance.getCurrentCharacter().getShip())
    #~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit").addChildWindow(self.CEGUI.WindowManager.getWindow("Inventaire"))
    #~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit").addChildWindow(self.CEGUI.WindowManager.getWindow("InfoItem"))

    def onMenuInventaire(self, args):
        self.InInventaireAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("Inventaire").moveToFront()

    def onClickMining(self, args):
        self.InMiningAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Mining/Stop").hide()
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Mining/Start").show()

    def mining(self, task):
        ship = User.getInstance().getCurrentCharacter().getShip()
        inv = ship.getItemInInventory()
        qty = 0
        for it in inv:
            if it.getTypeItem() == C_ITEM_MINERAL:
                qty = it.getQuantity()
                break
        qtyMined = qty - self.startQtyMineral
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Mining/Current").setText("Minerai recolte : " + str(qtyMined))
        return task.cont

    def onClickStartMining(self, args):
        nm = netMessage(C_NETWORK_START_MINING)
        nm.addInt(User.getInstance().getId())
        nm.addInt(self.target.getId())
        NetworkZoneServer.getInstance().sendMessage(nm)
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Mining/Stop").show()
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Mining/Start").hide()
        ship = User.getInstance().getCurrentCharacter().getShip()
        inv = ship.getItemInInventory()
        for it in inv:
            if it.getTypeItem() == C_ITEM_MINERAL:
                self.startQtyMineral = it.getQuantity()
                break
        taskMgr.add(self.mining, "mining")

    def onClickStopMining(self, args):
        nm = netMessage(C_NETWORK_STOP_MINING)
        nm.addInt(User.getInstance().getId())
        NetworkZoneServer.getInstance().sendMessage(nm)
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Mining/Stop").hide()
        self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Mining/Start").show()
        taskMgr.remove("mining")

    def onClickEnterStation(self, windowEventArgs):
        print "onClickEnterStation " + str(isinstance(self.target, Station))
        if isinstance(self.target, Station) == True:
            GameState.getInstance().setNewZone(self.target.getId())
            User.getInstance().getCurrentCharacter().changeZone()

    def onCloseClicked(self, windowEventArgs):
        if windowEventArgs.window.getName() == "HUD/Cockpit/Mining":
            self.OutMiningAnimationInstance.start()
            self.onClickStopMining(None)
        elif windowEventArgs.window.getName() == "Inventaire":
            self.OutInventaireAnimationInstance.start()
        else:
            windowEventArgs.window.hide()

    def onMenuQuitter(self, args):
        self.InQuitAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("root/Quit").moveToFront()

    def quitGame(self, ):
        self.InQuitAnimationInstance.start()
        self.CEGUI.WindowManager.getWindow("root/Quit").moveToFront()

    def onCancelQuitGame(self, args):
        #~ self.CEGUI.WindowManager.getWindow("root/Quit").hide()
        self.OutQuitAnimationInstance.start()

    def onQuiGameConfirmed(self, args):
        self.stopThread = True
        GameState.getInstance().setState(C_QUIT)

    def onClickInfo(self, args):
        print "info!:!"


    def evtMouseRootClicked(self, args):
        if args.button == PyCEGUI.MouseButton.LeftButton:
            self.setMouseBtn(0, 1)
        elif args.button == PyCEGUI.MouseButton.RightButton:
            self.setMouseBtn(1, 1)
        else:
            self.setMouseBtn(2, 1)

    def evtMouseRootReleased(self, args):
        if args.button == PyCEGUI.MouseButton.LeftButton:
            self.setMouseBtn(0, 0)
        elif args.button == PyCEGUI.MouseButton.RightButton:
            self.setMouseBtn(1, 0)
        else:
            self.setMouseBtn(2, 0)

    def keyDown(self, key, value):
        #~ print "KEYDOWN " + str(key) + "/" + str(value)
        if value == 0:
            if self.keysDown.has_key(key) == True:
                del self.keysDown[key]
                if key == 'q' or key == 'd' or key == 's' or key == 'z' or key == 'a' or key == 'w' or key == "lcontrol":
                    self.historyKey[key] = 0
                if key == 'q':
                    self.historyKey['qq'] = 0
                if key == 'd':
                    self.historyKey['dd'] = 0
                if key == 's':
                    self.historyKey['ss'] = 0
                if key == 'z':
                    self.historyKey['zz'] = 0

        else:
            if self.keysDown.has_key(key) == False:
                if key == 'q' or key == 'd' or key == 's' or key == 'z' or key == 'a' or key == 'w' or key == "lcontrol":
                    self.historyKey[key] = 1
                if key == 'q':
                    dt = globalClock.getRealTime() - self.doubleQTicks
                    if dt < 0.3:
                        self.historyKey['qq'] = 1
                    self.doubleQTicks = globalClock.getRealTime()
                if key == 'd':
                    dt = globalClock.getRealTime() - self.doubleDTicks
                    if dt < 0.3:
                        self.historyKey['dd'] = 1
                    self.doubleDTicks = globalClock.getRealTime()
                if key == 's':
                    dt = globalClock.getRealTime() - self.doubleSTicks
                    if dt < 0.3:
                        self.historyKey['ss'] = 1
                    self.doubleSTicks = globalClock.getRealTime()
                if key == 'z':
                    dt = globalClock.getRealTime() - self.doubleZTicks
                    if dt < 0.3:
                        self.historyKey['zz'] = 1
                    self.doubleZTicks = globalClock.getRealTime()

            self.keysDown[key] = value

    @staticmethod
    def getInstance():
        return GameInSpace.instance

    def destroy(self):
        self.stopThread = True
        GameState.lock.acquire()
        GameState.lock.release()
        GameInstance = None
        self.ambientSound.stop()
        for expl in self.listOfExplosion:
            expl.delete()
        self.ignoreKey(None)
        if self.ceGuiRootWindow != None:
            self.CEGUI.WindowManager.destroyWindow(self.ceGuiRootWindow)
        taskMgr.remove("pickmouse")
        taskMgr.remove("mining")

    def calcDistance(self, targetNode):
        currentDistance = 0
        ship = User.getInstance().getCurrentCharacter().getShip()
        #~ print "gameinSpace::calcDistance " + str(ship.getNode()) + "/" + str(targetNode)
        if ship != None and ship.getNode() != None and targetNode != None and ship.getNode().isEmpty() == False and targetNode.isEmpty() == False:
            posShip = ship.getNode().getPos()
            posItem = targetNode.getPos()
            dx = posShip.getX() - posItem.getX()
            dy = posShip.getY() - posItem.getY()
            dz = posShip.getZ() - posItem.getZ()
            currentDistance = int(round(sqrt(dx * dx + dy * dy + dz * dz), 0))
        return currentDistance

    def getNextTarget(self):
        listOfObj = self.currentZone.getListOfNPC()
        #~ listOfObj+=self.currentZone.getListOfPlayer()
        actualTarget = Follower.getInstance().getTarget()

        found = False
        firstObj = None
        target = None
        for o in listOfObj:
            if found == True:
                target = o
                break
            if firstObj == None:
                firstObj = o
            if o.getShip().getNode() == actualTarget:
                found = True

        if found == False:
            target = firstObj

        if target != None:
            Follower.getInstance().setTarget(target.getShip().getNode())
            #~ rocketTarget.getInstance().showWindow(target.getShip())
            self.target = target.getShip()
            self.changeTarget(self.target)

    def seekNearestTarget(self, typeTarget):
        #~ if typeTarget=="NPC":
        listOfObj = self.currentZone.getListOfNPC() + User.getListOfCharacters(True)
        distanceMax = 10000000
        newTarget = None

        for n in listOfObj:
            distance = self.calcDistance(n.getShip().node)
            if distance < distanceMax:
                distanceMax = distance
                newTarget = n
        if newTarget != None:
            Follower.getInstance().setTarget(newTarget.getShip().getNode())
            #~ rocketTarget.getInstance().showWindow(newTarget.getShip())
            self.target = newTarget.getShip()
            self.changeTarget(self.target)
        #~ print "gameinspace :: seekNearestTArget " + str(self.target)

    def runNewExplosion(self):
        tempMsg = NetworkZoneServer.getInstance().getListOfMessageById(C_NETWORK_EXPLOSION)

        if len(tempMsg) > 0:
            for msg in tempMsg:
                netMsg = msg.getMessage()
                pos = (netMsg[0], netMsg[1], netMsg[2])
                self.listOfExplosion.append(Explosion(render, pos, 20))
                self.expTask.append(taskMgr.add(self.runUpdateExplosion, "explosionTask" + str(Explosion.nbExplo - 1)))
                inProgress = len(self.listOfExplosion) - 1
                self.expTask[inProgress].fps = 30  #set framerate
                self.expTask[inProgress].obj = self.listOfExplosion[inProgress].getExpPlane()
                self.expTask[inProgress].textures = self.listOfExplosion[inProgress].getexpTexs()
                self.expTask[inProgress].timeFps = self.listOfExplosion[inProgress].getTimeFps()
            NetworkZoneServer.getInstance().removeMessage(msg)

    def runUpdateExplosion(self, task):
        if GameState.getInstance().getState() == C_PLAYING:
            currentFrame = int(task.time * task.fps)
            try:
                task.obj.setTexture(task.textures[currentFrame % len(task.textures)], 1)
                if currentFrame > task.timeFps:
                    tempToDelete = None
                    for expl in self.listOfExplosion:
                        if expl.getName() == task.obj.getName():
                            tempToDelete = expl

                    if tempToDelete != None:
                        self.listOfExplosion.remove(tempToDelete)
                        tempToDelete.delete()

                    self.expTask.remove(task)

                    return Task.done
                else:
                    return Task.cont  #Continue the task indefinitely
            except:
                print "Game::runUpdateExplosion something's wrong here"
                Task.done
        else:
            self.expTask.remove(task)
            return Task.done

    def run(self):
        #~ self.setupUI()
        #~ self.CEGUI.enable()
        mt = MenuTuto.getInstance()
        mt.setCeguiManager(self.CEGUI)

        if shimConfig.getInstance().hasReadTuto(C_MENU_TUTO_SPACE) == False:
            mt.displayTuto(C_MENU_TUTO_SPACE)
            shimConfig.getInstance().readTuto(C_MENU_TUTO_SPACE)
        ship = User.getInstance().getCurrentCharacter().getShip()
        #~ self.PE = ParticleEngine(ship.node, nb=40, ray=30, move = True)
        #~ self.PE.start()
        #~ self.PE.stop()
        #~ self.PE.speed=100
        while not self.stopThread and GameState.getInstance().getState() == C_PLAYING:
            #~ print "here"
            GameState.lock.acquire()
            #~ print "here2"
            ship = User.getInstance().getCurrentCharacter().getShip()
            if ship != None:
                ship.lock.acquire()
                if ship != None:
                    if ship.node.isEmpty() == False:

                        forwardVec = Quat(ship.node.getQuat()).getForward()
                        if ship.isHidden() == True:
                            if ship.node.isEmpty() == False:
                                base.camera.setPos((forwardVec * (1.0)) + ship.node.getPos())
                                base.camera.setHpr(ship.node.getHpr())
                        else:
                            if ship.node.isEmpty() == False:
                                #~ base.camera.setPos((forwardVec*(-200.0))+ ship.node.getPos())
                                mvtCam = (((forwardVec * (-200.0)) + ship.node.getPos()) * 0.20) + (
                                base.camera.getPos() * 0.80)
                                hprCam = ship.node.getHpr() * 0.2 + base.camera.getHpr() * 0.8
                                base.camera.setPos(mvtCam)
                                base.camera.setHpr(hprCam)

                        if globalClock.getRealTime() - self.updateInput > 0.1:
                            self.updateInput = globalClock.getRealTime()
                            #~ posMouseX=0
                            #~ posMouseY=0
                            #~ if self.mousebtn[2]==1:
                            #~ self.mouseToUpdate=True
                            #~ if base.mouseWatcherNode.hasMouse():
                            #~ posMouseX=-base.mouseWatcherNode.getMouseX()
                            #~ posMouseY=base.mouseWatcherNode.getMouseY()
                            #~ absx=abs(posMouseX)
                            #~ absy=abs(posMouseY)
                            #~ ## Trying to get smooth mouse to accelerating mouse
                            #~ if absx>=0:
                            #~ posMouseX*=1
                            #~ elif absx>=0.25 and absx<0.5:
                            #~ posMouseX*=3
                            #~ elif absx>=0.5 and absx<0.75:
                            #~ posMouseX*=3
                            #~ elif absx>=0.75:# and absx<0.9:
                            #~ posMouseX*=9
                            #~ elif absx>=0.9:
                            #~ posMouseX*=4
                            #~ if absy>=0:
                            #~ posMouseY*=1
                            #~ elif absy>0.25 and absy<0.5:
                            #~ posMouseY*=3
                            #~ elif absy>=0.5 and absy<0.75:
                            #~ posMouseY*=3
                            #~ elif absy>=0.75:# and absy<0.9:
                            #~ posMouseY*=9
                            #~ elif absy>=0.9:
                            #~ posMouseY*=27

                            #~ nm=netMessage(C_NETWORK_CHARACTER_MOUSE)
                            #~ nm.addUInt(User.getInstance().getId())
                            #~ nm.addFloat(posMouseX)
                            #~ nm.addFloat(posMouseY)
                            #~ NetworkZoneServer.getInstance().sendMessage(nm)
                            #~ self.speedup=0
                            #~ elif self.mouseToUpdate==True:
                            #~ self.mouseToUpdate=False
                            #~ nm=netMessage(C_NETWORK_CHARACTER_MOUSE)
                            #~ nm.addUInt(User.getInstance().getId())
                            #~ nm.addFloat(posMouseX)
                            #~ nm.addFloat(posMouseY)
                            #~ NetworkZoneServer.getInstance().sendMessage(nm)

                            if len(self.historyKey) > 0:
                                nm = netMessage(C_NETWORK_CHARACTER_KEYBOARD)
                                nm.addInt(User.getInstance().getId())
                                nm.addInt(len(self.historyKey))
                                for key in self.historyKey.keys():
                                    if key == 'q' or key == 'd' or key == 's' or key == 'z' or key == 'a' or key == 'w' or key == 'dd' or key == 'qq' or key == 'ss' or key == 'zz' or key == "lcontrol":
                                        nm.addString(key)
                                        nm.addInt(self.historyKey[key])
                                #~ NetworkZoneUdp.getInstance().sendMessage(nm)
                                NetworkZoneServer.getInstance().sendMessage(nm)

                                self.historyKey.clear()
                            if self.speedup != 0:
                                nm = netMessage(C_NETWORK_CHARACTER_SPEED)
                                nm.addUInt(User.getInstance().getId())
                                nm.addInt(self.speedup)
                                self.speedup = 0
                                NetworkZoneServer.getInstance().sendMessage(nm)

                            if MenuTuto.getInstance().isActiv() == False:

                                if len(self.historyKey) > 0:
                                    nm = netMessage(C_NETWORK_CHARACTER_KEYBOARD)
                                    nm.addUInt(User.getInstance().getId())
                                    nm.addUInt(len(self.historyKey))
                                    for key in self.historyKey.keys():
                                        if key == 'q' or key == 'd' or key == 's' or key == 'z' or key == 'a' or key == 'w' or key == 'dd' or key == 'qq' or key == 'ss' or key == 'zz' or key == "lcontrol":
                                            nm.addString(key)
                                            nm.addUInt(self.historyKey[key])
                                    #~ NetworkZoneUdp.getInstance().sendMessage(nm)
                                    NetworkZoneServer.getInstance().sendMessage(nm)

                                self.historyKey.clear()

                                if self.shooting:
                                    #~ if self.mousebtn[0]==1:
                                    #~ print "shot"
                                    if ship.shot():
                                        self.pointerLookingAt.setPos(ship.getPos())
                                        if self.pointToLookAt is not None:
                                            self.pointerLookingAt.lookAt(self.pointToLookAt)
                                        else:
                                            if base.mouseWatcherNode.hasMouse():
                                                x = base.mouseWatcherNode.getMouseX()
                                                y = base.mouseWatcherNode.getMouseY()
                                                t1 = Point3()
                                                t2 = Point3()
                                                ret = base.camLens.extrude(Point2(x, y), t1, t2)
                                                t2 = t2 / 100
                                                t2relative = render.getRelativePoint(camera, t2)
                                                self.pointerLookingAt.lookAt(t2relative)
                                        nm = netMessage(C_NETWORK_CHAR_SHOT)
                                        nm.addUInt(ship.getOwner().getUserId())
                                        nm.addUInt(ship.getOwner().getId())
                                        nm.addFloat(ship.getPos().getX())
                                        nm.addFloat(ship.getPos().getY())
                                        nm.addFloat(ship.getPos().getZ())
                                        nm.addFloat(self.pointerLookingAt.getQuat().getR())
                                        nm.addFloat(self.pointerLookingAt.getQuat().getI())
                                        nm.addFloat(self.pointerLookingAt.getQuat().getJ())
                                        nm.addFloat(self.pointerLookingAt.getQuat().getK())
                                        NetworkZoneServer.getInstance().sendMessage(nm)

                                if self.keysDown.has_key('t'):
                                    if (self.keysDown['t'] != 0):
                                        self.seekNearestTarget("NPC")
                                        self.keysDown['t'] = 0

                                if self.keysDown.has_key('v'):
                                    if (self.keysDown['v'] != 0):
                                        self.getNextTarget()
                                        self.keysDown['v'] = 0
                                if self.keysDown.has_key('k'):
                                    if (self.keysDown['k'] != 0):
                                        self.volume -= 0.1
                                        self.keysDown['k'] = 0
                                        self.ambientSound.setVolume(self.volume)
                                        print  "self.volume " + str(self.volume)
                                if self.keysDown.has_key('f12'):
                                    del self.keysDown['f12']
                                    if ship.isHidden() == True:
                                        ship.setVisible()
                                    else:
                                        ship.setInvisible()
                    ship.lock.release()
            User.lock.acquire()
            for usr in User.listOfUser:
                User.listOfUser[usr].getCurrentCharacter().run()
            User.lock.release()

            NPC.lock.acquire()
            listOfNpc = NPC.getListOfNpc()
            for n in listOfNpc:
                n.run()
            NPC.lock.release()

            Bullet.lock.acquire()
            for b in Bullet.listOfBullet:
                Bullet.listOfBullet[b].move()
            Bullet.lock.release()

            self.runNewExplosion()

            dt = globalClock.getRealTime() - self.ticksRenderUI
            self.renderTarget(dt)

            if dt > 0.05:
                md = base.win.getPointer(0)
                x = md.getX()
                z = md.getY()
                height = base.win.getYSize()
                width = base.win.getXSize()
                x = x - (width / 2)
                z = z - (height / 2)

                vec = PyCEGUI.PyCEGUI.UVector2(PyCEGUI.PyCEGUI.UDim(0, x), PyCEGUI.PyCEGUI.UDim(0, z))
                pos = self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Reticle").setPosition(vec)

                self.ticksRenderUI = globalClock.getRealTime()
                if ship != None:
                    #~ self.textObject.setText(str(ship.node.getPos()))
                    ship.lock.acquire()
                    prctHull, currentHull, maxHull = ship.getPrcentHull()
                    self.showShipName()
                    #~ print str(prctHull ) + "/" + str(currentHull)
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/HullBar").setProgress(prctHull)
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/HullBar").setTooltipText(
                        str(currentHull) + "/" + str(maxHull))
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/hullLabel").setText(
                        "Coque : " + str(prctHull * 100) + "%")
                    prctSpeed, currentPoussee, maxSpeed = ship.getPrcentSpeed()
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/speedBar").setProgress(prctSpeed)
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/speedBar").setTooltipText(
                        str(currentPoussee) + "/" + str(maxSpeed))
                    self.CEGUI.WindowManager.getWindow("HUD/Cockpit/LabelSpeed").setText(
                        "Vitesse : " + str(prctSpeed * 100) + "%")
                    #~ print prctSpeed
                    #~ self.PE.speed=prctSpeed*100*5
                    ship.lock.release()

            GameState.lock.release()