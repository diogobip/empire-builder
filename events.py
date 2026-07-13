class Event:
    def __init__(self,name,description, resource_type,resource_amount):
        self.name = name
        self.description = description
        self.resource_type = resource_type
        self.resource_amount = resource_amount 
    
    def trigger(self, food, wood, stone, gold):
        if self.resource_type == "food":
            food += self.resource_amount
        elif self.resource_type == "wood":
            wood += self.resource_amount
        elif self.resource_type == "stone":
            stone += self.resource_amount
        elif self.resource_type == "gold":
            gold += self.resource_amount
        print(f"{self.name}: {self.description}")
        return food, wood, stone, gold