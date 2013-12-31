# -*- coding: utf-8 -*- 
import sys,os
from panda3d.rocket import *
from shimstar.gui.shimrocket import *
from shimstar.user.user import *
from shimstar.core.shimconfig import *
from shimstar.core.functions import *
from shimstar.gui.core.configuration import *
from shimstar.gui.game.follower import *
from shimstar.world.zone.asteroid import *
from shimstar.core.constantes import *


class rocketTarget():
	instance=None
	def __init__(self):
		#~ print "rocketTarget::init"
		rocketTarget.instance=self
		self.context = shimRocket.getInstance().getContext()
		self.window = self.context.LoadDocument('windows/target.rml')
		self.window.AddEventListener("click","shot()")
		self.info=self.context.LoadDocument("windows/info.rml")
		self.obj=None
		self.miningItemFitted=None
		self.lastCalcDistance=0
		self.lastRender=0
		self.distance=0

		
	@staticmethod
	def getInstance():
		if rocketTarget.instance==None:
			rocketTarget()
		return rocketTarget.instance
		
	def collect(self):
		rocketCollect.getInstance().showWindow(self.obj)
		
	def showWindow(self,obj):
		#~ print "rocketTarget::showWindow"
		#~ needTuto=User.getInstance().getCurrentCharacter().hasTuto(C_TUTO_TARGET)
		#~ if needTuto==False:
			#~ rocketTutos.getInstance().showWindow(C_TUTO_TARGET)
		self.window.Show()
		self.obj=obj
		b=self.window.GetElementById("pg")
		if isinstance(obj,Ship)==True:
			b.SetAttribute("style","display:Block;")
		else:
			b.SetAttribute("style","display:None;")
		if isinstance(self.obj,Asteroid):
			b=self.window.GetElementById('divmine')
			b.SetAttribute("style","display:Block;")
			b=self.window.GetElementById('divgate')
			b.SetAttribute("style","display:None;")
			slots=User.getInstance().getCurrentCharacter().getShip().getSlots()
			self.miningItemFitted=None
			for s in slots:
				if s.getItem()!=None:
					if s.getItem().getTypeItem()==C_ITEM_MINING:
						self.miningItemFitted=s.getItem()
						break
						
		else:
			b=self.window.GetElementById('divmine')
			b.SetAttribute("style","display:None;")
		
		Follower.getInstance().setTarget(obj.getNode())
		self.showInfo()
		return self.window
		
	def map3dToAspect2d(self, node, point): 
		"""Maps the indicated 3-d point (a Point3), which is relative to 
		the indicated NodePath, to the corresponding point in the aspect2d 
		scene graph. Returns the corresponding Point3 in aspect2d. 
		Returns None if the point is not onscreen. """ 

		# Convert the point to the 3-d space of the camera 
		p3 = base.cam.getRelativePoint(node, point) 

		# Convert it through the lens to render2d coordinates 
		p2 = Point2() 
		if not base.camLens.project(p3, p2): 
			return None 

		r2d = Point3(p2[0], 0, p2[1]) 

		# And then convert it to aspect2d coordinates 
		a2d = aspect2d.getRelativePoint(render2d, r2d) 

		return a2d
		
		
	def emptyContentMineral(self):
		content=self.info.GetElementById("contentinfoitem")
		
		listOfActualDiv=content.GetElementsByTagName("div")
		for div in listOfActualDiv:
			content.RemoveChild(div)
		
	def showInfo(self):
		self.emptyContentMineral()
		if isinstance(self.obj,Asteroid):
			id=self.info.GetElementById("idobj")
			id.value=str(self.obj.getId())
			id=self.info.GetElementById("typeobj")
			id.value=str("asteroid")
			name=self.info.GetElementById("name")
			name.inner_rml=self.obj.getName()
			btnEnter=self.info.GetElementById("enterdiv")
			btnEnter.SetAttribute("style","position:absolute;top:170px;left:-0px;display:None;")
			content=self.info.GetElementById("contentinfoitem")
			listOfActualDiv=content.GetElementsByTagName("div")
			for div in listOfActualDiv:
				content.RemoveChild(div)
			minerals=self.obj.getMinerals()
			i=0
			for m in minerals:
				itMineral=mineral(m)
				div=self.info.CreateElement("div")
				div.SetAttribute("style","position:absolute;top:170px;left:" + str(30+i*40) + "px;width:32x;")
				el=self.info.CreateElement("img")
				itImg=itMineral.getImg()
				img=shimConfig.getInstance().getRessourceDirectory() + "images\\items\\" + itImg+ ".png"
				el.SetAttribute("width","32")
				el.SetAttribute("height","32")
				el.SetAttribute("src",str(img))
				div.AppendChild(el)
				content.AppendChild(div)
				div=self.info.CreateElement("div")
				div.SetAttribute("style","position:absolute;top:200px;left:" + str(-50+i*40) + "px;")
				but=self.info.CreateElement("button")
				but.SetAttribute("class","roundleft")
				but.SetAttribute("id","nbmin" + str(m))
				but.SetAttribute("style","width:60px;height:20px;font-size: 10;")
				but.inner_rml=str(minerals[m])
				div.AppendChild(but)
				content.AppendChild(div)
				i+=1
		#~ elif isinstance(self.obj,wormhole):			
			#~ id=self.info.GetElementById("idobj")
			#~ id.value=str(self.obj.getId())
			#~ id=self.info.GetElementById("typeobj")
			#~ id.value=str("station")
			#~ name=self.info.GetElementById("name")
			#~ name.inner_rml=self.obj.getName()
			#~ btnEnter=self.info.GetElementById("enterdiv")
			#~ btnEnter.SetAttribute("style","position:absolute;top:170px;left:-0px;display:None;")
			
		#~ elif isinstance(self.obj,station):			
			#~ id=self.info.GetElementById("idobj")
			#~ id.value=str(self.obj.getId())
			#~ id=self.info.GetElementById("typeobj")
			#~ id.value=str("station")
			#~ name=self.info.GetElementById("name")
			#~ name.inner_rml=self.obj.getName()
			#~ btnEnter=self.info.GetElementById("enterdiv")
			#~ btnEnter.SetAttribute("style","position:absolute;top:170px;left:-0px;display:Block;")
		elif isinstance(self.obj,Ship):
			#~ btnEnter=self.info.GetElementById("enterdiv")
			#~ btnEnter.SetAttribute("style","position:absolute;top:170px;left:-0px;display:None;")
			id=self.info.GetElementById("idobj")
			id.value=str(self.obj.getId())
			name=self.info.GetElementById("name")
			name.inner_rml=str(self.obj.getOwner().getName())
			img=self.info.GetElementById("imgobj")
			img.SetAttribute("src",shimConfig.getInstance().getRessourceDirectory() + "images\\items\\" + self.obj.getImg() )
			
		self.info.Show()
		
	def render(self):
		if self.obj!=None:
				if self.obj.getNode().isEmpty()==False and self.obj.getNode()!=None:
					#~ print self.obj.getNode().getPos()
					if globalClock.getRealTime()-self.lastCalcDistance>0.1:
						self.lastCalcDistance=globalClock.getRealTime()
						self.distance=calcDistance(self.obj.getNode(),User.getInstance().getCurrentCharacter().getShip().getNode())
					distanceEle=self.info.GetElementById("distance")
					distanceEle.inner_rml="distance : " + str(self.distance) + " m"
					if isInView(self.obj.getNode())==True: 
						if globalClock.getRealTime()-self.lastRender>0.03:
							self.lastRender=globalClock.getRealTime()
							self.window.Show()
							pos=self.map3dToAspect2d(render,self.obj.getNode().getPos(render))
							x=pos.getX()
							z=pos.getZ()
							z+=1
							z=C_USER_HEIGHT-(z*C_USER_HEIGHT/2)-30
							x+=C_RATIO
							x=(x*C_USER_WIDTH/(C_RATIO*2))-30
									
							distEle=self.window.GetElementById("distance")
							distEle.inner_rml=str(self.distance)
							
							self.window.SetAttribute("style","body{width:300px;height:250px;top:" + str(z) + "px;left:" + str(x) + "px;}")
							if isinstance(self.obj,Ship)==True:
								w=User.getInstance().getCurrentCharacter().getShip().getWeapon()
								b=self.window.GetElementById('target')
								if w!=None:
									if w.getRange()>=self.distance:
										b.SetAttribute("src",shimConfig.getInstance().getRessourceDirectory() + "images\\gui\\targetred.png")
									else:
										b.SetAttribute("src",shimConfig.getInstance().getRessourceDirectory() + "images\\gui\\target.png")
								else:
									b.SetAttribute("src",shimConfig.getInstance().getRessourceDirectory() + "images\\gui\\target.png")
								hp=self.obj.getHullPoints()
								hpmax=self.obj.getMaxHullPoints()
								
								prcent=int(100*round(float(hp)/float(hpmax),1))
								if prcent<0:
									prcent=0
								img=self.window.GetElementById("pg")
								img.SetAttribute("src",shimConfig.getInstance().getRessourceDirectory() + "\\images\\gui\\pgb" + str(prcent) + ".png")
								
								nameEle=self.window.GetElementById("name")
								nameEle.inner_rml=str(self.obj.getOwner().getName())
								
							else:
								nameEle=self.window.GetElementById("name")
								nameEle.inner_rml=str(self.obj.getName())
						
						
						if isinstance(self.obj,Asteroid):
							b=self.window.GetElementById('mine')
							if self.miningItemFitted!=None:
								if self.miningItemFitted.getRange()>=self.distance:
									b.SetAttribute("src",shimConfig.getInstance().getRessourceDirectory() + "images\\gui\\shovel.png")
								else:
									b.SetAttribute("src",shimConfig.getInstance().getRessourceDirectory() + "images\\gui\\shovelko.png")
							else:
								b.SetAttribute("src",shimConfig.getInstance().getRessourceDirectory() + "images\\gui\\shovelko.png")					
						#~ elif isinstance(self.obj,wormhole):
							#~ b=self.window.GetElementById('gate')
							#~ b.SetAttribute("src",shimConfig.getInstance().getRessourceDirectory() + "images\\gui\\wormhole.png")
					else:
						self.window.Hide()
				else:
					self.window.Hide()
		else:
			self.window.Hide()

		
	def hideWindow(self):
		self.window.Hide()
		
	def destroy(self):
		self.context.UnloadDocument(self.window)
		