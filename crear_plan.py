
import json
from os.path import isfile

niveles = ["formacion_inicial", "divisional", "formacion_basica", "formacion_profesional", "optativas"]

def normalizar_nombre(nombre: str):
    normalizado = nombre.lower()
    normalizado = normalizado.replace("á", "a")
    normalizado = normalizado.replace("é", "e")
    normalizado = normalizado.replace("í", "i")
    normalizado = normalizado.replace("ó", "o")
    normalizado = normalizado.replace("ú", "u")
    return normalizado

def inicializar_plan():
    plan = {
        "name": "",
        "formacion_inicial": [],
        "divisional": [],
        "formacion_basica": [],
        "formacion_profesional": [],
        "optativas": [],
        "requisitos": [],
        "ueas": {}
    }
    return plan
def agregar_materia(plan):
    nombre = input("Ingrese el nombre de la materia: ")
    nivel = int(input("""Ingrese el nivel de la materia:
1)Formación inicial
2)Divisional
3)Formación básica
4)Formación profesional
5)Optativas\n""")) - 1
    clave = input("Ingrese la clave de la materia: ")
    creditos = int(input("Ingrese la cantidad de créditos: "))
    trimestre = int(input("Ingrese el trimestre en el que se cursa: "))
    if trimestre == 0:
        trimestres = [int(x) for x in input("Ingrese los trimestres en los que se cursa separados por espacios: ").split(" ")]
    obligatoria = input("¿Es obligatoria? 0)No 1)Sí: ")
    if obligatoria == "1":
        obligatoria = True
    else:
        obligatoria = False
    serializacion = []
    print("Ingrese las claves de las materias que son requisitos de la materia\nPara terminar de enter sin escribir nada")
    while True:
        materia = input()
        if materia == "":
            break
        serializacion.append(materia)
        
    normalizado = normalizar_nombre(nombre)    
    plan[niveles[nivel]].append(nombre)
        
    uea = {
        "clave": clave,
        "creditos": creditos,
        "trimestre": trimestre,
        "obligatoria": obligatoria,
        "serializacion": serializacion,
        "nombre_normalizado": normalizado
    }
    if trimestre == 0:
        uea["trimestres"] = trimestres
    plan["ueas"][nombre] = uea
    return plan

def eliminar_materia(plan):
    nombre = input("Ingrese el nombre de la materia a eliminar: ")
    for nivel in niveles:
        if nombre in plan[nivel]:
            plan[nivel].remove(nombre)
            break
    del plan["ueas"][nombre]
    return plan

def agregar_requisito(plan):
    requisitos = []
    print("Ingrese los requisitos para graduarse de la carrera.\nPara terminar de enter sin escribir nada")
    while True:
        requisito = input()
        if requisito == "":
            break
        requisitos.append(requisito)
    plan["requisitos"] = requisitos
    return plan

def comprobar_serelizaciones(plan: dict):
    claves = set()
    for uea in plan["ueas"]:
        for serializacion in plan["ueas"][uea]['clave']:
            claves.add(serializacion)
            
    for uea in plan["ueas"]:
        for serializacion in plan["ueas"][uea]['clave']:
            if serializacion not in claves:
                return False
    return True

def buscarUEA(plan):
    opcion = int(input("Por nombre(0) o por clave(1)? : "))
    if opcion == 0:
        nombre = input("Ingrese el nombre de la UEA: ")
        if plan["ueas"].get(nombre):
            print("La UEA"+ nombre + "esta registrada con la clave: " + plan["ueas"][nombre]["clave"])
        else: 
            print("La UEA no esta registrada")
    elif opcion == 1:
        clave = input("Ingrese la clave de la UEA: ")
        for uea in plan["ueas"]:
            if plan["ueas"][uea]["clave"] == clave:
                print("La UEA" + uea + "esta registrada con el nombre: " + uea)
                break
        else:
            print("La UEA no esta registrada")
            
def listaUEAS(plan):
    opcion = int(input("¿Normal(0) o Normalizado(1)? : "))
    if opcion == 0:
        for uea in plan["ueas"]:
            print(uea)
    elif opcion == 1:
        for uea in plan["ueas"]:
            print(plan["ueas"][uea]["nombre_normalizado"])
            

def guardar_plan(plan, nombre):
    with open("data/planes_estudio/" + nombre + ".json", "w", encoding="utf-8") as file:
        json.dump(plan, file, ensure_ascii=False, indent=4)
    print("Plan de estudios guardado exitosamente")




if __name__ == "__main__":
    while True:
        print("---- Menú ----")
        print("1. Crear/editar plan de estudios")
        print("2. Salir")
        opcion = int(input("Seleccione una opción: "))
        
        if opcion == 1:
            nombre_plan = input("Ingrese el nombre del archivo del plan de estudios: ")
            plan = dict()
            if isfile("data/planes_estudio/" + nombre_plan + ".json"):
                print("El plan de estudios ya existe, ¿desea editarlo?")
                opcion = input("S/N: ")
                if opcion.lower() == "s":
                    with open("data/planes_estudio/" + nombre_plan + ".json", "r", encoding="utf-8") as file:
                        plan = json.load(file)
            if not plan.get("name"):
                nombre = input("Ingrese el nombre del plan de estudios: ")
                plan = inicializar_plan()
                plan["name"] = nombre
                
            while True:
                print("---- Menú ----")
                print("1. Agregar materia")
                print("2. Eliminar materia")
                print("3. Agregar requisito")
                print("4. Comprobar serializaciones")
                print("5. Buscar EUA")
                print("6. Lista UEAS")
                print("7. Guardar plan de estudios")
                print("8. Salir")
                opcion = int(input())
                if opcion   == 1:
                    plan = agregar_materia(plan)
                elif opcion == 2:
                    plan = eliminar_materia(plan)
                elif opcion == 3:
                    plan = agregar_requisito(plan)
                elif opcion == 4:
                    if comprobar_serelizaciones(plan):
                        print("Las serializaciones son correctas")
                    else:
                        print("Las serializaciones no son correctas")
                elif opcion == 5:
                    buscarUEA(plan)
                elif opcion == 6:
                    listaUEAS(plan)
                elif opcion == 7:
                    guardar_plan(plan, nombre_plan)
                elif opcion == 8:
                    break
                else:
                    print("Opción no válida")
        else:
            print("Saliendo...")
            break
        