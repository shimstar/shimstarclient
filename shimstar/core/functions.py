# -*- coding: iso-8859-1 -*-
from pandac.PandaModules import *

from math import sqrt

def isInView(obj, camnode=None, cam=None): 
		if camnode is None: 
				camnode = base.camNode 
		if cam is None: 
				cam =  base.cam 

		return camnode.isInView(obj.getPos(cam)) 


def sign(number): 
    return number / abs(number) if number != 0 else 0 

def transFormHtml(text):
	
	text=text.replace('\\r','<br/>')
	text=text.replace('\\n','<br/>')
	text=text.replace('\\1n','<br/>')
	text=text.replace('\\2n','<br/><br/>')
	#~ text=text.encode('iso-8859-1') 
	text=text.encode('utf-8')
	#~ text=text.replace('é','&eacute;')
	#~ text=text.replace('è','&egrave;')
	#~ text=text.replace('à','&Aagrave;')
	#~ text=text.replace('î','&Icirc;')
	#~ text=text.replace('ê','&Ecirc;')
	#~ print text
	return text
	
	#~ text.encode('iso-8859-1') 

def calcDistance(node1,node2):
		pos1=node1.getPos()
		pos2=node2.getPos()
		dx=pos1.getX()-pos2.getX()
		dy=pos1.getY()-pos2.getY()
		dz=pos1.getZ()-pos2.getZ()
		distance=int(round(sqrt(dx*dx+dy*dy+dz*dz),0))
		return distance