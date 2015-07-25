from direct.showbase.ShowBase import ShowBase
from shimstar.core.shimconfig import *
from shimstar.core.functions import *


class Follower(object):
    """Onscreen indicator for relationship of a node relative to the camera.
    Shows an indicator at the edge of the screen if target is not in view."""
    instance = None

    def __init__(self):
        """Arguments:
        target -- nodepath to follow
        """
        self.target = None
        self.pointer = loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() + "models/arrow")
        self.pointer.setScale(0.01)
        self.pointer.setColor(1, 0, 0, 1)
        self.pointer.reparentTo(base.aspect2d)
        self.pointer.hide()
        self.task = taskMgr.add(self.track, "onscreen follower")
        self.active = False

    @staticmethod
    def getInstance():
        if Follower.instance == None:
            Follower.instance = Follower()
        return Follower.instance


    @staticmethod
    def isInstantiated():
        if MenuSelectTarget.instance is not None:
            return True
        return False

    def setTarget(self, target):
        self.target = target
        self.active = True

    def getTarget(self):
        return self.target

    def track(self, task):
        if self.target != None and not self.target.isEmpty():
            if isInView(self.target):
                self.pointer.hide()

            else:
                self.pointer.show()
                x, y, z = self.target.getPos(base.cam)
                if abs(x) > abs(z):
                    z /= abs(x) if x != 0 else 1
                    x = sign(x)
                else:
                    x /= abs(z) if z != 0 else 1
                    z = sign(z)
                x *= base.getAspectRatio()
                self.pointer.setPos(x, 1, z)
        return task.cont

    def toggle(self):
        if self.active:
            self.pointer.hide()
            taskMgr.remove(self.task)
            self.active = False
        else:
            self.task = taskMgr.add(self.track, "onscreen follower")
            self.active = True

    def destroy(self):
        taskMgr.remove(self.task)
        self.pointer.removeNode()
        Follower.instance = None
			
