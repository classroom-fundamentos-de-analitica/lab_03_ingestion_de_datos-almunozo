"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""

import pandas as pd
import re


def formatHeader(header):
    return header.lower().replace(" ", "_")


def ingest_data():

    with open("clusters_report.txt", "r") as file:
        lines = file.readlines()

        # Creación de los encabezados
        lines[0] = re.sub(r"\s{2,}", "-", lines[0]).strip().split("-")
        lines[1] = re.sub(r"\s{2,}", "-", lines[1]).strip().split("-")
        lines[0].pop(), lines[1].pop(0)

        # Se añaden al futuro dataframe
        data = {
            lines[0][0]: [],
            lines[0][1] + " " + lines[1][0]: [],
            lines[0][2] + " " + lines[1][1]: [],
            lines[0][3]: [],
        }

        # Se da el formato deseado a los encabezados
        data = {formatHeader(x): l for x, l in data.items()}

        # A partir de que comienzan los datos
        for i in range(2, len(lines)):
            # Se detectan más de dos espacios en blanco, se eliminan y se eliminan
            # los elementos vacíos 
            lines[i] = re.sub(r"\s{2,}", ".", lines[i]).strip().split(".")
            lines[i] = list(filter(lambda x: x, lines[i]))

            # Si hay un número, significa que es el comienzo de una nueva fila
            if lines[i] and lines[i][0].isnumeric():
                data["cluster"].append(int(lines[i][0]))
                data["cantidad_de_palabras_clave"].append(int(lines[i][1]))
                data["porcentaje_de_palabras_clave"].append(float(lines[i][2][:-2].replace(",", ".")))
                data["principales_palabras_clave"].append(" ".join(lines[i][3:]))
            # De lo contrario, se continúa con las palabras clave de la fila anterior
            elif data["principales_palabras_clave"]:
                line = data["principales_palabras_clave"].pop() + " " + " ".join(lines[i])                
                data["principales_palabras_clave"].append(line.strip())

        df = pd.DataFrame(data)
        return df