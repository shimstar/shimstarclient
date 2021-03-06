import xml.dom.minidom
from math import sin, cos, pi
from math import sqrt

from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText

from shimstar.network.networkmainserver import *
from shimstar.network.message import *
from shimstar.network.netmessage import *
from shimstar.items.slot import *
from shimstar.items.engine import *
from shimstar.items.weapon import *
from shimstar.items.item import *
from shimstar.items.itemfactory import *
from shimstar.user.user import *
from shimstar.core.shimconfig import *
from shimstar.items.templates.shiptemplate import *

DEG_TO_RAD = pi / 180


class Ship:
    # ~ def __init__(self,id,xmlPart):
    listOfShip = {}
    lock = threading.Lock()

    def __init__(self, id, idTemplate, hullpoints=0, visible=True):
        # print "ship::init " + str(id) + "/" + str(idTemplate)
        Ship.lock.acquire()
        Ship.listOfShip[int(id)] = self
        Ship.lock.release()
        self.lock = threading.Lock()
        self.name = ""
        self.id = id
        self.textObject = None
        self.pousse = 0
        self.visible = visible
        self.template = idTemplate
        self.shipTemplate = None
        self.mainShip = False
        self.weapons = None
        self.engine = None
        self.actualSpeed = 0
        self.node = None
        self.img = ""
        self.owner = None  # owner obj (npc or character)
        self.group = 0
        self.mass = 0
        self.engineSound = None
        self.egg = ""
        self.lastMove = globalClock.getRealTime()
        self.hullpoints = hullpoints
        self.maxhull = 0
        self.maxTorque = 30
        self.poussee = 0
        self.currentTorqueX = 0
        self.currentTorqueY = 0
        self.itemInInventory = []
        self.lastDiffQuat = Quat(0, 0, 0, 0)
        self.oldQuat = Quat(0, 0, 0, 0)
        self.pointerToGo = loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() + "models/arrow")
        self.pointerToGo.reparentTo(render)
        self.pointerToGo.hide()
        self.pointerToGoOld = loader.loadModel(
            shimConfig.getInstance().getConvRessourceDirectory() + "models/arrow")
        self.pointerToGoOld.reparentTo(render)
        self.pointerToGoOld.hide()
        self.oldPos = (0, 0, 0)
        self.newPosition = False
        self.firstMove = False
        self.renderCounter = 0
        self.slots = []
        self.itemInInventory = []
        self.pousse = 0
        self.itemInInventory = []
        self.pyr = {'p': 0, 'y': 0, 'r': 0, 'a': 0}
        self.loadTemplate()

    #~ print "ship init" + str(self.id)


    def getItemInInventory(self):
        return self.itemInInventory

    def addItemInInventory(self, item):
        self.itemInInventory.append(item)

    def removeItemInInventory(self, item):
        self.itemInInventory.remove(item)

    def removeItemInInventoryById(self, itemId):
        itemToRemove = None
        for it in self.itemInInventory:
            if it.getId() == itemId:
                itemToRemove = it

        if itemToRemove is not None :
            self.itemInInventory.remove(itemToRemove)

    def getFirstPlaceFreeInInventory(self):
        """
            return the first place free in the inventory. The item have each a number allowing to locate it when the inventory is shown.
            This function returns first place not allocated.
        """
        places = []
        max = 0
        for i in self.itemInInventory:
            places.append(i.getLocation())
            if max < i.getLocation():
                max = i.getLocation()
        places.sort()
        returnValue = -1
        val = 0
        for p in places:
            if (val) != int(p):
                if (val) < int(p):
                    returnValue = val
                else:
                    returnValue = int(p)
                break
            val += 1

        if returnValue == -1:
            returnValue = max + 1
        return returnValue

    def getPointerToGo(self):
        return self.pointerToGo

    @staticmethod
    def getShipById(id):
        Ship.lock.acquire()
        shipToReturn = None
        if Ship.listOfShip.has_key(id) :
            shipToReturn = Ship.listOfShip[id]
        Ship.lock.release()
        return shipToReturn

    def getPoussee(self):
        return self.poussee

    def setPoussee(self, p):
        self.poussee = p

    def getLock(self):
        return self.lock

    def getTextObject(self):
        return self.textObject

    def setTextObject(self, t):
        self.textObject = t

    #~ def getPrcentHull(self):
    #~ prcent = float(self.hullpoints) / float(self.maxhull)
    #~ return float(prcent),self.hullpoints,self.maxhull

    def getPrcentSpeed(self):
        if self.engine != None:
            prcent = float(self.poussee) / float(self.engine.getSpeedMax())
            return float(prcent), self.poussee, self.engine.getSpeedMax()
        return 0,0,0


    def setOwner(self, owner):
        self.owner = owner


    def getOwner(self):
        return self.owner

    def setPosToGo(self, pos):
        self.pointerToGoOld.setPos(Vec3(self.pointerToGo.getPos()))
        self.pointerToGo.setPos(pos)
        self.newPosition = True
        self.renderCounter = 0

    def setHprToGo(self, hpr):
        self.pointerToGoOld.setQuat(Quat(self.pointerToGo.getQuat()))
        self.pointerToGo.setQuat(hpr)

    def getQuat(self):
        return self.node.getQuat()

    def move(self):
        dt = globalClock.getRealTime() - self.lastMove
        if dt > 0.01:
            if True:
                self.lock.acquire()
                try:
                    if self.node.isEmpty() != True:
                        if self.firstMove == True:
                            self.node.setPos(self.pointerToGo.getPos())
                            self.node.setQuat(self.pointerToGo.getQuat())
                            self.pointerToGoOld.setPos(self.pointerToGo.getPos())
                            self.pointerToGoOld.setQuat(self.pointerToGo.getQuat())
                            self.firstMove = False
                        else:
                            self.renderCounter += 1
                            lastPosServer = self.pointerToGo.getPos()
                            oldPosServer = self.pointerToGoOld.getPos()
                            targetPos = lastPosServer + (
                                                        lastPosServer - oldPosServer) * self.renderCounter * 1 / C_SENDTICKS * dt
                            currentPos = self.node.getPos()
                            ratioPos = currentPos * 0.95 + targetPos * 0.05  # ensure pseudo-continuous position
                            oldLinearVel = currentPos - self.oldPos
                            newLinearVel = oldLinearVel * 0.9 + (
                                                                ratioPos - currentPos) * 0.1  # ensure pseudo-continuous linear velocity

                            self.node.setPos(currentPos + newLinearVel)
                            self.oldPos = Vec3(currentPos)

                            lastQuatServer = self.pointerToGo.getQuat()
                            oldQuatServer = self.pointerToGoOld.getQuat()
                            diffQuat = Quat(lastQuatServer - oldQuatServer)

                            if diffQuat.getR() > 0.6 or diffQuat.getR() < -0.6 or diffQuat.getI() > 0.6 or diffQuat.getI() < -0.6 or diffQuat.getJ() > 0.6 or diffQuat.getJ() < -0.6 or diffQuat.getK() > 0.6 or diffQuat.getK() < -0.6:
                                lastQuatServer.setR(-lastQuatServer.getR())
                                lastQuatServer.setI(-lastQuatServer.getI())
                                lastQuatServer.setJ(-lastQuatServer.getJ())
                                lastQuatServer.setK(-lastQuatServer.getK())

                                self.pointerToGo.setQuat(lastQuatServer)

                            diffQuat = Quat(lastQuatServer - oldQuatServer)
                            self.lastDiffQuat = diffQuat

                            targetQuat = lastQuatServer + (
                                                          lastQuatServer - oldQuatServer) * self.renderCounter * 1 / C_SENDTICKS * dt
                            targetQuat.normalize()
                            currentQuat = self.node.getQuat()
                            ratioQuat = currentQuat * 0.9 + targetQuat * 0.1  # ensure pseudo-continuous rotation
                            oldAngularVel = currentQuat - self.oldQuat

                            newAngularVel = oldAngularVel * 0.925 + (
                                                                    ratioQuat - currentQuat) * 0.025  # ensure pseudo-continuous angular velocity

                            finalQuat = currentQuat + newAngularVel
                            finalQuat.normalize()
                            self.oldQuat = Quat(currentQuat)

                            self.node.setQuat(finalQuat)

                except:
                    print "exception : move in ship"

                self.lock.release()

            self.lastMove = globalClock.getRealTime()

    def loadTemplate(self):
        self.shipTemplate = ShipTemplate.getTemplate(self.template)
        self.name, self.maxhull, self.egg, self.img, self.slots = self.shipTemplate.getInfos()
        for tempSlot in self.slots:
            if tempSlot.getItem() != None:
                it = tempSlot.getItem()
                if it.getTypeItem() == C_ITEM_WEAPON:
                    self.weapons = it
                    it.setShip(self)
                if it.getTypeItem() == C_ITEM_ENGINE:
                    self.engine = it

        if self.visible == True:
            self.node = loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() + self.egg)
            self.node.reparentTo(render)
            self.node.setName("ship_" + str(self.id))
            self.node.setTag("classname", "ship")
            self.node.setTag("id", str(self.id))
            self.node.setShaderAuto()
            textObject = OnscreenText(text='my text string', parent=self.node)
            print "ship::loadTemplate " + str(self.node) + "/" + str(self.id)

    def getId(self):
        return self.id

    def getItemSlotted(self,idItem):
        for s in self.slots:
            it = s.getItem()
            if it is not None:
                if it.getId() == idItem:
                    return it

        return None

    def getItemFromInventory(self, id):
        for it in self.itemInInventory:
            if it.getId() == id:
                return it
        return None


    def getFirstPlaceFreeInInventory(self):
        """
            return the first place free in the inventory. The item have each a number allowing to locate it when the inventory is shown.
            This function returns first place not allocated.
        """
        places = []
        max = 0
        for i in self.itemInInventory:
            places.append(i.getLocation())
            if max < i.getLocation():
                max = i.getLocation()
        places.sort()
        returnValue = -1
        val = 0
        for p in places:
            if (val) != int(p):
                if (val) < int(p):
                    returnValue = val
                else:
                    returnValue = int(p)
                break
            val += 1

        if returnValue == -1:
            returnValue = max + 1
        return returnValue

    def uninstallItemBySlotId(self, slotId):
        for s in self.slots:
            if s.getId() == int(slotId):
                self.uninstallItem(s)
                break

    def getItemInstalledByCategory(self, cat):
        items = []
        for it in self.items:
            if it.getTypeItem() == cat:
                items.append(it)
        return items

    def uninstallItem(self, slot):
        itemUninstalled=slot.getItem()
        if itemUninstalled is not None:
            self.itemInInventory.append(slot.getItem())

            slot.setItem(None)
            msg = netMessage(C_NETWORK_CHARACTER_UNINSTALL_SLOT)
            msg.addUInt(self.owner.userRef.id)
            msg.addUInt(slot.getId())
            NetworkMainServer.getInstance().sendMessage(msg)
            if itemUninstalled.getTypeItem() == C_ITEM_WEAPON:
                self.weapons = None
            if itemUninstalled.getTypeItem() == C_ITEM_ENGINE:
                self.engine = None

    def removeTemplateSlots(self):
        self.slots = []

    def installItem(self, item, slot):
        slotToInstall = slot
        if slotToInstall != None:
            if slotToInstall.getItem() != None:
                self.uninstallItem(slotToInstall)

            itemToInstall = item
            if itemToInstall != None:
                slotToInstall.setItem(itemToInstall)
                self.itemInInventory.remove(itemToInstall)

                msg = netMessage(C_NETWORK_CHARACTER_INSTALL_SLOT)
                msg.addUInt(self.owner.userRef.id)
                msg.addUInt(slotToInstall.getId())
                msg.addUInt(itemToInstall.getId())
                NetworkMainServer.getInstance().sendMessage(msg)
                if itemToInstall.getTypeItem() == C_ITEM_WEAPON:
                    self.weapons = itemToInstall
                if itemToInstall.getTypeItem() == C_ITEM_ENGINE:
                    self.engine = itemToInstall

    def addMinerals(self, id, typeMineral, qt):
        alreadyGot = False
        for i in self.itemInInventory:
            if i.getTypeItem() == C_ITEM_MINERAL:
                if i.getId() == id:
                    i.addMineral(qt)
                    alreadyGot = True
                    break

        if alreadyGot == False:
            newItem = Mineral(typeMineral)
            newItem.addMineral(qt)
            newItem.setId(id)
            self.itemInInventory.append(newItem)

    def removeMinerals(self, id, qt):
        for i in self.itemInInventory:
            if i.getTypeItem() == C_ITEM_MINERAL:
                if i.getId() == id:
                    i.removeMineral(qt)
                    break

    def getSlots(self):
        return self.slots

    def getWeapon(self):
        return self.weapons

    def changeZone(self):
        self.actualSpeed = 0

    def getPos(self):
        return self.node.getPos()

    def setPos(self, pos):
        self.lock.acquire()
        self.node.setPos(pos)
        self.lock.release()

    def setQuat(self, quat):
        self.lock.acquire()
        self.node.setQuat(quat)
        self.lock.release()

    def getNode(self):
        return self.node

    def getName(self):
        return self.name

    def getImg(self):
        return self.img

    def setVisible(self):
        self.node.show()

    def setInvisible(self):
        print "ship::setInvisibleA " + str(self.node)
        if self.node == None:
            self.node = loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() + self.egg)
            self.node.reparentTo(render)
            self.node.setShaderAuto()
            self.node.setName("ship_" + str(self.id))
            self.node.setTag("classname", "ship")
            self.node.setTag("id", str(self.id))
        self.node.hide()

        print "ship::setInvisible " + str(self.id) + "/" + str(self.node)

    def isHidden(self):
        return self.node.isHidden()

    def getSpeed(self):
        return self.actualSpeed

    def getSpeedMax(self):
        return self.engine.getSpeedMax()

    def addBullet(self, bulId, pos, quat):
        if self.weapons != None:
            self.weapons.addBullet(bulId, pos, quat)

    def shot(self):
        if self.weapons != None:
            return self.weapons.shot(self.node.getPos(), self.node.getQuat())
        return None

    def destroy(self):
        self.lock.acquire()
        try:
            self.node.detachNode()
            self.node.removeNode()
            print "ship::destroy " + str(self.id)
            if self.textObject != None:
                self.textObject.detachNode()
                self.textObject.removeNode()
        except:
            print "exception : destroy node in ship"

        self.lock.release()

        Ship.lock.acquire()
        if Ship.listOfShip.has_key(self.id):
            del Ship.listOfShip[self.id]
        Ship.lock.release()


    def getPrcentHull(self):
        prcent = float(self.hullpoints) / float(self.maxhull)
        return float(prcent), self.hullpoints, self.maxhull


    def getPrcentShield(self):
        listOfShield = self.hasItems(C_ITEM_SHIELD)
        shHP = 0
        shHPMax = 0
        prcent = 0
        for n in listOfShield :
            shHP += n.getHitPoints()
            shHPMax += n.getMaxHitpoints()

        if shHPMax>0:
            prcent = float(shHP) / float(shHPMax)
        return float(prcent), shHP, shHPMax

    def getMaxHullPoints(self):
        return self.maxhull

    ## Return True if ship has hull>0
    ## Return False if shup has hull<=0
    def takeDamage(self, hitpoints):
        self.hullpoints -= hitpoints
        if self.hullpoints <= 0:
            #~ self.setVisible(False)
            return False
        return True

    def getHullPoints(self):
        return self.hullpoints

    def setHullPoints(self,hp):
        self.hullpoints = hp

    def addSlot(self, s):
        self.slots.append(s)
        it=s.getItem()
        if it is not None:
            if it.getTypeItem() == C_ITEM_WEAPON:
                self.weapons = it
            if it.getTypeItem() == C_ITEM_ENGINE:
                self.engine = it

    def hasItems(self,typeItem):
        listOfItem = []
        for s in self.slots:
            it = s.getItem()
            if it is not None:
                if it.getTypeItem() == typeItem:
                    listOfItem.append(it)

        return listOfItem