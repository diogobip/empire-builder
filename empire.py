#Imports
from army import UnitType, Army
from territory import Territory
from events import Event
import random
import json

#Dictionaries
drought = Event("Drought", "A dry season withers your crops.", "food", -10)
good_harvest = Event("Good Harvest", "An excellent season brings extra food.", "food", 15)
bandit_theft = Event("Bandit Theft", "Thieves steal from your storehouse.", "gold", -5)
trade_windfall = Event("Trade Windfall", "A passing merchant pays well.", "gold", 10)

archer_type = UnitType("Archer", attack=6, defense=2, upkeep=1)
infantry_type = UnitType("Infantry", attack=8, defense=5, upkeep=1)
cavalry_type = UnitType("Cavalry", attack=12, defense=4, upkeep=2)

my_army = Army()
bandit_camp = Army()
bandit_camp.add_units("Infantry",8)


#variables
population = 20
food = 50
wood = 20
stone = 10
gold = 5

buildings = {
    "house": False,
    "farm": False,
    "mineshaft": False,
    "barrack": False
}

unit_types = {
    "Archer": archer_type,
    "Infantry": infantry_type,
    "Cavalry": cavalry_type
}

rival_population = 10
rival_army = Army()
rival_army.add_units("Infantry", 3)

bretagne = Territory("Bretagne", "food", 5, 8)
rheims = Territory("Rheims", "gold", 5, 14)
paris = Territory("Paris", "wood", 5, 20)

events = [drought, good_harvest, bandit_theft, trade_windfall]

#functions
def show_help():
    print("""
Available actions:
  farm, mine, chop, quarry       - assign your people to gather resources
  build house / build farms / build mineshaft / build barrack
  recruit                        - recruit 5 Infantry (needs a Barrack)
  attack                         - raid the bandit camp
  conquer bretagne / conquer rheims / conquer paris
  save / load                    - save or load your progress
  help                           - show this menu again
""")
def check_famine(food, population):
    if food < 0:
        food = 0
        population -= 1
        print("Famine! You lost a person this turn.")
    return food, population


def apply_job(choice, food, wood, stone, gold,buildings,population):
    if choice == "farm":
        if buildings["farm"]:
            food += 20
        else:
            food += 10
    elif choice == "help":
        show_help()
        
    elif choice == "mine":
            if buildings["mineshaft"]:
                gold += 10
            else:
                gold += 5
    elif choice == "recruit":
        if buildings["barrack"]:
            if population >= 5 and food >= 10 and gold >= 5:
                population -= 5
                food -= 10
                gold -= 5
                my_army.add_units("Infantry", 5)
                print("5 people joined your army as Infantry.")
            else:
                print("Not enough population, food, or gold to recruit.")
        else:
                print("You need a Barracks before you can recruit soldiers.")
    elif choice == "chop":
        wood += 5
    elif choice == "quarry":
        stone += 5
    elif choice == "build house":
        if wood >= 15 and stone >= 10:
            wood -= 15
            stone -= 10
            population += 5
            buildings["house"] = True
            print("You built a house! Population +5.")
        else:
            print("Not enough resources to build a house.")
    elif choice == "build farms":
        if wood >= 20 and stone >= 10:
            wood -= 20
            stone -= 10
            buildings["farm"] = True
            print("You built a farm! Farming now gives +20 food instead of +10.")
        else:
            print("Not enough resources to build a farm.")
    elif choice == "build mineshaft":
        if wood >= 15 and stone >= 20:
            wood -= 15
            stone -= 20
            buildings["mineshaft"] = True
            print("You built a mine shaft! Mining now gives +10 gold instead of +5.")
        else:
            print("Not enough resources to build a mine shaft.")
    elif choice == "build barrack":
        if wood >= 30 and stone >= 25:
            wood -= 30
            stone -= 25
            buildings["barrack"] = True
            print("You built a barrack! Now you can recruit soldiers.")
        else:
            print("Not enough resources to build a barrack.")
    elif choice == "attack":
        my_attack = my_army.total_attack(unit_types)
        enemy_attack = bandit_camp.total_attack(unit_types)
        if my_attack > enemy_attack:
            gold += 20
            bandit_camp.apply_losses()
            print("You defeated the bandit camp! You looted 20 gold.")
        else:
            my_army.apply_losses()
            print("Your army was not strong enough to win.")
    elif choice == "conquer bretagne":
        if bretagne.conquered:
            print("You already conquered Bretagne.")
        else:
            my_attack = my_army.total_attack(unit_types)
            enemy_attack = bretagne.army.total_attack(unit_types)
            if my_attack > enemy_attack:
                bretagne.conquered = True
                bretagne.army.apply_losses()
                print("You conquered Bretagne!")
            else:
                my_army.apply_losses()
                print("Your army was not strong enough to conquer Bretagne.")
    elif choice == "conquer rheims":
        if rheims.conquered:
            print("You already conquered Rheims.")
        else:
            my_attack = my_army.total_attack(unit_types)
            enemy_attack = rheims.army.total_attack(unit_types)
            if my_attack > enemy_attack:
                rheims.conquered = True
                rheims.army.apply_losses()
                print("You conquered Rheims!")
            else:
                my_army.apply_losses()
                print("Your army was not strong enough to conquer Rheims.")
    elif choice == "conquer paris":
        if paris.conquered:
            print("You already conquered Paris.")
        else:
            my_attack = my_army.total_attack(unit_types)
            enemy_attack = paris.army.total_attack(unit_types)
            if my_attack > enemy_attack:
                paris.conquered = True
                paris.army.apply_losses()
                print("You conquered Paris!")
            else:
                my_army.apply_losses()
                print("Your army was not strong enough to conquer Paris.")
    elif choice == "save":
        save_game()
    elif choice == "load":
        population, food,wood, stone, gold,  buildings, rival_population = load_game()
        print("Game loaded!")

    else:
        print("Not a valid choice, your people did nothing this turn.")
    return food, wood, stone, gold,buildings,population


