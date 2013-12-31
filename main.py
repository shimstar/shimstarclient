from pandac.PandaModules import loadPrcFileData 

loadPrcFileData('', 'win-size %i %i' % (1280, 720))
#~ loadPrcFileData('', 'state-cache 0')
import sys,os
from array import array
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.task.Task import Task

from shimstar.game.gamestate import *
from shimstar.gui.system.menuconnectrocket import *
from shimstar.gui.system.menucreateaccountrocket import *
from shimstar.gui.system.menuchooseherorocket import *
from shimstar.gui.system.menuloadzone import *
from shimstar.network.networkmainserver import *
from shimstar.user.user import *
from shimstar.world.zone.zone import *
from shimstar.game.gameinspace import *
from shimstar.game.explosion import *
from shimstar.gui.system.menuconnectcegui import *
from shimstar.gui.system.menuchooseherocegui import *
from shimstar.gui.system.menuloadzonecegui import *


base.win.setCloseRequestEvent("CLOSEF4")

class ShimStarClient(DirectObject):
	def __init__(self):
		GameState().setState(0)
		
		
		NetworkMainServer.getInstance().start()
		self.menu=None
		base.disableMouse()
		base.setFrameRateMeter(True)
		render.setAntialias(AntialiasAttrib.MAuto)
		self.preLoad()
		taskMgr.add(self.dispatch,"dispatch Main",-40)  
		
	def preLoad(self):
		Explosion.preload()
	
	def dispatch(self,task):
		state=GameState.getInstance().getState()
		if state==C_INIT:
			if self.menu!=None:
				if isinstance(self.menu,MenuConnectCegui)!=True:
				#~ if isinstance(self.menu,menuconnectRocket)!=True:
					self.menu.destroy()
					self.menu=None
					#~ self.menu=menuconnectRocket().getInstance()
					self.menu=MenuConnectCegui()
			else:
				self.menu=MenuConnectCegui()
				#~ self.menu=menuconnectRocket().getInstance()
		elif state==C_MENUCREATEACCOUNT:
			if isinstance(self.menu,MenuCreateAccountRocket)!=True:
				self.menu.destroy()
				self.menu=None
				self.menu=MenuCreateAccountRocket().getInstance()
			else:
				self.menu=MenuCreateAccountRocket().getInstance()
			GameState.getInstance().setState(C_MENUCREATINGACCOUNT)
		elif state==C_CHOOSE_HERO:
			if self.menu!=None:
				#~ if isinstance(self.menu,menuchooseHeroRocket)!=True:
				if isinstance(self.menu,MenuChooseHeroCegui)!=True:
					self.menu.destroy()
					self.menu=None
					#~ self.menu=menuchooseHeroRocket()				
					self.menu=MenuChooseHeroCegui()				
			else:
				self.menu=MenuChooseHeroCegui()				
				#~ self.menu=menuchooseHeroRocket()				
		elif state==C_CHANGEZONE:
			idZone=User.getInstance().getCurrentCharacter().getIdZone()
			name,typeZone=Zone.getTinyInfosFromZone(idZone)
			#~ print str(idZone) + "/" + str(name) + str(typeZone)
			if typeZone==C_TYPEZONE_SPACE:
				msg=netMessage(C_NETWORK_INFO_ZONE)
				msg.addInt(idZone)
				NetworkMainServer.getInstance().sendMessage(msg)
				GameState.getInstance().setState(C_WAITING_INFOZONE)
				#~ if isinstance(self.menu,menuLoadZoneRocket)!=True:
				if isinstance(self.menu,MenuLoadZoneCegui)!=True:
					self.menu.destroy()
					self.menu=None
					#~ self.menu=menuLoadZoneRocket()
					self.menu=MenuLoadZoneCegui()
				else:
					#~ self.menu=menuLoadZoneRocket()
					self.menu=MenuLoadZoneCegui()
		elif state==C_GOPLAY:
			if isinstance(self.menu,GameInSpace)!=True:
				self.menu.destroy()
				self.menu=None
				self.menu=GameInSpace()
			else:
				self.menu=GameInSpace()
			self.menu.start()
		elif state==C_RECEIVED_INFOZONE:
			msg=netMessage(C_NETWORK_CONNECT)
			msg.addInt(User.getInstance().getId())
			msg.addInt(User.getInstance().getCurrentCharacter().getId())
			NetworkZoneServer.getInstance().sendMessage(msg)
			NetworkZoneServer.getInstance().start()
			NetworkZoneUdp.getInstance().start()
			idZone=User.getInstance().getCurrentCharacter().getIdZone()
			name,typeZone=Zone.getTinyInfosFromZone(idZone)
			GameState.getInstance().setState(C_WAITING_LOADINGZONE)
			#~ if typeZone==C_TYPEZONE_SPACE:
				#~ if isinstance(self.menu,GameInSpace)!=True:
					#~ self.menu.destroy()
					#~ self.menu=None
					#~ self.menu=GameInSpace()
				#~ else:
					#~ self.menu=GameInSpace()
				#~ self.menu.start()
		elif state==C_WAITING_ASKING_INFO_CHARACTER:
			tempMsg=NetworkZoneServer.getInstance().getListOfMessageById(C_NETWORK_CURRENT_CHAR_INFO)
			if len(tempMsg)>0:
				for msg in tempMsg:
					netMsg=msg.getMessage()
					User.getInstance().getCurrentCharacter().setShip(netMsg[0])
					GameState.getInstance().setState(C_WAITING_CHARACTER_RECEIVED)
					NetworkZoneServer.getInstance().removeMessage(msg)
		elif state==C_QUIT:
			sys.exit()
		return Task.cont
		
app=ShimStarClient()
run()
