C_INIT=0
C_MENUCONNECT=1
C_GOPLAY=2
C_PLAYING=3
C_CHANGEZONE=4
C_ENTERSTATION=5
C_QUIT=6
C_CHOOSE_HERO=7
C_CHOOSING_HERO=8
C_MENUCREATEACCOUNT=9
C_MENUCREATINGACCOUNT=10
C_DEATH=11
C_DEATH_WAITING=12
C_DEATH_WAITING_VALIDATION=13
C_SERVER_DOWN=14
C_SERVER_DOWN_WAITING=15
C_WAITING_INFOZONE=16
C_RECEIVED_INFOZONE=17
C_WAITING_LOADINGZONE=18
C_WAITING_ASKING_INFO_NPC=19
C_WAITING_INFO_NPC=20
C_WAITING_INFO_CHARACTER=21
C_WAITING_ASKING_INFO_CHARACTER=22
C_WAITING_NPC_RECEIVED=23
C_WAITING_CHARACTER_RECEIVED=24


class GameState:
	instance=None
	def __init__(self):
		self.state=C_INIT
		GameState.instance=self
		self.idZone=0
		
	def getNewZone(self):
		return self.idZone
		
	def setNewZone(self,id):
		self.idZone=id

	def getState(self):
		return self.state
		
	def setState(self,state):
		self.state=state
		
	@staticmethod
	def getInstance():
		if GameState.instance==None:
			GameState.instance=GameState()
		return GameState.instance