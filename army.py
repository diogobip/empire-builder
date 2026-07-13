class UnitType:
    def __init__(self,name,attack, defense, upkeep):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.upkeep = upkeep

class Army:
    def __init__(self):
        self.units = {"Archer": 0, "Infantry": 0, "Cavalry": 0}

    def add_units(self, unit_type_name, amount):
        self.units[unit_type_name] += amount
    
    def total_attack(self,unit_types):
        total = 0
        for unit_name, count in self.units.items():
            total += count * unit_types[unit_name].attack

        return total
    
    def apply_losses(self):
        for unit_name in self.units:
            self.units[unit_name] = self.units[unit_name] // 2