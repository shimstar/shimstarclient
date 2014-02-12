import os,sys
from pandac.PandaModules import * 
from direct.distributed.PyDatagram import PyDatagram 
from direct.distributed.PyDatagramIterator import PyDatagramIterator 
from direct.stdpy import threading

from shimstar.core.constantes import *
from shimstar.network.message import *
from shimstar.game.gamestate import *

class NetworkZoneServer(threading.Thread):
	instance=None
	def __init__(self,ip,port):
		print "NetworkZoneServer::__init__" + str(ip) + "/" + str(port)
		threading.Thread.__init__(self)
		NetworkZoneServer.instance=self
		self.port=port
		self.ip=ip
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
		print "NetWorkZoneServer::init connection " + str(self.myConnection)
		
	@staticmethod
	def getInstance():
		return NetworkZoneServer.instance
		
	def isConnected(self):
		if self.myConnection==None:
			return False
		else:
			return True
		
	def run(self):
		while not self.stopThread:
			#~ print "pwet"
			try:
				while self.cReader.dataAvailable():
					datagram=NetDatagram()  # catch the incoming data in this instance
					if self.cReader.getData(datagram):
						self.myProcessDataFunction(datagram)
			except:
				print "pb thread networkzoneServer" + str(sys.exc_info()[0])
		print "le thread NetworkMainServer s'est termine proprement"
		
	def stop(self):
		self.stopThread=True
		
	def myProcessDataFunction(self,netDatagram):
		myIterator=PyDatagramIterator(netDatagram)
		connexion=netDatagram.getConnection()
		msgID=myIterator.getUint32()
		msgTab=[]
		#~ print msgID
		if msgID==C_NETWORK_CONNECT:
			state=myIterator.getUint32()
			msgTab.append(state)
			if state==0:
				msgTab.append(myIterator.getString())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NETWORK_INFO_ZONE:
			ip=myIterator.getString()
			port=myIterator.getUint32()
			port2=myIterator.getUint32()
		elif msgID==C_NETWORK_NPC_INCOMING:
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getString())
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())		
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NETWORK_NEW_CHAR_SHOT:
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
		elif msgID==C_NETWORK_NEW_NPC_SHOT:
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
		elif msgID==C_NETWORK_CURRENT_CHAR_INFO:
			msgTab.append(myIterator.getUint32())		
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
			
		elif msgID==C_NETWORK_REMOVE_SHOT:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NETWORK_EXPLOSION:
			msgTab=[]
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			msgTab.append(myIterator.getStdfloat())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
			
		elif msgID==C_NETWORK_NPC_SENT:
			GameState.getInstance().setState(C_NETWORK_NPC_SENT)
		elif msgID==C_NETWORK_CHAR_SENT:
			GameState.getInstance().setState(C_WAITING_CHARACTER_RECEIVED)
		elif msgID==C_NETWORK_TAKE_DAMAGE_NPC:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NETWORK_TAKE_DAMAGE_CHAR:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NETWORK_REMOVE_NPC:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NETWORK_REMOVE_CHAR:
			msgTab=[]
			msgTab.append(myIterator.getUint32())
			temp=message(msgID,msgTab)
			self.listOfMessage.append(temp)
		elif msgID==C_NETWORK_CHAR_INCOMING:
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
		elif msgID==C_NETWORK_REMOVE_NPC:
			GameState.getInstance().setState(C_WAITING_ASKING_INFO_NPC)
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
		self.cWriter.send(msg.getMsg(),self.myConnection)