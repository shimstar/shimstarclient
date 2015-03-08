from pandac.PandaModules import loadPrcFileData 

loadPrcFileData('', 'win-size %i %i' % (1280, 720))
#~ loadPrcFileData('', 'win-size %i %i' % (1600, 900))
#~ loadPrcFileData('', 'state-cache 0')
#~ loadPrcFileData('','fullscreen 1')
import sys,os
from array import array
#~ import win32api
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.task.Task import Task

from shimstar.game.gamestate import *
from shimstar.network.networkmainserver import *
from shimstar.user.user import *
from shimstar.world.zone.zone import *
from shimstar.game.gameinspace import *
from shimstar.game.explosion import *
from shimstar.gui.system.menuconnectcegui import *
from shimstar.gui.system.menuchooseherocegui import *
from shimstar.gui.system.menuloadzonecegui import *
from shimstar.gui.game.menudeath import *
from shimstar.gui.station.guistation import *


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
		#~ while 1:
			#~ self.dispatch()
		
	def preLoad(self):
		Explosion.preload()
	
	def dispatch(self,task):
	#~ def dispatch(self):
		state=GameState.getInstance().getState()
		if state==C_INIT:
			if self.menu!=None:
				if isinstance(self.menu,MenuConnectCegui)!=True:
					self.menu.destroy()
					self.menu=None
					self.menu=MenuConnectCegui()
			else:
				self.menu=MenuConnectCegui()
		elif state==C_CHOOSE_HERO:
			if self.menu!=None:
				if isinstance(self.menu,MenuChooseHeroCegui)!=True:
					self.menu.destroy()
					self.menu=None
					self.menu=MenuChooseHeroCegui()				
			else:
				self.menu=MenuChooseHeroCegui()				
		elif state==C_CHANGEZONE:
			idZone=GameState.getInstance().getNewZone()
			
			if idZone==0 or idZone==User.getInstance().getCurrentCharacter().getIdZone():
				idZone=User.getInstance().getCurrentCharacter().getIdZone()
			name,typeZone=Zone.getTinyInfosFromZone(idZone)
			if typeZone==C_TYPEZONE_SPACE:
				msg=netMessage(C_NETWORK_INFO_ZONE)
				msg.addUInt(idZone)
				NetworkMainServer.getInstance().sendMessage(msg)
				GameState.getInstance().setState(C_WAITING_INFOZONE)
				if isinstance(self.menu,MenuLoadZoneCegui)!=True:
					self.menu.destroy()
					self.menu=None
					self.menu=MenuLoadZoneCegui()
				
			else:
				GameState.getInstance().setState(C_GOPLAY)

		elif state==C_GOPLAY:
			idZone=User.getInstance().getCurrentCharacter().getIdZone()
			print "main::dispatch GOPLAY" + str(idZone)
			name,typeZone=Zone.getTinyInfosFromZone(idZone)
			if typeZone==C_TYPEZONE_SPACE:
				if isinstance(self.menu,GameInSpace)!=True:
					self.menu.destroy()
					self.menu=None
					self.menu=GameInSpace()
				
				self.menu.start()
			else:
				if isinstance(self.menu,GuiStation)!=True:
					self.menu.destroy()
					self.menu=None
					self.menu=GuiStation()
				#~ else:
					#~ self.menu=GuiStation()
		#~ elif state==C_PLAYING:
			#~ if isinstance(self.menu,GameInSpace)==True:
				#~ self.menu.run()
				
		elif state==C_RECEIVED_INFOZONE:
			msg=netMessage(C_NETWORK_CONNECT)
			msg.addUInt(User.getInstance().getId())
			msg.addUInt(User.getInstance().getCurrentCharacter().getId())
			#~ msg.addUInt(NetworkZoneUdp.getInstance().port)
			NetworkZoneServer.getInstance().sendMessage(msg)
			NetworkZoneServer.getInstance().start()
			#~ NetworkZoneUdp.getInstance().start()
			idZone=User.getInstance().getCurrentCharacter().getIdZone()
			name,typeZone=Zone.getTinyInfosFromZone(idZone)
			GameState.getInstance().setState(C_WAITING_LOADINGZONE)
		elif state==C_WAITING_ASKING_INFO_CHARACTER:
			tempMsg=NetworkZoneServer.getInstance().getListOfMessageById(C_NETWORK_CURRENT_CHAR_INFO)
			if len(tempMsg)>0:
				for msg in tempMsg:
					netMsg=msg.getMessage()
					ch=User.getInstance().getCurrentCharacter()
					ch.setShip(netMsg[0],netMsg[1],netMsg[2],False)
					nbInv=netMsg[3]
					ship=ch.getShip()
					compteur=4
					for i in range(nbInv):
						typeItem=netMsg[compteur]
						compteur+=1
						templateId=netMsg[compteur]
						compteur+=1
						idItem=netMsg[compteur]
						compteur+=1
						it=itemFactory.getItemFromTemplateType(templateId,typeItem)
						it.setId(idItem)
						quantity=netMsg[compteur]
						compteur+=1
						if typeItem==C_ITEM_MINERAL:
							it.setQuantity(quantity)
						ship.addItemInInventory(it)
						
					nbSlot=netMsg[compteur]
					ship.removeTemplateSlots()
					compteur+=1
					for n in range(nbSlot):
						idSlot=netMsg[compteur]
						tempSlot=Slot(None,idSlot)
						compteur+=1
						nbTypes=netMsg[compteur]
						compteur+=1
						for t in range(nbTypes):
							idType=netMsg[compteur]
							compteur+=1
							tempSlot.appendTypes(idType)
						typeItem=netMsg[compteur]
						compteur+=1
						templateItem=netMsg[compteur]
						compteur+=1
						idItem=netMsg[compteur]
						compteur+=1
						if idItem!=0:
							it=itemFactory.getItemFromTemplateType(templateItem,typeItem)
							it.setId(idItem)
							tempSlot.setItem(it)
						ship.addSlot(tempSlot)
					GameState.getInstance().setState(C_WAITING_CHARACTER_RECEIVED)
					NetworkZoneServer.getInstance().removeMessage(msg)
		elif state==C_QUIT:
			sys.exit()
		elif state==C_DEATH:
			Zone.getInstance().stop()
			if self.menu!=None:
				if isinstance(self.menu,MenuDeath)!=True:
					self.menu.destroy()
					self.menu=MenuDeath()
			else:
				self.menu=MenuDeath()
		
		
		GameState.lock.acquire()
		GameState.lock.release()
		
		return Task.cont
		
#~ print 'Number of arguments:', len(sys.argv), 'arguments.'
#~ print 'Argument List:', str(sys.argv)
#~ dir="."
#~ if len(sys.argv):
	#~ dir=str(sys.argv)

app=ShimStarClient()
run()
