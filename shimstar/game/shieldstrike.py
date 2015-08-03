import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.task.Task import Task

from shimstar.core.shimconfig import *

class ShieldStrike:
    def __init__(self, pos):
        self.model = loader.loadModel(shimConfig.getInstance().getConvRessourceDirectory() + "models/shieldstrike/shields")
        self.model.setScale(5)
        self.model.reparentTo(render)
        self.model.setLightOff()
        self.model.setPos(pos)
        self.model.setTwoSided(1)
        self.model.find('**/+SequenceNode').node().loop(1)
        self.stepTask = taskMgr.add(self.step, "Shieldstrike")
        self.stepTask.last = 0

    def destroy(self):
        taskMgr.remove(self.stepTask)
        self.model.detachNode()

    def step(self, task):
        if task.time > .5: self.destroy()

        return task.cont
