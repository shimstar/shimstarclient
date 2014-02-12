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
	def __init__(self,ip,port,port2,nom='threadUDP'):
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
		self.port2=port2
		print "NetworkZoneUdp " +str(ip) + "/" + str(port)
	# how long until we give up trying to reach the server?
		timeout_in_miliseconds=3000  # 3 seconds
	
		self.myConnection=self.cManager.openUDPConnection(self.port+1)
		print "NetworkZoneUdp" + str(self.myConnection)
		if self.myConnection:
			self.cReader.addConnection(self.myConnection)  # receive messages from server
			self.serverAddr = NetAddress() 
			self.serverAddr.setHost(self.ip, self.port) 
		else:
			self.myConnection=self.cManager.openUDPConnection(self.port2+1)
			if self.myConnection:
				self.port=port2
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
			#~ print "UDP :: run : " + str(self.cReader.dataAvailable())
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
		try:
			#~ print "UDP : : sendMessage " + str(self.serverAddr)
			self.cWriter.send(msg.getMsg(),self.myConnection,self.serverAddr)
		except:
			print "UDP sendMessage :: Unexpected error:", sys.exc_info()[0]
			
						
	def myProcessDataFunction(self,netDatagram):
		myIterator=PyDatagramIterator(netDatagram)
		connexion=netDatagram.getConnection()
		msgID=myIterator.getUint32()
		#~ print "zoneudp" + str(msgID)
		if msgID==C_NETWORK_CHARACTER_UPDATE_POS:
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
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NETWORK_NPC_UPDATE_POS:
			msgTab=[]
			nbNpc=myIterator.getUint32()
			msgTab.append(nbNpc)
			for itNpc in range(nbNpc):
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
		elif msgID==C_NETWORK_POS_SHOT:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			temp=message(msgID,msgTab)
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
    