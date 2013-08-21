from pandac.PandaModules import * 
from direct.distributed.PyDatagram import PyDatagram 
from direct.distributed.PyDatagramIterator import PyDatagramIterator 
from direct.stdpy import threading

from shimstar.core.constantes import *
from shimstar.network.message import *
from shimstar.network.networkzoneserver import *
from shimstar.network.networkzoneudp import *
from shimstar.game.gamestate import *

class NetworkMainServer(threading.Thread):
	instance=None
	def __init__(self):
		threading.Thread.__init__(self)
		self.port=7777
		self.ip="127.0.0.1"
		#~ self.ip="10.85.80.74"
		self.stopThread=False
		self.timeout_in_miliseconds=3000  # 3 seconds
		self.listOfMessage=[] 
		
		self.cManager = QueuedConnectionManager()
		self.cReader = QueuedConnectionReader(self.cManager, 0)
		self.cWriter = ConnectionWriter(self.cManager,0)
		
		self.myConnection=self.cManager.openTCPClientConnection(self.ip,self.port,self.timeout_in_miliseconds)
		if self.myConnection:
			self.cReader.addConnection(self.myConnection)  # receive messages from server
			self.myConnection.setNoDelay(True)
		
		
	@staticmethod
	def getInstance():
		if NetworkMainServer.instance==None:
			NetworkMainServer.instance=NetworkMainServer()
			
		return NetworkMainServer.instance
		
	def isConnected(self):
		if self.myConnection==None:
			return False
		else:
			return True
		
	def run(self):
		while not self.stopThread:
			#~ print "pwet"
			while self.cReader.dataAvailable():
				datagram=NetDatagram()  # catch the incoming data in this instance
				if self.cReader.getData(datagram):
					self.myProcessDataFunction(datagram)
					
		print "le thread NetworkMainServer s'est termine proprement"
		
	def stop(self):
		self.stopThread=True
		
	def myProcessDataFunction(self,netDatagram):
		myIterator=PyDatagramIterator(netDatagram)
		connexion=netDatagram.getConnection()
		msgID=myIterator.getUint32()
		msgTab=[]
		if msgID==C_NETWORK_CONNECT:
			state=myIterator.getUint32()
			msgTab.append(state)
			if state==0:
				msgTab.append(myIterator.getString())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_CREATE_USER:
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NETWORK_INFO_ZONE:
			ip=myIterator.getString()
			port=myIterator.getUint32()
			portudp=myIterator.getUint32()
			if NetworkZoneServer.getInstance()!=None:
				NetworkZoneServer.getInstance().stop()
			NetworkZoneServer(ip,port)
			if NetworkZoneUdp.getInstance()!=None:
				NetworkZoneUdp.getInstance().stop()
			NetworkZoneUdp(ip,portudp)
			GameState.getInstance().setState(C_RECEIVED_INFOZONE)
		elif msgID==C_USER_ADD_CHAR:
			msgTab.append(myIterator.getString())
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
		
	def sendMessage(self,msg):
		#~ print msg.getMsg()
		self.cWriter.send(msg.getMsg(),self.myConnection)