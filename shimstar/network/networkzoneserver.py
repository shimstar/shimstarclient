import os, sys
from pandac.PandaModules import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.stdpy import threading

from shimstar.core.constantes import *
from shimstar.network.message import *
from shimstar.game.gamestate import *


class NetworkZoneServer(threading.Thread):
    instance = None

    def __init__(self, ip, port):
        print "NetworkZoneServer::__init__" + str(ip) + "/" + str(port)
        threading.Thread.__init__(self)
        NetworkZoneServer.instance = self
        self.port = port
        self.ip = ip
        self.name = "NetworkZoneServer"
        self.stopThread = False
        self.timeout_in_miliseconds = 3000  # 3 seconds
        self.listOfMessage = []

        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)
        self.myConnection = self.cManager.openTCPClientConnection(self.ip, self.port, self.timeout_in_miliseconds)
        if self.myConnection:
            self.cReader.addConnection(self.myConnection)  # receive messages from server
            self.myConnection.setNoDelay(True)
        print "NetWorkZoneServer::init connection " + str(self.myConnection)


    @staticmethod
    def getInstance():
        return NetworkZoneServer.instance

    def isConnected(self):
        if self.myConnection == None:
            return False
        else:
            return True

    def run(self):
        # GameState.getInstance().setZoneNetworkStarted(True)

        while not self.stopThread:
            # ~ print "pwet"
            try:
                while self.cReader.dataAvailable():
                    datagram = NetDatagram()  # catch the incoming data in this instance
                    if self.cReader.getData(datagram):
                        self.myProcessDataFunction(datagram)
            except:
                # GameState.getInstance().setZoneNetworkStarted(False)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                self.stopThread = True
                print "problem into networkzone server"


        # GameState.getInstance().setZoneNetworkStarted(False)
        print "le thread NetworkZoneServer s'est termine proprement"


    def stop(self):
        self.stopThread = True


    def myProcessDataFunction(self, netDatagram):
        myIterator = PyDatagramIterator(netDatagram)
        connexion = netDatagram.getConnection()
        msgID = myIterator.getUint32()
        msgTab = []
        # print "gamestatene =" +str(GameState.getInstance().getState()) + str(GameState.getInstance())
        # if msgID not in (110,112):
        # print msgID
        if msgID == C_NETWORK_CONNECT:
            state = myIterator.getUint32()
            msgTab.append(state)
            if state == 0:
                msgTab.append(myIterator.getString())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_INFO_ZONE:
            ip = myIterator.getString()
            port = myIterator.getUint32()
            port2 = myIterator.getUint32()
        elif msgID == C_NETWORK_CHAR_INCOMING:
            msgTab.append(myIterator.getUint32())  # iduser
            msgTab.append(myIterator.getString())  # name user
            msgTab.append(myIterator.getUint32())  # id char
            msgTab.append(myIterator.getString())  # namechar
            msgTab.append(myIterator.getString())  # facechar
            msgTab.append(myIterator.getUint32())  # idzone
            msgTab.append(myIterator.getUint32())  # idship
            msgTab.append(myIterator.getUint32())  # templateship
            msgTab.append(myIterator.getUint32())  # hullpoints
            nbInv = myIterator.getUint32()         # nb item in inv
            msgTab.append(nbInv)
            for itInv in range (nbInv):
                msgTab.append(myIterator.getUint32())  # typeItem
                msgTab.append(myIterator.getUint32())  # templateId
                msgTab.append(myIterator.getUint32())  # id
                msgTab.append(myIterator.getUint32())  # nb

            nbSlot = myIterator.getUint32()        # nb Slot
            msgTab.append(nbSlot)
            for itSlot in range(nbSlot):
                msgTab.append(myIterator.getUint32()) #idSlot
                nbTypeItem = myIterator.getUint32()   #nbTypeItem
                msgTab.append(nbTypeItem)
                for itType in range (nbTypeItem):
                    msgTab.append(myIterator.getUint32())
                msgTab.append(myIterator.getUint32()) # typeItem
                msgTab.append(myIterator.getUint32()) # templateId
                msgTab.append(myIterator.getUint32()) # id
                msgTab.append(myIterator.getUint32()) # Enabled/disabled
                msgTab.append(myIterator.getInt32()) # pos slot X
                msgTab.append(myIterator.getInt32()) # pos slot Y
                msgTab.append(myIterator.getInt32()) # pos slot Z
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_NPC_INCOMING:
            msgTab.append(myIterator.getUint32())  #idnpc
            msgTab.append(myIterator.getString())  #name
            msgTab.append(myIterator.getUint32())  #templatenpc
            msgTab.append(myIterator.getUint32())  #idship
            msgTab.append(myIterator.getUint32())  #idtemplateship
            msgTab.append(myIterator.getUint32())  #hullpoints
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_SEND_NPC_LOADINGZONE:
            nbNpc = myIterator.getUint32()  #nbNpc
            msgTab.append(nbNpc)
            for nbNpc in range(nbNpc):
                msgTab.append(myIterator.getUint32())  #idnpc
                msgTab.append(myIterator.getString())  #name
                msgTab.append(myIterator.getUint32())  #templatenpc
                msgTab.append(myIterator.getUint32())  #idship
                msgTab.append(myIterator.getUint32())  #idtemplateship
                msgTab.append(myIterator.getUint32())  #hullpoints
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_DESTROY_JUNK:
            msgTab.append(myIterator.getUint32())  #idjunk
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_NEW_CHAR_SHOT:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_NEW_NPC_SHOT:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_CURRENT_CHAR_INFO:
            print " receiving C_NETWORK_CURRENT_CHAR_INFO " + str(C_NETWORK_CURRENT_CHAR_INFO)
            msgTab.append(myIterator.getUint32())  #id ship
            msgTab.append(myIterator.getUint32())  #idtemplate ship
            msgTab.append(myIterator.getUint32())  #hull
            lenInv = int(myIterator.getUint32())  #inventory : length
            msgTab.append(lenInv)
            for i in range(lenInv):
                typeItem = int(myIterator.getUint32())  #inventory ; typeitem
                templateItem = int(myIterator.getUint32())  #inventory ; templateitem
                idItem = int(myIterator.getUint32())  #inventory ; id item
                msgTab.append(typeItem)
                msgTab.append(templateItem)
                msgTab.append(idItem)
                msgTab.append(myIterator.getUint32())  #quantity
            lenSlot = int(myIterator.getUint32())  #nb slot
            msgTab.append(lenSlot)
            for i in range(lenSlot):
                msgTab.append(myIterator.getUint32())  #idSlot
                lenTypes = myIterator.getUint32()  #nb types slot
                msgTab.append(lenTypes)
                for t in range(lenTypes):
                    msgTab.append(myIterator.getUint32())  #idtype
                msgTab.append(myIterator.getUint32())  #type item associe au slot
                msgTab.append(myIterator.getUint32())  #id template item associe au slot
                msgTab.append(myIterator.getUint32())  #id item associe au slot
                msgTab.append(myIterator.getUint32()) # enabled
                msgTab.append(myIterator.getInt32())
                msgTab.append(myIterator.getInt32())
                msgTab.append(myIterator.getInt32())

            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_CHARACTER_ADD_TO_INVENTORY:
            msgTab = []
            typeItem = int(myIterator.getUint32())  #inventory ; typeitem
            templateItem = int(myIterator.getUint32())  #inventory ; templateitem
            idItem = int(myIterator.getUint32())  #inventory ; id item
            msgTab.append(typeItem)
            msgTab.append(templateItem)
            msgTab.append(idItem)
            msgTab.append(myIterator.getUint32())  #quantity
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_REMOVE_SHOT:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_EXPLOSION:
            msgTab = []
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_EXPLOSION_SHIELD:
            msgTab = []
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            # msgTab.append(myIterator.getStdfloat())
            # msgTab.append(myIterator.getStdfloat())
            # msgTab.append(myIterator.getStdfloat())
            # msgTab.append(myIterator.getStdfloat())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_USER_OUTGOING:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_ADD_ITEMINSPACE:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_ADD_JUNK:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            nbItem = myIterator.getUint32()
            msgTab.append(nbItem)
            for i in range(nbItem):
                msgTab.append(myIterator.getUint32())
                msgTab.append(myIterator.getUint32())
                msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_CHARACTER_ADD_TO_INVENTORY_FROM_JUNK:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_NPC_SENT:
            msgTab = []
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_JUNK_SENT:
            msgTab = []
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_CHAR_SENT:
            # print "C_NETWORK_CHAR_SENT "
            msgTab = []
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_ITEMINSPACE_SENT:
            print "C_NETWORK_ITEMINSPACE_SENT"
            msgTab = []
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)

        elif msgID == C_NETWORK_TAKE_DAMAGE_NPC:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_TAKE_DAMAGE_CHAR:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_REMOVE_NPC:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_REMOVE_CHAR:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_DEATH_CHAR:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_CHARACTER_UPDATE_POS:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getUint32()) #poussee
            msgTab.append(myIterator.getUint32()) #hitpoints
            nbShield = myIterator.getUint32()
            msgTab.append(nbShield)
            for i in range (nbShield):
                msgTab.append(myIterator.getUint32()) #idShield
                msgTab.append(myIterator.getUint32()) #hitpoints shield
            # print msgTab
            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_NPC_UPDATE_POS:
            msgTab = []
            nbNpc = myIterator.getUint32()
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
                hp = myIterator.getUint32()
                msgTab.append(hp) #hitpoints
                nbShield = myIterator.getUint32()
                msgTab.append(nbShield)
                for itShield in range (nbShield):
                    msgTab.append(myIterator.getUint32())
                    msgTab.append(myIterator.getUint32())

            temp = message(msgID, msgTab)
            self.listOfMessage.append(temp)
        elif msgID == C_NETWORK_POS_SHOT:
            msgTab = []
            msgTab.append(myIterator.getUint32())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
            msgTab.append(myIterator.getStdfloat())
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
        if self.listOfMessage.count(msg) > 0:
            try:
                self.listOfMessage.remove(msg)
            except:
                print "NetWorkZoneServer::RemoveMessage Warning : Message was'nt present into list of message"


    def sendMessage(self, msg):
        self.cWriter.send(msg.getMsg(), self.myConnection)