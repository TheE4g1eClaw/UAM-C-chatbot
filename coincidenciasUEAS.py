import json

plan1 = input("Ingresa el nombre del primer plan de estudio: ")
plan2 = input("Ingresa el nombre del segundo plan de estudio: ")

plan1 = json.load(open(f"./data/planes_estudio/{plan1}.json", "r", encoding="utf-8"))
plan2 = json.load(open(f"./data/planes_estudio/{plan2}.json", "r", encoding="utf-8"))

for uea in plan1["ueas"]:
    if uea in plan2["ueas"]:
        print(uea)
        print(plan1["ueas"][uea]["clave"])
        if plan1["ueas"][uea]["clave"] == plan2["ueas"][uea]["clave"]:
            print("Coincide")
            if plan1["ueas"][uea]["serializacion"] == plan2["ueas"][uea]["serializacion"]:
                print("Serializacion: Coincide")
            else:
                print("Serializacion: No coincide")
        else:
            print(plan2["ueas"][uea]["clave"])
        print()