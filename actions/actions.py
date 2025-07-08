# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from json import load

import os

ruta = "./data/planes_estudio/"
JSON_EXT = ".json"
carreras = [os.path.splitext(x)[0] for x in os.listdir(ruta)]

class ActionSayCareer(Action):
    def name(self) -> Text:
        return "action_say_career"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        career = tracker.get_slot("career")
        if not career:
        elif career in carreras:
            plan = load(open(ruta + career + JSON_EXT, encoding="utf-8"))
            dispatcher.utter_message(f"Estudias la carrera de {plan['name']}.")
            dispatcher.utter_message(f"Estudias la carrera de {plan['name']}.")
        else:
            dispatcher.utter_message(f"Indicaste que estudias la carrera de {career}, pero no tengo información sobre ella.")
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
            plan = load(open(ruta + career + JSON_EXT, encoding="utf-8"))
            mensaje = f"En el nivel de {self.niveles[level]} tienes las siguientes UEA's:\n"
            for uea in plan[level]:
                mensaje += f"- {uea}\n"
            dispatcher.utter_message(mensaje)
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
            plan = load(open("data/planes_estudio/" + career + JSON_EXT, encoding="utf-8"))
            mensaje = f"Para poder cursar la carrera de {career} necesitas los siguientes requisitos:\n"
            for req in plan["requisitos"]:
                mensaje += f"- {req}\n"
            dispatcher.utter_message(mensaje)
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
            plan = load(open("data/planes_estudio/" + career + JSON_EXT, encoding="utf-8"))
            mensaje = f"En el trimestre {trimester} tienes las siguientes UEA's:\n"
            trimester = int(trimester)
            for uea in plan["ueas"]:
                if plan["ueas"][uea]["trimestre"] == trimester:
                    mensaje += f"- {uea}\n"
                    if 'Movilidad' in uea:
                        mensaje += f"Si no se cursa esta UEA se pueden adelantar otras UEAs\n"
                if plan["ueas"][uea]["trimestre"] == 0:
                    if trimester in plan["ueas"][uea]["trimestres"] and plan["ueas"][uea]["obligatoria"] == True:
                        mensaje += f"- {uea}\n"
            dispatcher.utter_message(mensaje)
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
            plan = load(open("data/planes_estudio/" + career + JSON_EXT, encoding="utf-8"))
            mensaje = "Para poder iniciar la movilidad necesitas cursar las siguientes UEA's:\n"
            niveles = ["formacion_inicial", "divisional", "formacion_basica"]
            for nivel in niveles:
                for uea in plan[nivel]:
                    mensaje += f"- {uea}\n"
            dispatcher.utter_message(mensaje)
            dispatcher.utter_message(mensaje)
            
class ActionSayOptativas(Action):
    def name(self) -> Text:
        return "action_say_optativas"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        career = tracker.get_slot("career")
        
        if not career:
            dispatcher.utter_message("Lo siento, no tengo información sobre que carrera estudias")
            plan = load(open(ruta + career + JSON_EXT, encoding="utf-8"))
            mensaje = f"Las UEA's optativas de orientación que ofrece la carrera de {career} que puedes cursar son:\n"
            for uea in plan["optativas"]:
                mensaje += f"- {uea}\n"
            dispatcher.utter_message(mensaje)
            dispatcher.utter_message(mensaje)
            
        return []
    
    
            
class ActionSaySerializacion(Action):
    def name(self) -> Text:
        return "action_say_serializacion"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        career = tracker.get_slot("career")
        uea = tracker.get_slot("uea")
        clave = tracker.get_slot("clave")
        
        if not career:
            dispatcher.utter_message("Lo siento, no tengo información sobre que carrera estudias")
        elif not uea and not clave:
            dispatcher.utter_message("Lo siento, no tengo información sobre que UEA deseas serializar")
            plan = load(open("data/planes_estudio/" + career + JSON_EXT, encoding="utf-8"))
            existe = False
            
            if clave:
                uea = getUEAPorClave(clave, plan)
                if uea:
                    existe = True
            elif uea not in plan["ueas"]:
                normalizado = normalizar_nombre(uea)
                for ueaAux in plan["ueas"]:
                    if normalizado in normalizar_nombre(ueaAux):
                        uea = ueaAux
                        existe = True
                        break
                        break
                    
            eventos = [SlotSet("uea", None), SlotSet("clave", None)]
            if not uea:
                dispatcher.utter_message("Lo siento, no tengo UEAs con la clave" + clave)
            elif (uea not in plan["ueas"]):
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
            return eventos

