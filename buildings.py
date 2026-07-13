class Buildings:
    def __init__(self,name,tier,cost,effect):
        self.name = name
        self.tier = tier
        self.cost = cost
        self.effect = effect
        self.is_build = False
    
    def upgrade(self):
        self.tier += 1