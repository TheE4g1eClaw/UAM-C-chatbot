# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from json import load

class ActionSayCareer(Action):
    def name(self) -> Text:
        return "action_say_career"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        career = tracker.get_slot("career")
        if not career:
            dispatcher.utter_message("Lo siento, no tengo información sobre que carrera estudias")
        else:
            dispatcher.utter_message(f"Estudias la carrera de {career}")

        return []
    
class ActionSayUEAPerLevel(Action):
    niveles = {
        "formacion_inicial": "Tronco General Formación Inicial",
        "divisional": "Tronco Divisional",
        "formacion_basica": "Formación Básica",
        "formacion_profesional": "Formación Profesional",
    }
    
    def name(self) -> Text:
        return "action_say_uea_per_level"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        career = tracker.get_slot("career")
        level = tracker.get_slot("level")
        
        if not career:
            dispatcher.utter_message("Lo siento, no tengo información sobre que carrera estudias")
        elif not level:
            dispatcher.utter_message("Lo siento, no tengo información sobre en que nivel estás")
        else:
            plan = load(open("data/planes_estudio/" + career + ".json", encoding="utf-8"))
            mensaje = f"En el nivel de {self.niveles[level]} tienes las siguientes UEA's:\n"
            for uea in plan[level]:
                mensaje += f"- {uea}\n"
            dispatcher.utter_message(mensaje)
        return []
    
class ActionSayRequirements(Action):
    def name(self) -> Text:
        return "action_say_requirements"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        career = tracker.get_slot("career")
        if not career:
            dispatcher.utter_message("Lo siento, no tengo información sobre que carrera estudias")
        else:
            plan = load(open("data/planes_estudio/" + career + ".json", encoding="utf-8"))
            mensaje = f"Para poder cursar la carrera de {career} necesitas los siguientes requisitos:\n"
            for req in plan["requisitos"]:
                mensaje += f"- {req}\n"
            dispatcher.utter_message(mensaje)
        return []
    
class ActionSayUEAPerTrimester(Action):
    def name(self) -> Text:
        return "action_say_uea_per_trimester"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        career = tracker.get_slot("career")
        trimester = tracker.get_slot("trimester")
        
        if not career:
            dispatcher.utter_message("Lo siento, no tengo información sobre que carrera estudias")
        elif not trimester:
            dispatcher.utter_message("Lo siento, no tengo información sobre en que trimestre estás")
        else:
            plan = load(open("data/planes_estudio/" + career + ".json", encoding="utf-8"))
            mensaje = f"En el trimestre {trimester} tienes las siguientes UEA's:\n"
            for uea in plan["ueas"]:
                trimester = int(trimester)
                if plan["ueas"][uea]["trimestre"] == trimester:
                    mensaje += f"- {uea}\n"
            dispatcher.utter_message(mensaje)
        return []
    
class ActionUEAParaMovilidad(Action):
    def name(self) -> Text:
        return "action_uea_para_movilidad"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        career = tracker.get_slot("career")
        trimester = tracker.get_slot("trimester")
        
        if not career:
            dispatcher.utter_message("Lo siento, no tengo información sobre que carrera estudias")
        elif not career in ["administracion", "dercho", "diseño", "comunicacion", "computacion"]:
            dispatcher.utter_message("No hay materias necesarias para iniciar la movilidad")
        else:
            plan = load(open("data/planes_estudio/" + career + ".json", encoding="utf-8"))
            mensaje = "Para poder iniciar la movilidad necesitas cursar las siguientes UEA's:\n"
            niveles = ["formacion_inicial", "divisional", "formacion_basica"]
            for nivel in niveles:
                for uea in plan[nivel]:
                    mensaje += f"- {uea}\n"
            dispatcher.utter_message(mensaje)
            
class ActionSaySerializacion(Action):
    def name(self) -> Text:
        return "action_say_serializacion"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        career = tracker.get_slot("career")
        uea = tracker.get_slot("uea")
        
        if not career:
            dispatcher.utter_message("Lo siento, no tengo información sobre que carrera estudias")
        elif not uea:
            dispatcher.utter_message("Lo siento, no tengo información sobre que UEA deseas serializar")
        else:
            plan = load(open("data/planes_estudio/" + career + ".json", encoding="utf-8"))
            existe = False
            for ueaAux in plan["ueas"]:
                if plan["ueas"][ueaAux]["nombre_normalizado"] == uea:
                    uea = ueaAux
                    existe = True
            if (uea not in plan["ueas"] or not existe):
                dispatcher.utter_message("Lo siento, no tengo información sobre la UEA " + uea + ". Por favor verifica que el nombre sea correcto")
            else:    
                serializacion = getBackSerializacion(uea, plan, set())
                if len(serializacion) == 0:
                    mensaje = "No hay ninguna UEA que necesites cursar para poder cursar la UEA " + uea + ".\n"
                else:
                    mensaje = "Para cursar la UEA " + uea + " necesitas haber aprobado las siguientes UEA's:\n"
                    for ueaAux in serializacion:
                        mensaje += f"- {ueaAux}\n"
                serializacion = getFrontSerializacion(uea, plan, set())
                if len(serializacion) > 0:
                    mensaje += "Y necesitas haber aprobado esta UEA para cursar:\n"
                    for ueaAux in serializacion:
                        mensaje += f"- {ueaAux}\n"
                else:
                    mensaje += "Esta UEA no es requisito para ninguna otra UEA"
                dispatcher.utter_message(mensaje)
                


# Funciones generales
def getUEAPorClave(clave: str, plan: dict):
    for uea in plan["ueas"]:
        if plan["ueas"][uea]["clave"] == clave:
            return uea

def getBackSerializacion(uea: str, plan: dict, serializacion: set):
    if len(plan["ueas"][uea]["serializacion"]) == 0:
        return serializacion
    else:
        for clave in plan["ueas"][uea]["serializacion"]:
            nombreUEA = getUEAPorClave(clave, plan)
            if nombreUEA not in serializacion:
                serializacion.add(nombreUEA)
                subSerializacion = getBackSerializacion(nombreUEA, plan, serializacion)
                for ueaAux in subSerializacion:
                    serializacion.add(ueaAux)
        return serializacion
            
            
def getFrontSerializacion(uea: str, plan: dict, serializacion: set):
    clave = plan["ueas"][uea]["clave"]
    futurasUEAs = set()
    for ueaAux in plan["ueas"]:
        if clave in plan["ueas"][ueaAux]["serializacion"] and ueaAux not in serializacion:
            futurasUEAs.add(ueaAux)

    if len(futurasUEAs) == 0:
        return serializacion
    else:
        for ueaAux in futurasUEAs:
            serializacion.add(ueaAux)
            subSerializacion = getFrontSerializacion(ueaAux, plan, serializacion)
            for uea in subSerializacion:
                serializacion.add(uea)
        return serializacion