class ActionSayInfoUEA(Action):
    def name(self) -> Text:
        return "action_say_info_uea"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        career = tracker.get_slot("career")
        uea = tracker.get_slot("uea")
        clave = tracker.get_slot("clave")
        
        if not career:
            dispatcher.utter_message("Lo siento, no tengo información sobre que carrera estudias")
        elif not uea and not clave:
            dispatcher.utter_message("Lo siento, no tengo información sobre que UEA deseas consultar")
        else:
            plan = load(open("data/planes_estudio/" + career + ".json", encoding="utf-8"))
            existe = False
            
            if clave:
                uea = getUEAPorClave(clave, plan)
                if uea:
                    existe = True
            elif uea not in plan["ueas"]:
                normalizado = normalizar_nombre(uea)
                for ueaAux in plan["ueas"]:
                    if normalizado in normalizar_nombre(ueaAux):
                        uea = ueaAux
                        existe = True
                        break
            eventos = [SlotSet(key="uea", value=None), SlotSet(key="clave", value=None)]
            if not uea:
                dispatcher.utter_message("Lo siento, no tengo UEAs con la clave" + clave)
            elif (uea not in plan["ueas"]):
                dispatcher.utter_message("Lo siento, no tengo información sobre la UEA " + uea + ". Por favor verifica que el nombre sea correcto")
            else:
                ueaInfo = plan["ueas"][uea]
                mensaje = f"La UEA {uea} tiene la siguiente información:\n"
                if ueaInfo["obligatoria"]:
                    mensaje += "- Es una UEA obligatoria\n"
                else:
                    mensaje += "- Es una UEA optativa\n"
                if ueaInfo["clave"] != "":
                    mensaje += f"- Clave: {ueaInfo['clave']}\n"
                if ueaInfo["trimestre"] == 0:
                    mensaje += "- La UEA se puede cursar en los trimestres: "
                    for trimestre in ueaInfo["trimestres"]:
                        mensaje += f"{trimestre}, "
                    mensaje = mensaje[:-2] + "\n"
                else:
                    mensaje += f"- Se recomienda cursarse en el trimestre: {ueaInfo['trimestre']}\n"
                mensaje += f"- Créditos: {ueaInfo['creditos']}\n"
                dispatcher.utter_message(mensaje)
                
            return eventos
        
class ActionSayPagina(Action):
    def name(self) -> Text:
        return "action_say_pagina"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        career = tracker.get_slot("career")
        print(career)
        if not career:
            dispatcher.utter_message("Lo siento, no tengo información sobre que carrera estudias")
        elif not career in carreras:
            dispatcher.utter_message("Lo siento, no tengo información sobre la carrera " + career)
            plan = load(open("data/planes_estudio/" + career + JSON_EXT, encoding="utf-8"))
            dispatcher.utter_message(f"La página de la carrera de {plan['name']} es {plan['pagina']}")
        return []
        return []
                
class ActionSetSlot(Action):
    def name(self) -> Text:
        return "action_set_slot"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        #print(intent)
        if intent != "serializacion_uea" and intent != "info_uea":
            return []
        entidades = tracker.latest_message['entities']
        
        slots = {"uea" : {"entity": "uea", "start": 0, "end": 0, "value": None, "extractor": None},
        "career" : {"entity": None, "start": 0, "end": 0, "value": None, "extractor": None}}
        #print(entidades)
        for entidad in entidades:
            if entidad["entity"] == "uea":
                if (entidad["start"] >= slots["career"]["start"] and entidad["start"] <= slots["career"]["end"]) and slots["career"]["value"]:
                    slots["uea"] = entidad
                    slots["career"] = {"entity": None, "start": 0, "end": 0, "value": None, "extractor": None}
                elif entidad["extractor"] == "RegexEntityExtractor" and slots["uea"]["extractor"] != "RegexEntityExtractor":
                    slots["uea"] = entidad
                elif entidad["extractor"] == "RegexEntityExtractor" and entidad["end"] > slots["uea"]["end"]:
                    slots["uea"] = entidad
                elif slots["uea"]["extractor"] != "RegexEntityExtractor":
                    slots["uea"] = entidad
            elif entidad["entity"] == "career":
                if entidad["start"] < slots["uea"]["start"] or entidad["start"] > slots["uea"]["end"] :
                    slots["career"] = entidad
        eventos = []            
        if slots["uea"]["value"]:
            #print("uea:" + slots["uea"]["value"])
            eventos.append(SlotSet(key = "uea", value = slots["uea"]["value"]))
        if slots["career"]["value"]:
            #print("career:" + slots["career"]["value"])
            eventos.append(SlotSet(key = "career", value = slots["career"]["value"]))
            
        return eventos
            
                
            


# Funciones generales
def getUEAPorClave(clave: str, plan: dict):
    for uea in plan["ueas"]:
        if plan["ueas"][uea]["clave"] == clave:
            return uea
    return None

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
    
def normalizar_nombre(nombre: str):
    normalizado = nombre.lower()
    normalizado = normalizado.replace("á", "a")
    normalizado = normalizado.replace("é", "e")
    normalizado = normalizado.replace("í", "i")
    normalizado = normalizado.replace("ó", "o")
    normalizado = normalizado.replace("ú", "u")
    return normalizado