def show_status(population, food, wood, stone, gold, buildings):
    print(f"Population: {population} | Food: {food} | Wood: {wood} | Stone: {stone} | Gold: {gold}")
    print("Buildings:")
    for name, built in buildings.items():
        if built:
            status = "built"
        else:
            status = "not built"
        print(f"  {name}: {status}")
    print("Army:")
    for unit_type, count in my_army.units.items():
        print(f"  {unit_type}: {count}")
    print(f"Rival City -> Population: {rival_population} | Army: {rival_army.units}")

def save_game():
    save_data = {
        "population": population,
        "food": food,
        "wood": wood,
        "stone": stone,
        "gold": gold,
        "buildings": buildings,
        "my_army_units": my_army.units,
        "rival_population": rival_population,
        "rival_army_units": rival_army.units,
        "bretagne_conquered": bretagne.conquered,
        "rheims_conquered": rheims.conquered,
        "paris_conquered": paris.conquered
    }
    file = open("save.json", "w")
    json.dump(save_data, file)
    file.close()
    print("Game saved!")

def load_game():
    file = open("save.json", "r")
    save_data = json.load(file)
    file.close()

    population = save_data["population"]
    food = save_data["food"]
    wood = save_data["wood"]
    stone = save_data["stone"]
    gold = save_data["gold"]
    buildings = save_data["buildings"]
    my_army.units = save_data["my_army_units"]
    rival_population = save_data["rival_population"]
    rival_army.units = save_data["rival_army_units"]
    bretagne.conquered = save_data["bretagne_conquered"]
    rheims.conquered = save_data["rheims_conquered"]
    paris.conquered = save_data["paris_conquered"]

    return population, food, wood, stone, gold, buildings, rival_population

show_help()

#this is the main loop 
while True:
    choice = input("What should your people do? ")
    food -= 2

    food, population = check_famine(food, population)

    if population <= 0:
        print("Your tribe has perished. Game over.")
        print("Thank you for playing!")
        break
    if bretagne.conquered and rheims.conquered and paris.conquered:
        print("You have conquered all of France! Victory!")
        print("Thank you for playing!")
        break

    food, wood, stone, gold,buildings,population = apply_job(choice, food, wood, stone, gold,buildings,population)

    
    

    show_status(population, food, wood, stone, gold,buildings)

    if bretagne.conquered:
        if bretagne.resource_type == "food":
            food += bretagne.resource_amount
    if rheims.conquered:
        if rheims.resource_type == "gold":
            gold += rheims.resource_amount
    if paris.conquered:
        if paris.resource_type == "wood":
            wood += paris.resource_amount
    
    if random.randint(1, 4) == 1:
        chosen_event = random.choice(events)
        food, wood, stone, gold = chosen_event.trigger(food, wood, stone, gold)

    rival_population += 1
    if rival_population % 5 == 0:
         rival_army.add_units("Infantry", 1)
    input("Press Enter for next turn...")