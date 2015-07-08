from pandac.PandaModules import * 
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.task import Task
from shimstar.world.zone.zone import *
from shimstar.npc.npc import *
from shimstar.items.radaritem import *
from shimstar.constantes import *

class radar:
  instance=None
  def __init__(self,parent):
    radar.instance=self
    self.ships=[]
    self.users=[]
    self.asteroids=[]
    self.worm=[]
    self.dots=[]
    self.dotsAster=[]
    self.dotsUsers=[]
    self.dotsWorm=[]
    self.scale = 100
    self.parent=parent
    self.pointer = self.parent.attachNewNode('Pointer')
    self.map = aspect2d.attachNewNode('Map')
    props = base.win.getProperties( )
    self.Height = float(props.getYSize())
    self.Hscale = (1/self.Height)
    self.radarItem=user.instance.getCurrentCharacter().getShip().getItemInstalledByCategory(C_ITEM_RADAR)[0]
    self.distance=self.radarItem.getDistance()
    self.widthEye=90
    self.map.setScale(self.Hscale)  #Sets scale to the screen resolution.
    self.map.setPos(Vec3(-.95,0,-.70)) #this is the location on aspect2d for the minimap. 
    self.image = OnscreenImage(image = "models/map.png", scale = 100, parent = self.map)
  
    self.image.setTransparency(TransparencyAttrib.MAlpha)
    
    self.stepTask = taskMgr.add(self.step,"MinimapTask")
  
  def destroy(self):
    taskMgr.remove("MinimapTask")
    self.pointer.detachNode()
    self.pointer.removeNode()
    self.image.detachNode()
    self.image.removeNode()
    self.map.detachNode()
    self.map.removeNode()
  
  def removeShip(self,ship):
    index=self.ships.index(ship)
    self.ships.remove(ship)
    dot=self.dots[index]
    self.dots.remove(dot)
    dot.destroy()
    
  def addShip(self,ship):
    self.ships.append(ship)
    dot= OnscreenImage(image ="models/dot.png", scale = 8 ,pos = (0,0,1), parent = self.map)
    dot.setTag("name",ship.getName())
    self.dots.append(dot)
    dot.setTransparency(TransparencyAttrib.MAlpha)
  
  def removeUser(self,ship):
    index=self.users.index(ship)
    self.users.remove(ship)
    dot=self.dotsUsers[index]
    self.dotsUsers.remove(dot)
    dot.destroy()  
  
  def addUser(self,ship):
    self.users.append(ship)
    dot= OnscreenImage(image ="models/dot2.png", scale = 8 ,pos = (0,0,1), parent = self.map)
    dot.setTag("name",ship.getName())
    self.dotsUsers.append(dot)
    dot.setTransparency(TransparencyAttrib.MAlpha)
  
  def initRadarWithZone(self,zone):
    listOfNpc=zone.getListOfNPC()
    for npc in listOfNpc:
      ship=npc.getShip()
      self.addShip(ship)
    asteroids=zone.getListOfAsteroids()
    for aster in asteroids:
      self.addAsteroid(aster)
    worms=zone.getListOfWormHole()
    for worm in worms:
      self.addWorm(worm)
  
  
  def addAsteroid(self,aster):
    self.asteroids.append(aster)
    dot= OnscreenImage(image ="models/dotmarron.png", scale = 3 ,pos = (0,0,1), parent = self.map)
    dot.setTag("name",aster.getName())
    self.dotsAster.append(dot)
    dot.setTransparency(TransparencyAttrib.MAlpha)
  
  def addWorm(self,worm):
    self.worm.append(worm)
    dot= OnscreenImage(image ="models/dotpink.png", scale = 3 ,pos = (0,0,1), parent = self.map)
    dot.setTag("name",worm.getName())
    self.dotsWorm.append(dot)
    dot.setTransparency(TransparencyAttrib.MAlpha)
  
  def calcDistance(self,node):
    posShip=self.parent.getPos()
    posItem=node.getPos()
    dx=posShip.getX()-posItem.getX()
    dy=posShip.getY()-posItem.getY()
    dz=posShip.getZ()-posItem.getZ()
    distance=int(round(sqrt(dx*dx+dy*dy+dz*dz),0))
    return distance
  
  def setDots(self,obj,dot):
    self.pointer.lookAt(obj)
    pH=self.pointer.getH()
    pP=self.pointer.getP()
    if pH > self.widthEye or pH < -self.widthEye: #This means that the object is behind us, we don't want to process this object.					
      dot.hide()
    elif pP > self.widthEye or pP < -self.widthEye:
      dot.hide()
    else:
      dot.show()
      x = (pH/-self.widthEye) * self.scale #this will give a value between 1 and -1
      y = 0
      z = (pP/self.widthEye) * self.scale#this will give a value between 1 and -1
      
      distance=self.calcDistance(obj)
      
      if distance>0:
        if distance > self.distance:
          dot.hide()
        else:
          scale=8-(float(distance)/float(self.distance)*8)
          if scale > 0:
            dot.setScale(scale)
      dot.setPos(x,y,z)

  def step(self,task):
    for i in range(len(self.ships)):
      self.setDots(self.ships[i].getNode(),self.dots[i])
    
    for i in range(len(self.asteroids)):
      self.setDots(self.asteroids[i].getObj(),self.dotsAster[i])
      
    for i in range(len(self.users)):
      self.setDots(self.users[i].getNode(),self.dotsUsers[i])
    
    for i in range(len(self.worm)):
      self.setDots(self.worm[i].getObj(),self.dotsWorm[i])
    
    return Task.cont