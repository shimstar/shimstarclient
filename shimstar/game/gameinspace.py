import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject

from shimstar.core.shimconfig import *
from shimstar.core.functions import *
from shimstar.gui.core.configuration import *
from shimstar.world.zone.zone import *
from shimstar.user.user import *
from shimstar.game.gamestate import *
from shimstar.game.explosion import *
from shimstar.gui.game.follower import *
import PyCEGUI
from shimstar.gui.shimcegui import * 
#~ from shimstar.gui.game.rocketshipinfo import *
#~ from shimstar.gui.game.rockettarget import *


class GameInSpace(DirectObject,threading.Thread):
	instance=None
	def __init__(self):
		print "GameInSpace::__init__"
		threading.Thread.__init__(self)
		self.Terminated = False
		self.CEGUI=ShimCEGUI.getInstance()
		self.ceGuiRootWindow=None
		self.stopThread=False
		self.currentZone=Zone.getInstance()
		GameInSpace.instance = None
		self.keysDown={}
		self.historyKey={}
		self.expTask=[]
		self.target=None
		self.mousebtn = [0,0,0]
		self.enableKey(None)
		base.camera.setPos(0,-600,50)
		GameState.getInstance().setState(C_PLAYING)
		self.ticksRenderUI=0
		self.updateInput=0
		self.listOfExplosion=[]
		ship=User.getInstance().getCurrentCharacter().getShip()
		ship.setInvisible()
		alight = AmbientLight('alight')
		alight.setColor(VBase4(0.7, 0.7, 0.7, 1))
		alnp = render.attachNewNode(alight)
		render.setLight(alnp)
		
	def enableKey(self,args):
		self.accept("i",self.keyDown,['i',1])
		self.accept("m",self.keyDown,['m',1])
		self.accept("j",self.keyDown,['j',1])
		self.accept("v",self.keyDown,['v',1])
		self.accept("enter",self.keyDown,['enter',1])
		self.accept("z",self.keyDown,['z',1])
		self.accept("z-up",self.keyDown,['z',0])
		self.accept("q",self.keyDown,['q',1])
		self.accept("q-up",self.keyDown,['q',0])
		self.accept("s",self.keyDown,['s',1])
		self.accept("s-up",self.keyDown,['s',0])
		self.accept("d",self.keyDown,['d',1])
		self.accept("d-up",self.keyDown,['d',0])
		self.accept("a",self.keyDown,['a',1])
		self.accept("a-up",self.keyDown,['a',0])
		self.accept("x",self.keyDown,['x',1])
		self.accept("x-up",self.keyDown,['x',0])
		self.accept("g",self.keyDown,['g',1])
		self.accept("g-up",self.keyDown,['g',0])
		self.accept("v",self.keyDown,['v',1])
		self.accept("v-up",self.keyDown,['v',0])
		self.accept("w",self.keyDown,['w',1])
		self.accept("w-up",self.keyDown,['w',0])
		self.accept("c",self.keyDown,['c',1])
		self.accept("c-up",self.keyDown,['c',0])
		self.accept("t",self.keyDown,['t',1])
		self.accept("t-up",self.keyDown,['t',0])
		self.accept("n",self.keyDown,['n',1])
		self.accept("n-up",self.keyDown,['n',0])
		self.accept("f12",self.keyDown,['f12',1])
		self.accept("f12-up",self.keyDown,['f12',0])
		self.accept("escape",self.quitGame,)
		self.accept("CLOSEF4",self.quitGame,)
		self.accept("mouse1", self.setMouseBtn, [0, 1])
		self.accept("mouse1-up", self.setMouseBtn, [0, 0])
		self.accept("mouse2", self.setMouseBtn, [1, 1])
		self.accept("mouse2-up", self.setMouseBtn, [1, 0])
		self.accept("mouse3", self.setMouseBtn, [2, 1])
		self.accept("mouse3-up", self.setMouseBtn, [2, 0])
		#~ self.setupRocketUI()
		self.setupUI()
		self.CEGUI.enable() 
		
		
	def quitGame(self):
		#~ self.stopThread=True
		#~ GameState.getInstance().setState(C_QUIT)
		self.InQuitAnimationInstance.start()
		self.CEGUI.WindowManager.getWindow("root/Quit").moveToFront()
		
	def setMouseBtn(self, btn, value):
		self.mousebtn[btn]=value
		
	def ignoreKey(self,args):
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
				self.historyKey[key]=0
				
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
		
	def renderTarget(self):
		#~ print self.target
		if self.target!=None and self.target.getNode().isEmpty()!=True:
			pos=self.map3dToAspect2d(render,self.target.getNode().getPos(render))
			if pos!=None:
				if self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").isVisible()==False:
					self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").setVisible(True)
				pos2= self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").getPosition()
				x2=pos2.d_x.d_offset
				z2=pos2.d_y.d_offset
				x=pos.getX()
				z=pos.getZ()
				z=C_USER_HEIGHT/2*z*-1
				x=(x*C_USER_WIDTH/(C_RATIO*2))
				vec=PyCEGUI.PyCEGUI.UVector2(PyCEGUI.PyCEGUI.UDim(0,x),PyCEGUI.PyCEGUI.UDim(0,z))
				pos= self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").setPosition(vec)
			else:
				if self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").isVisible()==True:
					self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").setVisible(False)
		elif self.target!=None and self.target.getNode().isEmpty()==True:
				self.target=None
		else:
			if self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget")!=None and self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").isVisible()==True:
				self.CEGUI.WindowManager.getWindow("HUD/Cockpit/ReticleTarget").setVisible(False)
				
	def setupUI(self):
		self.CEGUI.SchemeManager.create("TaharezLook.scheme") 
		self.CEGUI.SchemeManager.create("shimstar.scheme") 
		self.CEGUI.System.setDefaultTooltip("TaharezLook/Tooltip")
		self.CEGUI.System.setDefaultMouseCursor("ShimstarImageset", "MouseArrow") 
		self.CEGUI.System.setDefaultFont("Brassiere-m")
		self.ceGuiRootWindow = self.CEGUI.WindowManager.loadWindowLayout("ingame.layout") 
		self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Reticle").setMouseInputPropagationEnabled(True)
		self.CEGUI.WindowManager.getWindow("HUD/Cockpit").subscribeEvent( PyCEGUI.Window.EventMouseButtonDown , self, 'evtMouseRootClicked')
		self.CEGUI.WindowManager.getWindow("HUD/Cockpit").subscribeEvent( PyCEGUI.Window.EventMouseButtonUp , self, 'evtMouseRootReleased')
		#~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Chat/NewMessage").subscribeEvent(PyCEGUI.Window.EventActivated,self,'ignoreKey')
		#~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit/Chat/NewMessage").subscribeEvent(PyCEGUI.Window.EventDeactivated,self,'enableKey')
		self.CEGUI.WindowManager.getWindow("root/Quit/CancelQuit").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'onCancelQuitGame')
		self.CEGUI.WindowManager.getWindow("root/Quit/Quit").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'onQuiGameConfirmed')
		#~ self.CEGUI.WindowManager.getWindow("HUD/Menubar/Menu/AutoPopup/Inventaire").subscribeEvent(PyCEGUI.MenuItem.EventClicked, self, 'onMenuInventaire')
		#~ self.CEGUI.WindowManager.getWindow("HUD/Menubar/Menu/AutoPopup/Missions").subscribeEvent(PyCEGUI.MenuItem.EventClicked, self, 'onMenuMissions')
		self.CEGUI.WindowManager.getWindow("HUD/Menubar/Menu/AutoPopup/Quitter").subscribeEvent(PyCEGUI.MenuItem.EventClicked, self, 'onMenuQuitter')
		self.OutQuitAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
		self.InQuitAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
		self.OutQuitAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("root/Quit"))
		self.InQuitAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("root/Quit"))
		self.CEGUI.WindowManager.getWindow("HUD/Cockpit/hullLabel").setFont("Brassiere-s")
		self.CEGUI.WindowManager.getWindow("HUD/Cockpit").show()
		self.CEGUI.WindowManager.getWindow("Station").hide()
		self.CEGUI.System.setGUISheet(self.ceGuiRootWindow)
		#~ self.OutInventaireAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
		#~ self.InInventaireAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
		#~ self.OutInventaireAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Inventaire"))
		#~ self.InInventaireAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("Inventaire"))
		#~ self.CEGUI.WindowManager.getWindow("Inventaire").subscribeEvent(PyCEGUI.FrameWindow.EventCloseClicked,self,'inventoryCloseClicked')
		#~ menuInventory.getInstance('inventaire').setParent(self)
		#~ menuInventory.getInstance('inventaire').setObj(user.instance.getCurrentCharacter().getShip())
		#~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit").addChildWindow(self.CEGUI.WindowManager.getWindow("Inventaire"))
		#~ self.CEGUI.WindowManager.getWindow("HUD/Cockpit").addChildWindow(self.CEGUI.WindowManager.getWindow("InfoItem"))
				
	#~ def setupRocketUI(self):
		#~ self.context = shimRocketRocket.getInstance().getContext()
		#~ self.background = self.context.LoadDocument('windows/backgroundgame.rml')
		#~ self.background.Show()
		#~ rocketShipInfo.getInstance().showWindow()
		
	def onMenuQuitter(self,args):
		self.InQuitAnimationInstance.start()
		self.CEGUI.WindowManager.getWindow("root/Quit").moveToFront()
		
	def quitGame(self,):
		self.InQuitAnimationInstance.start()
		self.CEGUI.WindowManager.getWindow("root/Quit").moveToFront()
		
	def onCancelQuitGame(self,args):
		#~ self.CEGUI.WindowManager.getWindow("root/Quit").hide()
		self.OutQuitAnimationInstance.start()
		
	def onQuiGameConfirmed(self,args):
		self.stopThread=True
		GameState.getInstance().setState(C_QUIT)
	
	def evtMouseRootClicked(self,args):
		if args.button==PyCEGUI.MouseButton.LeftButton:
			self.setMouseBtn(0, 1)
		elif args.button==PyCEGUI.MouseButton.RightButton:
			self.setMouseBtn(1, 1)
		else:
			self.setMouseBtn(2, 1)
			
	def evtMouseRootReleased(self,args):
		if args.button==PyCEGUI.MouseButton.LeftButton:
			self.setMouseBtn(0, 0)
		elif args.button==PyCEGUI.MouseButton.RightButton:
			self.setMouseBtn(1, 0)
		else:
			self.setMouseBtn(2, 0)
				
	def keyDown(self,key,value):
		if value==0:
			if self.keysDown.has_key(key)==True:
				del self.keysDown[key]
				if key=='q' or key=='d' or key=='s' or key=='z' or key=='a' or key=='w':
					self.historyKey[key]=0
		else:
			if self.keysDown.has_key(key)==False:
				if key=='q' or key=='d' or key=='s' or key=='z' or key=='a' or key=='w':
					self.historyKey[key]=1
			self.keysDown[key]=value
	

		
	@staticmethod
	def getInstance():
		return GameInSpace.instance
		
	def destroy(self):
		GameInstance=None
		for expl in self.listOfExplosion:
			expl.delete()
		self.ignoreKey(None)
		if self.ceGuiRootWindow!=None:
			self.CEGUI.WindowManager.destroyWindow(self.ceGuiRootWindow)
		
	def calcDistance(self,targetNode):
		ship=User.getInstance().getCurrentCharacter().getShip()
		posShip=ship.getNode().getPos()
		posItem=targetNode.getPos()
		dx=posShip.getX()-posItem.getX()
		dy=posShip.getY()-posItem.getY()
		dz=posShip.getZ()-posItem.getZ()
		currentDistance=int(round(sqrt(dx*dx+dy*dy+dz*dz),0))
		return currentDistance
		
	def getNextTarget(self):
		listOfObj=self.currentZone.getListOfNPC()
		listOfObj+=self.currentZone.getListOfPlayer()
		actualTarget=Follower.getInstance().getTarget()
		
		found=False
		firstObj=None
		target=None
		for o in listOfObj:
			if found==True:
				target=o
				break
			if firstObj==None:
				firstObj=o
			if o.getShip().getNode()==actualTarget:
				found=True
				
		if found==False:
			target=firstObj
			
		if target!=None:
			Follower.getInstance().setTarget(target.getShip().getNode())
			#~ rocketTarget.getInstance().showWindow(target.getShip())
			self.target=target.getShip()
		
	def seekNearestTarget(self,typeTarget):
		#~ if typeTarget=="NPC":
		listOfObj=self.currentZone.getListOfNPC() + User.getListOfCharacters(True)
		distanceMax=10000000
		newTarget=None
		
		for n in listOfObj:
			distance=self.calcDistance(n.getShip())
			if distance<distanceMax:
				distanceMax=distance
				newTarget=n
		if newTarget!=None:
			Follower.getInstance().setTarget(newTarget.getShip().getNode())
			#~ rocketTarget.getInstance().showWindow(newTarget.getShip())
			self.target=newTarget.getShip()
		
	def runNewExplosion(self):
		tempMsg=NetworkZoneServer.getInstance().getListOfMessageById(C_NETWORK_EXPLOSION)
		
		if len(tempMsg)>0:
			for msg in tempMsg:
				netMsg=msg.getMessage()
				pos=(netMsg[0],netMsg[1],netMsg[2])
				self.listOfExplosion.append(Explosion(render,pos,20))
				self.expTask.append(taskMgr.add(self.runUpdateExplosion, "explosionTask" + str(Explosion.nbExplo-1)))
				inProgress=len(self.listOfExplosion)-1
				self.expTask[inProgress].fps = 30                                 #set framerate
				self.expTask[inProgress].obj = self.listOfExplosion[inProgress].getExpPlane()
				self.expTask[inProgress].textures = self.listOfExplosion[inProgress].getexpTexs()
				self.expTask[inProgress].timeFps = self.listOfExplosion[inProgress].getTimeFps()			
			NetworkZoneServer.getInstance().removeMessage(msg)
		
	def runUpdateExplosion(self, task):		
		if GameState.getInstance().getState()==C_PLAYING:
			currentFrame = int(task.time * task.fps)
			try:
				task.obj.setTexture(task.textures[currentFrame % len(task.textures)], 1)
				if currentFrame>task.timeFps:
					tempToDelete=None
					for expl in self.listOfExplosion:
						if expl.getName()==task.obj.getName():
							tempToDelete=expl
						
					if tempToDelete!=None:
						self.listOfExplosion.remove(tempToDelete)
						tempToDelete.delete()
						
					self.expTask.remove(task)
							
					return Task.done
				else:
					return Task.cont          #Continue the task indefinitely
			except:
				print "Game::runUpdateExplosion something's wrong here"
				Task.done
		else:
			self.expTask.remove(task)
			return Task.done
		
	def run(self):
		while not self.stopThread and GameState.getInstance().getState()==C_PLAYING:
			ship=User.getInstance().getCurrentCharacter().getShip()
			if ship!=None:
				if ship.node.isEmpty()==False:
					forwardVec=Quat(ship.node.getQuat()).getForward()
					if ship.isHidden()==True:
						if ship.node.isEmpty()==False:
							base.camera.setPos((forwardVec*(1.0))+ ship.node.getPos())
							base.camera.setHpr(ship.node.getHpr())
					else:
						if ship.node.isEmpty()==False:
						#~ base.camera.setPos((forwardVec*(-200.0))+ ship.node.getPos())
							mvtCam = (((forwardVec*(-200.0)) + ship.node.getPos()) * 0.20) + (base.camera.getPos() * 0.80)
							hprCam = ship.node.getHpr()*0.2 + base.camera.getHpr()*0.8
							base.camera.setPos(mvtCam)
							base.camera.setHpr(hprCam)
					
					if globalClock.getRealTime()-self.updateInput>0.1:
						self.updateInput=globalClock.getRealTime()
						if len(self.historyKey)>0:
							nm=netMessage(C_NETWORK_CHARACTER_KEYBOARD)
							nm.addInt(User.getInstance().getId())
							nm.addInt(len(self.historyKey))
							for key in self.historyKey.keys():
								if key=='q' or key=='d' or key=='s' or key=='z' or key=='a' or key=='w':
									nm.addString(key)
									nm.addInt(self.historyKey[key])
							#~ NetworkZoneUdp.getInstance().sendMessage(nm)
							NetworkZoneServer.getInstance().sendMessage(nm)
						
						self.historyKey.clear()
						
						if self.mousebtn[0]==1:
							if ship.shot()==True:
								nm=netMessage(C_NETWORK_CHAR_SHOT)
								nm.addInt(ship.getOwner().getUserId())
								nm.addInt(ship.getOwner().getId())
								nm.addFloat(ship.getPos().getX())
								nm.addFloat(ship.getPos().getY())
								nm.addFloat(ship.getPos().getZ())
								nm.addFloat(ship.getQuat().getR())
								nm.addFloat(ship.getQuat().getI())
								nm.addFloat(ship.getQuat().getJ())
								nm.addFloat(ship.getQuat().getK())
								#~ NetworkZoneUdp.getInstance().sendMessage(nm)
								NetworkZoneServer.getInstance().sendMessage(nm)
						
						if self.keysDown.has_key('t'):
							if (self.keysDown['t']!=0):
								self.seekNearestTarget("NPC")
								self.keysDown['t']=0
								
						if self.keysDown.has_key('v'):
							if (self.keysDown['v']!=0):
								self.getNextTarget()
								self.keysDown['v']=0
								
						if self.keysDown.has_key('f12'):
							del self.keysDown['f12']
							if ship.isHidden()==True:
								ship.setVisible()
							else:
								ship.setInvisible()
					
			User.lock.acquire()
			for usr in User.listOfUser:
				User.listOfUser[usr].getCurrentCharacter().run()
			User.lock.release()
			
			NPC.lock.acquire()
			listOfNpc=NPC.getListOfNpc()
			for n in listOfNpc:
				n.run()
			NPC.lock.release()
			
			Bullet.lock.acquire()
			for b in Bullet.listOfBullet:
				Bullet.listOfBullet[b].move()
			Bullet.lock.release()
			
			self.runNewExplosion()
			
			self.renderTarget()
			
			dt=globalClock.getRealTime()-self.ticksRenderUI
			if dt>0.1:
				if ship!=None:
					prctHull,currentHull,maxHull=ship.getPrcentHull()
				#~ print str(prctHull ) + "/" + str(currentHull)
				self.CEGUI.WindowManager.getWindow("HUD/Cockpit/HullBar").setProgress(prctHull)
				self.CEGUI.WindowManager.getWindow("HUD/Cockpit/HullBar").setTooltipText(str(currentHull) + "/" + str(maxHull))
				self.CEGUI.WindowManager.getWindow("HUD/Cockpit/hullLabel").setText("Coque : " + str(prctHull*100) + "%")
			