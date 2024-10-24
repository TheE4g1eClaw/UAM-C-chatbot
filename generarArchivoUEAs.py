import os
import json

def normalizar_nombre(nombre: str):
    normalizado = nombre.lower()
    normalizado = normalizado.replace("á", "a")
    normalizado = normalizado.replace("é", "e")
    normalizado = normalizado.replace("í", "i")
    normalizado = normalizado.replace("ó", "o")
    normalizado = normalizado.replace("ú", "u")
    return normalizado

if __name__ == "__main__":
    # Se obtiene la los planes de estudio
    ruta = "./data/"
    archivos = os.listdir(ruta + "planes_estudio/")
    
    ueas = set()
    
    for archivo in archivos:
        plan = json.load(open(ruta + f"planes_estudio/{archivo}", "r", encoding="utf-8"))
        ueas = ueas.union(plan["ueas"].keys())
        
    with open(ruta + "ueas.yml", "w", encoding="utf-8") as file:
        file.write("""version: "3.1"

nlu:
- lookup: uea
  examples: |\n""") 
        for uea in ueas:
            file.write(f"    - {uea}\n")
            file.write(f"    - {normalizar_nombre(uea)}\n")
