from army import UnitType, Army

class Territory:
    def __init__(self,name,resource_type,resource_amount,defense_strength):
        self.name = name
        self.resource_type = resource_type
        self.resource_amount = resource_amount
        self.defense_strength = defense_strength
        self.army = Army()
        self.army.add_units("Infantry", defense_strength)
        self.conquered = False

bretagne = Territory("Bretagne", "food", 5, 8)
