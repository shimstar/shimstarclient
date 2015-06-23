from shimstar.core.decorators import *

class Reward:
	def __init__(self,id,typeReward,templateItem,nbItem):
		self.id=id
		self.typeReward=typeReward
		self.templateItem=templateItem
		self.nb=nbItem
		
	def getId(self):
		return self.id
		
	def getTypeReward(self):
		return self.typeReward
		
	def getTemplateItem(self):
		return self.templateItem
		
	def getNb(self):
		return self.nb
		
