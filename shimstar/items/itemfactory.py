from shimstar.items.engine import *
from shimstar.items.weapon import *
# ~ from shimstar.items.mining import *
from shimstar.items.item import *
from shimstar.core.constantes import *
from shimstar.items.mineral import *

class itemFactory():
    def __init__(self):
        pass

    @staticmethod
    def getItemFromTemplate(templateId):
        item = ShimstarItem(templateId)
        if item.getTypeItem() == C_ITEM_ENGINE:
            item = Engine(templateId)
        elif item.getTypeItem() == C_ITEM_WEAPON:
            item = Weapon(templateId)
        elif item.getTypeItem() == C_ITEM_MINERAL:
            item = Mineral(templateId)
        #~ elif item.getTypeItem()==C_ITEM_MINING:
        #~ item=Mining(templateId)
        return item

    @staticmethod
    def getItemFromTemplateType(templateId, typeItem):
        item = None
        if typeItem == C_ITEM_ENGINE:
            item = Engine(templateId)
        elif typeItem == C_ITEM_WEAPON:
            item = Weapon(templateId)
        elif typeItem == C_ITEM_MINERAL:
            item=Mineral(templateId)
        else:
            item = ShimstarItem(templateId)
        return item


@staticmethod


def getItemFromXml(xmlPart, typeItem):
    item = None
    if typeItem == C_ITEM_ENGINE:
        item = Engine(0, xmlPart)
    elif typeItem == C_ITEM_WEAPON:
        item = Weapon(0, xmlPart)
    #~ elif typeItem==C_ITEM_MINING:
    #~ item=Mining(0,xmlPart)
    elif typeItem == C_ITEM_MINERAL:
        item = Mineral(0, xmlPart)
    else:
        item = ShimstarItem(0, xmlPart)

    return item
		