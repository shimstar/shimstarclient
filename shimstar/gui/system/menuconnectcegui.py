# -*- coding: utf-8 -*- 
import sys,os
from string import *
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.distributed.PyDatagram import PyDatagram 
from direct.distributed.PyDatagramIterator import PyDatagramIterator 
from direct.gui.DirectFrame import DirectFrame
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from direct.task import Task
from direct.showbase.ShowBase import ShowBase 
from shimstar.network.networkmainserver import *
import PyCEGUI
from shimstar.gui.shimcegui import * 
from shimstar.game.gamestate import *
from shimstar.user.user import *
from shimstar.network.netmessage import *
from shimstar.core.shimconfig import *

C_MENUCONNECT_WAITING=1

def setText(textEntered):
	textObject.setText(textEntered)

class MenuConnectCegui(ShowBase):
	def __init__(self):
		self.focuson=0
		self.CEGUI=ShimCEGUI.getInstance()
		self.setupUI()
		self.btnConnect=self.CEGUI.WindowManager.getWindow("MenuConnect/Login/ButtonEnter")
		self.lastConnectSend=globalClock.getRealTime()
		self.btnNew=self.CEGUI.WindowManager.getWindow("MenuConnect/Login/ButtonNew")

		self.userEdit=self.CEGUI.WindowManager.getWindow("MenuConnect/Login/EditboxLogin")
		self.userEdit.setText(shimConfig.getInstance().getUser())
		self.userEdit.activate()
		self.pwdEdit=self.CEGUI.WindowManager.getWindow("MenuConnect/Login/EditboxPass")
		self.pwdEdit.setTextMasked(True)
		self.pwdEdit.setText(shimConfig.getInstance().getPwd())
		self.statusEdit=self.CEGUI.WindowManager.getWindow("MenuConnect/Login/LabelStatus")
		taskMgr.add(self.event,"event reader menu connect",-40)  
		self.stateConnexion=0
		
		self.buttonSound= base.loader.loadSfx(shimConfig.getInstance().getConvRessourceDirectory() + "sounds/Buttton_press3.ogg")
		self.buttonSound2= base.loader.loadSfx(shimConfig.getInstance().getConvRessourceDirectory() + "sounds/Buttton_press1.ogg")
		self.buttonSound.setVolume(shimConfig.getInstance().getSoundVolume())
		self.buttonSound2.setVolume(shimConfig.getInstance().getSoundVolume())
		
		self.accept("tab",self.tab)
		self.accept("escape",self.quitGame)
		self.accept("enter",self.connect, [0])
		
		if NetworkMainServer.getInstance().isConnected()==False:
			self.statusEdit.setText("Server : [colour='FFFF0000']Offline")
			self.btnConnect.setText("[colour='FFFF0000']Connect")
			self.btnConnect.disable()
			self.btnNew.disable()
			#~ #TODO disable connect/create button.
		else:
			self.statusEdit.setText("Server : [colour='FF00FF00']Online")
			self.btnConnect.setText("Connect")
		self.CEGUI.enable() 
		
	def setupUI(self):
		#  Chargement des sch?s
		self.CEGUI.SchemeManager.create("TaharezLook.scheme") 
		self.CEGUI.SchemeManager.create("shimstar.scheme") 
		self.CEGUI.System.setDefaultMouseCursor("ShimstarImageset", "MouseArrow") 
		self.CEGUI.System.setDefaultFont("Brassiere-m")
		self.root = self.CEGUI.WindowManager.loadWindowLayout("welcome.layout") 
		#~ self.CEGUI.ImageSetManager.createFromImageFile("MenuConnect/Background", "backmenuconnect.jpg", "imagesets")
		customImageset = self.CEGUI.ImageSetManager.createFromImageFile("TempImageset", "background/backmenuconnect.jpg", "images")
		self.CEGUI.WindowManager.getWindow("MenuConnect/Background").setProperty("BackgroundImage", "set:TempImageset image:full_image")
		self.CEGUI.System.setGUISheet(self.root) 
		
		# ------------
		#  Animations
		# ------------
		#  Chargement du XML
		self.CEGUI.AnimationManager.loadAnimationsFromXML("shimstar.anim.xml", "animations")
		
		#  Cr?ion des instances
		self.OutLoginAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
		self.InLoginAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
		self.OutNewAccountAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
		self.InNewAccountAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
		self.OutNewAccountReportAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
		self.InNewAccountReportAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
		self.OutLoginReportAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowOut")
		self.InLoginReportAnimationInstance = self.CEGUI.AnimationManager.instantiateAnimation("WindowIn")
		
		#  Affectation des instances ?eurs fen?es respectives
		self.OutLoginAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("MenuConnect/Login"))
		self.InLoginAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("MenuConnect/Login"))
		self.OutNewAccountAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccount"))
		self.InNewAccountAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccount"))
		self.OutNewAccountReportAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccountReport"))
		self.InNewAccountReportAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccountReport"))
		self.OutLoginReportAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("MenuConnect/LoginReport"))
		self.InLoginReportAnimationInstance.setTargetWindow(self.CEGUI.WindowManager.getWindow("MenuConnect/LoginReport"))
		
		#  Ev?ments
		self.CEGUI.WindowManager.getWindow("MenuConnect/Login/ButtonEnter").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'connect')
		self.CEGUI.WindowManager.getWindow("MenuConnect/Login/ButtonNew").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'ButtonClicked')
		self.CEGUI.WindowManager.getWindow("MenuConnect/LoginReport/ButtonOK").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'ButtonClicked')
		self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccount/ButtonCreate").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'createAccount')
		self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccount/ButtonCancel").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'ButtonClicked')
		self.CEGUI.WindowManager.getWindow("MenuConnect/Login/ButtonEnter").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'connect')
	
	def ButtonClicked(self,windowEventArgs):
		self.buttonSound.play()
		if (windowEventArgs.window.getName() == "MenuConnect/LoginReport/ButtonOK"):
			self.OutLoginReportAnimationInstance.start()
			self.InLoginAnimationInstance.start()
			self.userEdit.activate()
		elif (windowEventArgs.window.getName() == "MenuConnect/Login/ButtonNew"):
			#  User wants to create a new account
			self.OutLoginAnimationInstance.start()
			self.InNewAccountAnimationInstance.start()
			self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccount/EditboxLogin").activate()
		elif (windowEventArgs.window.getName() == "MenuConnect/NewAccount/ButtonCancel"):
			#  Cancel creation of a new account --> go back to login
			self.OutNewAccountAnimationInstance.start()
			self.InLoginAnimationInstance.start()
			self.userEdit.activate()
		elif (windowEventArgs.window.getName() == "MenuConnect/NewAccountReport/ButtonOK"):
				#  User has seen the report --> go back to login
				self.OutNewAccountReportAnimationInstance.start()
				self.InNewAccountAnimationInstance.start()
				
	def tab(self):
		if self.userEdit.isActive()==True:
			self.pwdEdit.activate()
		elif self.pwdEdit.isActive():
			self.userEdit.activate()
		elif self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccount/EditboxLogin").isActive()==True:
			self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccount/EditboxPass").activate()
		elif self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccount/EditboxPass").isActive()==True:
			self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccount/EditboxLogin").activate()
		
	def quitGame(self,):
		GameState.getInstance().setState(C_QUIT_MENU)

	def event(self,arg):
		if(self.stateConnexion==C_MENUCONNECT_WAITING):
			temp=NetworkMainServer.getInstance().getListOfMessageById(C_NETWORK_CONNECT)
			if(len(temp)>0):
				msg=temp[0]
				netMsg=msg.getMessage()
				state=int(netMsg[0])
				NetworkMainServer.getInstance().removeMessage(msg)
				if state==0:
					User(netMsg[1],netMsg[2],True)
					for i in range (netMsg[3]):
						User.getInstance().addCharacter(netMsg[4+(4*i)],netMsg[5+(4*i)],netMsg[6+(4*i)],netMsg[7+(4*i)]);
					GameState.getInstance().setState(C_CHOOSE_HERO)
					usr=self.userEdit.getText()
					pwd=self.pwdEdit.getText()
					shimConfig.getInstance().setUser(usr)
					shimConfig.getInstance().setPwd(pwd)
					shimConfig.getInstance().saveConfig()
					return Task.done
				else:
					self.btnConnect.enable()
					self.btnConnect.setText("Connect")
					self.OutLoginAnimationInstance.start();
					self.OutNewAccountAnimationInstance.start();
					self.InLoginReportAnimationInstance.start();
					if state==1:
						errorMsg="Ce compte n'existe pas"
					elif state==2:
						errorMsg="Mauvais password"
					elif state==3:
						errorMsg="Compte deja en utilisation"
					self.CEGUI.WindowManager.getWindow("MenuConnect/LoginReport/LabelReport").setText(errorMsg)
		elif(self.stateConnexion==C_MENUCREATINGACCOUNT):
			temp=NetworkMainServer.getInstance().getListOfMessageById(C_CREATE_USER)
			if(len(temp)>0):
				for msg in temp:
					netMsg=msg.getMessage()
					state=int(netMsg[0])
					if state==1:					
						self.OutNewAccountAnimationInstance.start();
						self.InNewAccountReportAnimationInstance.start();
						self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccountReport/LabelReport").setText("Votre compte a bien ete cree")
						self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccountReport/ButtonOK").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'connectNewAccount')
						#~ return Task.done
					else:
						self.OutNewAccountAnimationInstance.start();
						self.InNewAccountReportAnimationInstance.start();
						self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccountReport/LabelReport").setText("Ce compte existe deja")
						self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccountReport/ButtonOK").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'ButtonClicked')
					NetworkMainServer.getInstance().removeMessage(msg)
				
		return Task.cont
		
	def createAccount(self,windowEventArgs):
		user=self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccount/EditboxLogin").getText()
		pwd=self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccount/EditboxPass").getText()
		self.stateConnexion=C_MENUCREATINGACCOUNT
		msg=netMessage(C_CREATE_USER)
		msg.addString(user)
		msg.addString(pwd)
		NetworkMainServer.getInstance().sendMessage(msg)
		
	def connectNewAccount(self,windowEventArgs):
		self.user=self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccount/EditboxLogin").getText()
		self.userEdit.setText(self.user)
		self.pwd=self.CEGUI.WindowManager.getWindow("MenuConnect/NewAccount/EditboxPass").getText()
		self.pwdEdit.setText(self.pwd)
		self.OutNewAccountReportAnimationInstance.start();
		self.InLoginAnimationInstance.start()
		
	def connect(self,windowEventArgs):
		self.buttonSound2.play()
		if NetworkMainServer.getInstance().isConnected()!=False:
		#~ if network.reference.isConnected()!=False:
			#~ actual=globalClock.getRealTime()
			#~ if actual-self.lastConnectSend>0.1:
				#~ self.lastConnectSend=globalClock.getRealTime()
			user=self.userEdit.getText()
			pwd=self.pwdEdit.getText()
				#~ network.reference.sendMessage(C_CONNECT,user+"/"+pwd)
			self.stateConnexion=C_MENUCONNECT_WAITING
			msg=netMessage(C_NETWORK_CONNECT)
			msg.addString(user)
			msg.addString(pwd)
			NetworkMainServer.getInstance().sendMessage(msg)
			self.btnConnect.disable()
			self.btnConnect.setText("[colour='FF00FF00']Connexion...")
			
	def destroy(self):
		taskMgr.remove("event reader menu connect")
		self.CEGUI.WindowManager.destroyWindow(self.root)
		self.ignore("enter")
		self.ignore("escape")