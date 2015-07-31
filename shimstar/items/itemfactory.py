from shimstar.items.engine import *
from shimstar.items.weapon import *
# ~ from shimstar.items.mining import *
from shimstar.items.item import *
from shimstar.core.constantes import *
from shimstar.items.mineral import *
from shimstar.items.reactor import *
from shimstar.items.shield import *

class itemFactory():
    def __init__(self):
        pass

    @staticmethod
    def loadXml():
        dom = xml.dom.minidom.parse(shimConfig.getInstance().getRessourceDirectory() + "config\\itemtemplates.xml")
        it = dom.getElementsByTagName('item')
        for i in it:
            typeItem = int(i.getElementsByTagName('typeitem')[0].firstChild.data)
            templateId = int(i.getElementsByTagName('templateid')[0].firstChild.data)
            if ItemTemplate.listOfTemplate.has_key(str(typeItem) + "-" + str(templateId))!=True:
                if typeItem == C_ITEM_ENERGY:
                    ReactorTemplate(i)
                elif typeItem == C_ITEM_WEAPON:
                    WeaponTemplate(i)
                elif typeItem == C_ITEM_ENGINE:
                    EngineTemplate(i)
                elif typeItem == C_ITEM_SHIELD:
                    ShieldTemplate(i)
                # elif typeItem == C_ITEM_MINERAL:
                #     Min(i)
                else:
                    ItemTemplate(i)

    @staticmethod
    def getItemFromTemplate(templateId):
        item = ShimstarItem(templateId)
        if item.getTypeItem() == C_ITEM_ENGINE:
            item = Engine(templateId)
        elif item.getTypeItem() == C_ITEM_WEAPON:
            item = Weapon(templateId)
        elif item.getTypeItem() == C_ITEM_MINERAL:
            item = Mineral(templateId)
        elif item.getTypeItem() == C_ITEM_ENERGY:
            item = Reactor(templateId)
        elif item.getTypeItem() == C_ITEM_SHIELD:
            item = Shield(templateId)
        #~ elif item.getTypeItem()==C_ITEM_MINING:
        #~ item=Mining(templateId)
        return item

    @staticmethod
    def getItemFromTemplateType(templateId, typeItem):

        if typeItem == C_ITEM_ENGINE:
            item = Engine(templateId)
        elif typeItem == C_ITEM_WEAPON:
            item = Weapon(templateId)
        elif typeItem == C_ITEM_MINERAL:
            item = Mineral(templateId)
        elif typeItem == C_ITEM_ENERGY:
            item = Reactor(templateId)
        elif typeItem == C_ITEM_SHIELD:
            item = Shield(templateId)
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
        elif typeItem == C_ITEM_ENERGY:
            item = Reactor(0, xmlPart)
        elif typeItem == C_ITEM_SHIELD:
            item = Shield(0,xmlPart)
        else:
            item = ShimstarItem(0, xmlPart)

        return item