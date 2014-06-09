from shimstar.core.constantes import *
from shimstar.core.decorators import *
from shimstar.core.shimconfig import *

class dialog:
	def __init__(self,id):
		self.id=id
		self.text=""
		self.typeDialog=0
		self.proba=0
		self.readonce=0
		self.parent=0
		#~ self.keywords=[]
		self.keywords={}
		#~ self.loadFromBDD()
		self.loadXml()
		
	def loadXml(self):
		dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() +"config\\dialogs.xml")
		dialogs=dom.getElementsByTagName('dialog')
		for d in dialogs:
			id=int(d.getElementsByTagName('iddialog')[0].firstChild.data)
			if id == self.id:
				self.text=d.getElementsByTagName('text')[0].firstChild.data
				self.typeDialog=int(d.getElementsByTagName('idtype')[0].firstChild.data)
				self.proba=int(d.getElementsByTagName('proba')[0].firstChild.data)
				self.readonce=int(d.getElementsByTagName('readonce')[0].firstChild.data)
				self.parent=int(d.getElementsByTagName('refdialog')[0].firstChild.data)
				keywordsXml=d.getElementsByTagName('keyword')
				for k in keywordsXml:
					label=str(k.getElementsByTagName('labelkeyword')[0].firstChild.data)
					id=int(k.getElementsByTagName('idkeyword')[0].firstChild.data)
					self.keywords[id]=label
				
	def getTypeDialog(self):
		return self.typeDialog
		
	def getParent(self):
		return self.parent
		
	def getReadOnce(self):
		return self.readonce
		
	def getId(self):
		return self.id
		
	def getProba(self):
		return self.proba
		
	def getKeywords(self):
		return self.keywords
		
	def getText(self):
		return self.text
		
	def containsKeyword(self,keyword):
		for k in self.keywords:
			if k==keyword:
				return True
				
		return False
		