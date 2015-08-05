import xml.dom.minidom
import os, sys

from shimstar.network.networkmainserver import *
from shimstar.network.message import *
from shimstar.network.netmessage import *
from shimstar.game.gamestate import *
from shimstar.items.ship import *


class Character:
    def __init__(self, id, name, egg, idZone, userRef):
        self.id = id
        self.name = name
        self.face = egg
        self.coin = 0
        self.current = False
        self.ship = None
        self.idZone = idZone
        self.lastStation = 0
        self.invStation = []
        self.missions = []
        self.visible = False
        self.userRef = userRef  # user obj
        self.readDialogs = []
        print "character::init" + str(self.id) + "// idzone =" + str(idZone)

    def setInvStation(self,inv):
        self.invStation = inv

    def getInvStation(self):
        return self.invStation

    def appendInvStation(self,item):
        self.invStation.append(item)

    def getItemInInvStation(self,itemId):
        for it in self.invStation:
            if it.getId() == itemId:
                return it

        return None

    def removeItemFromInvstation(self,item):
        if item in self.invStation:
            self.invStation.remove(item)

    def removeItemFromInvStationById(self,idItem):
        itemToRemove = None
        for it in self.invStation:
            if it.getId() == idItem:
                itemToRemove = it
                break

        if itemToRemove is not None:
            self.invStation.remove(itemToRemove)

    def getCoin(self):
        return self.coin

    def setCoin(self,coin):
        self.coin = coin

    def addCoin(self,coin):
        self.coin += coin

    def getMissions(self):
        return self.missions

    def addMission(self, m):
        self.missions.append(m)

    def getReadDialogs(self):
        return self.readDialogs

    def appendDialogs(self, id):
        if (id in self.readDialogs) == False:
            self.readDialogs.append(id)
            return True
        return False

    def manageDeath(self):
        print "Character::manageDeath"
        if self.ship != None:
            self.ship.destroy()
            self.ship = None

    def setShip(self, idShip, idTemplate, hullpoints, visible=True):
        print "character :: setsHip " + str(hullpoints) + "/" + str(idShip)
        self.ship = Ship(idShip, idTemplate, hullpoints, visible)
        self.ship.setOwner(self)
        print "character:setShip" + str(self.ship)

        # ~ def removeShip(self):


    def destroy(self):
        if self.ship != None:
            self.ship.destroy()
            self.ship = None

    def takeDamage(self, damage):
        #~ print "character::takedamage " + str(damage)
        if self.ship != None:
            return self.ship.takeDamage(damage)
        return None

    def setPos(self, pos):
        self.ship.setPos(pos)

    def setQuat(self, quat):
        self.ship.setQuat(quat)

    def getUserId(self):
        return self.userRef.getId()

    def run(self):
        if self.ship != None:
            self.ship.move()

    def getShip(self):
        return self.ship

    def addBullet(self, bulId, pos, quat):
        self.ship.addBullet(bulId, pos, quat)

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def getIdZone(self):
        return self.idZone

    def getFace(self):
        return self.face

    def setCurrent(self, current):
        self.current = current

    def isCurrent(self):
        return self.current

    def getInvStationWithout(self,typeWithout):
        invToReturn = []
        for inv in self.invStation:
            if inv.getTypeItem() not in typeWithout:
                invToReturn.append(inv)
        return invToReturn

    def changeZone(self, death=False):
        if GameState.getInstance().getNewZone() != 0:
            self.idZone = GameState.getInstance().getNewZone()
        msg = netMessage(C_NETWORK_USER_CHANGE_ZONE)
        #~ print "characeter::changeZone " + str(self.userRef.id) + "/" + str(self.userRef.getId()) + "/" + str(self.ship)
        msg.addUInt(self.userRef.getId())
        msg.addUInt(self.idZone)
        NetworkMainServer.getInstance().sendMessage(msg)

        if NetworkZoneServer.getInstance() != None:
            nm = netMessage(C_NETWORK_USER_CHANGE_ZONE)
            nm.addUInt(self.userRef.getId())
            NetworkZoneServer.getInstance().sendMessage(nm)

        if self.ship != None:
            self.ship.changeZone()

        if death:
            GameState.getInstance().setState(C_DEATH)
        else:
            GameState.getInstance().setState(C_CHANGEZONE)
        return

    def evaluateMission(self, id, idNPC):
        for m in self.missions:
            if m.getId() == int(id):
                if m.getStatus() == C_STATEMISSION_FINISHED:
                    return C_STATEMISSION_FINISHED
                else:
                    missionFinished = False
                    objectifs = m.getObjectifs()
                    for o in objectifs:
                        if C_OBJECTIF_TRANSPORT == o.getIdType():
                            for i in self.ship.getItemInInventory():
                                if i.getTemplate() == o.getIdItem():
                                    if i.getQuantity() >= o.getNbItem():
                                        o.setStatus(True)
                                    break

                    for o in objectifs:
                        if o.getStatus() == False:
                            missionFinished = o.getStatus()
                            break
                        else:
                            missionFinished = o.getStatus()
                    if m.getEndingNPC() != int(idNPC):
                        missionFinished = False
                    if missionFinished == True:
                        return C_STATEMISSION_SUCCESS
                    else:
                        return C_STATEMISSION_INPROGRESS

        return C_STATEMISSION_DONTHAVE
				
