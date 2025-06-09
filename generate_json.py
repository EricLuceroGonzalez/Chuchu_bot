import os
import json
import math
from datetime import datetime


json_file = os.path.join(os.path.dirname(__file__), "frases_chuchu.json")
output_file = os.path.join(os.path.dirname(__file__), "todas_las_citas.json")


def crear_lista_todas_citas():
    todas_las_citas = []
    with open(json_file, "r") as openfile:
        json_object = json.load(openfile)
    for libro in json_object:
        for cita in libro["quotes"]:
            cita_completa = {
                "texto": cita,
                "libro": libro["book"],
                "autor": libro["author"],
                "año": libro["year"],
                "portada": libro["portada"],
                "publicado": False,
                "enviado": 0,
            }
            todas_las_citas.append(cita_completa)
    return todas_las_citas


def cargar_existentes():
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def guardar_todos_los_json():
    nuevas_citas = crear_lista_todas_citas()
    existentes = cargar_existentes()

    # Usar un set para los textos ya existentes (puedes usar otro campo si lo prefieres)
    textos_existentes = set(cita["texto"] for cita in existentes)

    # Solo agregar las nuevas citas que no estén ya en el archivo
    for cita in nuevas_citas:
        if cita["texto"] not in textos_existentes:
            existentes.append(cita)
            textos_existentes.add(cita["texto"])

    # Asignar IDs únicos
    for idx, cita in enumerate(existentes, 1):
        cita["id"] = idx

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(existentes, f, ensure_ascii=False, indent=2)
    print("Archivo 'todas_las_citas.json' actualizado exitosamente.")


# guardar_todos_los_json()


def contar_caracteres():
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    not_valid_quotes = []
    for quote in data:
        max_lenght = len(quote["libro"]) + 15
        if (len(quote["texto"]) + max_lenght) > 250:
            print(f"\n{len(quote["texto"])} + {max_lenght}")
            print(quote["texto"])
        if (len(quote["texto"]) + max_lenght) > 280:
            print(f'Book: {quote["libro"]}')
            print(f"Quote ({len(quote['texto'])} chars+max:{max_lenght}): {quote}\n")
            not_valid_quotes.append(quote)
    print(len(not_valid_quotes))


contar_caracteres()
