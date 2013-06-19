import sys,os
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.distributed.PyDatagram import PyDatagram 
from direct.distributed.PyDatagramIterator import PyDatagramIterator 
from direct.gui.DirectFrame import DirectFrame
#~ from direct.task.TaskOrig import Task
from direct.task import Task
from shimstar.network.message import *
from shimstar.core.constantes import *
from direct.stdpy import threading


class NetworkZoneUdp(DirectObject,threading.Thread):
	instance=None
	def __init__(self,ip,port,nom='threadUDP'):
		threading.Thread.__init__(self)
		self.nom = nom
		self.Terminated = False
		self.stopThread=False
		self.updateChar={}
		self.lastRun=globalClock.getRealTime()
		NetworkZoneUdp.instance=self

		self.port_address=port# same for client and server
		self.cManager = QueuedConnectionManager()
		self.cReader = QueuedConnectionReader(self.cManager, 0)
		self.cReader.setRawMode(0)
		self.cWriter = ConnectionWriter(self.cManager,0)
		self.cWriter.setRawMode(0)
		self.ip=ip
		self.port=port
		

	# how long until we give up trying to reach the server?
		timeout_in_miliseconds=3000  # 3 seconds
	
		self.myConnection=self.cManager.openUDPConnection(self.port+1)
		if self.myConnection:
			self.cReader.addConnection(self.myConnection)  # receive messages from server
			self.serverAddr = NetAddress() 
			self.serverAddr.setHost(self.ip, self.port) 
		
		self.listOfMessage=[] 
	
	@staticmethod
	def getInstance():
		return NetworkZoneUdp.instance
	
		
	def run(self):
		i = 0
		while not self.stopThread:
			while self.cReader.dataAvailable()!=False:
				dt=globalClock.getRealTime()-self.lastRun
				self.lastRun=globalClock.getRealTime()
				datagram=NetDatagram()  # catch the incoming data in this instance
				# Check the return value; if we were threaded, someone else could have
				# snagged this data before we did
				if self.cReader.getData(datagram):
					self.myProcessDataFunction(datagram)
				dt2=globalClock.getRealTime()-self.lastRun
		print "le thread Network s'est termine proprement"
	
	def stop(self):
		self.stopThread=True
		
	def isConnected(self):
		if self.myConnection==None:
			return False
		else:
			return True

	def myNewPyDatagram(self,id,message):
		myPyDatagram=PyDatagram()
		myPyDatagram.addUint8(id)
		myPyDatagram.addString(message)
		
		return myPyDatagram
		
	def sendMessage(self,msg):
		#~ print "MESSAGE OUT UDP : ##############" + str(id )
		print self.serverAddr.getPort()
		print msg.getMsg()
		self.cWriter.send(msg.getMsg(),self.myConnection,self.serverAddr)
						
	def myProcessDataFunction(self,netDatagram):
		myIterator=PyDatagramIterator(netDatagram)
		connexion=netDatagram.getConnection()
		msgID=myIterator.getUint32()
		if msgID==C_UPDATE_POS_CHAR:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_UPDATE_POS_NPC:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_UPDATE_CHAR_COIN:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_UPDATE_CHAR_BUYITEM:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_UPDATE_CHAR_SELLITEM:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_UPDATE_CHAR_SHOT:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getString())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NPC_INCOMING:
			msgTab=[]
			msgTab.append(myIterator.getString())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NEWPLAYER_INCOMING:
			msgTab=[]
			msgTab.append(myIterator.getString())
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_JUNK_REMOVE:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getString())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_ADD_JUNK:
			msgTab=[]
			msgTab.append(myIterator.getString())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_ADD_EXPLOSION:
			msgTab=[]
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_CHAR_UPDATE_UPMISSION:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getString())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_UPDATE_CHAR_COLLECT:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_UPDATE_CHAR_TAKEDAMAGE:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_UPDATE_NPC_TAKEDAMAGE:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			#~ msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_PING:
			msgTab=[]
			msgTab.append(myIterator.getStdfloat())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_UPDATE_NPC_SHOT:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getString())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		else:
			msg=myIterator.getString()		
			msgtab=msg.split("@")
			temp=message(msgID,msgtab[1])
			self.listOfMessage.append(temp)
		
	def getListOfMessageById(self,id):
		msgToReturn=[]
		for msg in self.listOfMessage:
			iop=msg.getId()
			if(msg.getId()==id):
				msgToReturn.append(msg)
			
		return msgToReturn
		
	def removeMessage(self,msg):
		self.listOfMessage.remove(msg)
    