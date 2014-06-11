from pandac.PandaModules import * 
from direct.distributed.PyDatagram import PyDatagram 
from direct.distributed.PyDatagramIterator import PyDatagramIterator 
from direct.stdpy import threading

from shimstar.core.constantes import *
from shimstar.core.shimconfig import *
from shimstar.network.message import *
from shimstar.network.networkzoneserver import *
from shimstar.game.gamestate import *

class NetworkMainServer(threading.Thread):
	instance=None
	def __init__(self):
		threading.Thread.__init__(self)
		self.port=7777
		self.ip=shimConfig.getInstance().getIp()
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
		print "mainserver msgID:: " + str(msgID)
		if msgID==C_NETWORK_CONNECT:
			state=myIterator.getUint32()
			msgTab.append(state)
			if state==0:
				#~ msgTab.append(myIterator.getString())
				msgTab.append(myIterator.getUint32())
				msgTab.append(myIterator.getString())
				nbChar=myIterator.getUint32()
				msgTab.append(nbChar)
				for i in range (nbChar):
					msgTab.append(myIterator.getUint32())
					msgTab.append(myIterator.getString())
					msgTab.append(myIterator.getString())
					msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NETWORK_CURRENT_CHAR_INFO:
			msgTab.append(myIterator.getUint32())		
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			lenInv=int(myIterator.getUint32())
			for i in range(lenInv):
				inv=int(myIterator.getUint32())
			nbDialog=int(myIterator.getUint32())
			msgTab.append(nbDialog)
			for i in range (nbDialog):
				msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_CREATE_USER:
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_USER_DELETE_CHAR:
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NETWORK_INFO_ZONE:
			ip=myIterator.getString()
			port=myIterator.getUint32()
			portudp=myIterator.getUint32()
			portudp2=myIterator.getUint32()
			if NetworkZoneServer.getInstance()!=None:
				NetworkZoneServer.getInstance().stop()
			#~ print "############# " + str(ip) + '/' + str(port)
			NetworkZoneServer(ip,port)
			GameState.getInstance().setState(C_RECEIVED_INFOZONE)
		elif msgID==C_USER_ADD_CHAR:
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getString())
			msgTab.append(myIterator.getString())
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NETWORK_DEATH_CHAR_STEP2:
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			#~ print "networkmainserver::msg " + str(msgTab)
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