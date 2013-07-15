import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject

from shimstar.world.zone.zone import *
from shimstar.user.user import *
from shimstar.game.gamestate import *
from shimstar.gui.game.follower import *

class GameInSpace(DirectObject,threading.Thread):
	instance=None
	def __init__(self):
		threading.Thread.__init__(self)
		self.Terminated = False
		self.stopThread=False
		self.currentZone=Zone(User.instance.getCurrentCharacter().getIdZone())
		GameInSpace.instance = None
		self.keysDown={}
		self.historyKey={}
		self.mousebtn={}
		self.enableKey(None)
		base.camera.setPos(0,-600,50)
		GameState.getInstance().setState(C_PLAYING)
		
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
		self.accept("w",self.keyDown,['w',1])
		self.accept("w-up",self.keyDown,['w',0])
		self.accept("c",self.keyDown,['c',1])
		self.accept("c-up",self.keyDown,['c',0])
		self.accept("t",self.keyDown,['t',1])
		self.accept("t-up",self.keyDown,['t',0])
		self.accept("n",self.keyDown,['n',1])
		self.accept("n-up",self.keyDown,['n',0])
		self.accept("escape",self.quitGame,)
		self.accept("CLOSEF4",self.quitGame,)
		self.accept("mouse2", self.setMouseBtn, [1, 1])
		self.accept("mouse2-up", self.setMouseBtn, [1, 0])
		self.accept("mouse3", self.setMouseBtn, [2, 1])
		self.accept("mouse3-up", self.setMouseBtn, [2, 0])
		
	def quitGame(self):
		self.stopThread=True
		GameState.getInstance().setState(C_QUIT)
		
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
		self.ignore("escape")
		self.ignore("enter")
		self.accept("mouse2", self.setMouseBtn, [1, 1])
		self.accept("mouse2-up", self.setMouseBtn, [1, 0])
		self.accept("mouse3", self.setMouseBtn, [2, 1])
		self.accept("mouse3-up", self.setMouseBtn, [2, 0])
		self.ignore("CLOSEF4")
		for key in self.keysDown.keys():
				del self.keysDown[key]
				self.historyKey[key]=0
				
				
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
		self.ignoreKey(None)
		
	def calcDistance(self,targetNode):
		ship=User.getInstance().getCurrentCharacter().getShip()
		posShip=ship.getNode().getPos()
		posItem=targetNode.getPos()
		dx=posShip.getX()-posItem.getX()
		dy=posShip.getY()-posItem.getY()
		dz=posShip.getZ()-posItem.getZ()
		currentDistance=int(round(sqrt(dx*dx+dy*dy+dz*dz),0))
		return currentDistance
		
	def seekNearestTarget(self,typeTarget):
		if typeTarget=="NPC":
			listOfObj=self.currentZone.getListOfNPC()
		print listOfObj
		distanceMax=10000000
		newTarget=None
		for n in listOfObj:
			distance=self.calcDistance(n.getShip())
			if distance<distanceMax:
				distanceMax=distance
				newTarget=n
		if newTarget!=None:
			Follower.getInstance().setTarget(newTarget.getShip().getNode())
		print newTarget
		
	def run(self):
		Zone.getInstance().start()
		while not self.stopThread:
			ship=User.getInstance().getCurrentCharacter().getShip()
			forwardVec=Quat(ship.node.getQuat()).getForward()
			base.camera.setPos((forwardVec*(-200.0))+ ship.node.getPos())
			base.camera.setHpr(ship.node.getHpr())
			if len(self.historyKey)>0:
				nm=netMessage(C_NETWORK_CHARACTER_KEYBOARD)
				nm.addInt(User.getInstance().getId())
				nm.addInt(len(self.historyKey))
				for key in self.historyKey.keys():
					if key=='q' or key=='d' or key=='s' or key=='z' or key=='a' or key=='w':
						nm.addString(key)
						nm.addInt(self.historyKey[key])
				NetworkZoneUdp.getInstance().sendMessage(nm)
			
			self.historyKey.clear()
			
			
			if self.keysDown.has_key('t'):
				if (self.keysDown['t']!=0):
					self.seekNearestTarget("NPC")
					self.keysDown['t']=0
						
			User.getInstance().getCurrentCharacter().run()
			listOfNpc=self.currentZone.getListOfNPC()
			for n in listOfNpc:
				n.run()
			