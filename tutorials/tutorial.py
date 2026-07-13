class Character:
    def __init__(self,name,health):
        self.name = name
        self.health = health
    def take_damage(self,amount):
        self.health -= amount    
    def heal(self,amount):
        self.health += amount

hero = Character("Hero",50)
hero.take_damage(15)
hero.heal(10)
print(hero.health)

class Buildings:
    def __init__(self, name, cost_wood, cost_stone, effect_resource, effect_amount):
        self.name = name
        self.cost_wood = cost_wood
        self.cost_stone = cost_stone
        self.effect_resource = effect_resource
        self.effect_amount = effect_amount
        self.build = False
        self.level = 1
    def can_afford(self, wood, stone):
        if wood >= self.cost_wood and stone >= self.cost_stone:
            return True
        else:
             return False
    def build_now(self, wood, stone):
        if self.can_afford(wood, stone):
            self.build = True
            return True
        else:
            return False
    def upgrade(self):
        self.level += 1
        self.effect_amount += 5
    
farm = Buildings("Farm", 20, 10, "food", 20)
farm.build_now(25, 15)
print(farm.build, farm.effect_amount)
farm.upgrade()
print(farm.level, farm.effect_amount)