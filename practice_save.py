import json

buildings = {"house": True, "farm": False}

file = open("save.json", "w")
json.dump(buildings, file)
file.close()

import json
file = open("save.json", "r")
loaded_buildings = json.load(file)
file.close()
print(loaded_buildings)