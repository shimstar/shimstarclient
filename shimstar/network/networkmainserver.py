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
    instance = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.port = 7777
        self.ip = shimConfig.getInstance().getIp()
        self.stopThread = False
        self.timeout_in_miliseconds = 3000  # 3 seconds
        self.listOfMessage = []
        self.name = "NetWorkMainServer thread"
        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)
        self.started = False

        self.myConnection = self.cManager.openTCPClientConnection(self.ip, self.port, self.timeout_in_miliseconds)
        if self.myConnection:
            self.cReader.addConnection(self.myConnection)  # receive messages from server
            self.myConnection.setNoDelay(True)

    def isStarted(self):
        return self.started

    @staticmethod
    def getInstance():
        if NetworkMainServer.instance == None:
            NetworkMainServer.instance = NetworkMainServer()

        return NetworkMainServer.instance

    def isConnected(self):
        if self.myConnection == None:
            return False
        else:
            return True

    def run(self):
        # GameState.getInstance().setMainNetworkStarted(True)
        self.started=True
        while not self.stopThread:
            # ~ print "pwet"
            while self.cReader.dataAvailable():
                datagram = NetDatagram()  # catch the incoming data in this instance
                if self.cReader.getData(datagram):
                    self.myProcessDataFunction(datagram)
        self.started=False
        print "le thread NetworkMainServer s'est termine proprement"

    def stop(self):
        self.stopThread = True

    def myProcessDataFunction(self, netDatagram):
        myIterator = PyDatagramIterator(netDatagram)
        connexion = netDatagram.getConnection()
        msgID = myIterator.getUint32()
        msgTab = []
        print "mainserver msgID:: " + str(msgID)
        if msgID == C_NETWORK_CONNECT:
            state = myIterator.getUint32()
            msgTab.append(state)
            if state == 0:
                # ~ msgTab.append(myIterator.getString())
                msgTab.append(myIterator.getUint32())
                msgTab.append(myIterator.getString())
                nbChar = myIterator.getUint32()
                msgTab.append(nbChar)
                for i in range(nbChar):
                    msgTab.append(myIterator.getUint32())
                    msgTab.append(myIterator.getString())
                    msgTab.append(myIterator.getString())
                    msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_CURRENT_CHAR_INFO:
            msgTab.append(myIterator.getUint32())  # id ship
            msgTab.append(myIterator.getUint32())  # idtemplate ship
            msgTab.append(myIterator.getUint32())  # hull
            lenInv = int(myIterator.getUint32())  # inventory : length
            msgTab.append(lenInv)
            for i in range(lenInv):
                typeItem = int(myIterator.getUint32())  # inventory ; typeitem
                templateItem = int(myIterator.getUint32())  # inventory ; templateitem
                idItem = int(myIterator.getUint32())  # inventory ; id item
                msgTab.append(typeItem)
                msgTab.append(templateItem)
                msgTab.append(idItem)
                msgTab.append(myIterator.getUint32())  # quantity
            lenSlot = int(myIterator.getUint32())  # nb slot
            msgTab.append(lenSlot)
            for i in range(lenSlot):
                msgTab.append(myIterator.getUint32())  # idSlot
                lenTypes = myIterator.getUint32()  # nb types slot
                msgTab.append(lenTypes)
                for t in range(lenTypes):
                    msgTab.append(myIterator.getUint32())  # idtype
                msgTab.append(myIterator.getUint32())  # type item associe au slot
                msgTab.append(myIterator.getUint32())  # id template item associe au slot
                msgTab.append(myIterator.getUint32())  # id item associe au slot

            nbDialog = int(myIterator.getUint32())  # nb dialogues lus
            msgTab.append(nbDialog)
            for i in range(nbDialog):
                msgTab.append(myIterator.getUint32())  # id dialogue lu

            nbMission = int(myIterator.getUint32())
            msgTab.append(nbMission)
            for m in range(nbMission):
                msgTab.append(myIterator.getUint32())  # mission id
                msgTab.append(myIterator.getUint32())  # mission status
            nbItemInvStation = myIterator.getUint32()
            msgTab.append(nbItemInvStation)
            for nis in range(nbItemInvStation):
                msgTab.append(myIterator.getUint32())
                msgTab.append(myIterator.getUint32())
                msgTab.append(myIterator.getUint32())
                msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_CHARACTER_STATION2INV:
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_CHARACTER_INV2STATION:
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_CHARACTER_BUY_ITEM:
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_CHARACTER_SELL_ITEM:
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_CREATE_USER:
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_USER_DELETE_CHAR:
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_INFO_ZONE:
            ip = myIterator.getString()
            port = myIterator.getUint32()
            portudp = myIterator.getUint32()
            portudp2 = myIterator.getUint32()
            if NetworkZoneServer.getInstance() != None:
                NetworkZoneServer.getInstance().stop()
                # ~ print "############# " + str(ip) + '/' + str(port)
            NetworkZoneServer(ip, port)
            GameState.getInstance().setState(C_RECEIVED_INFOZONE)
        elif msgID == C_USER_ADD_CHAR:
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getString())
            msgTab.append(myIterator.getString())
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_DEATH_CHAR_STEP2:
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            # ~ print "networkmainserver::msg " + str(msgTab)
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)

    def getListOfMessageById(self, id):
        msgToReturn = []
        for msg in self.listOfMessage:
            iop = msg.getId()
            if (msg.getId() == id):
                msgToReturn.append(msg)

        return msgToReturn

    def removeMessage(self, msg):
        try:
            self.listOfMessage.remove(msg)
        except:
            print "networkMainServer::removeMessage : Warning : message not here"

    def sendMessage(self, msg):
        # ~ print msg.getMsg()
        self.cWriter.send(msg.getMsg(), self.myConnection)