# -*- coding: utf-8 -*-


def parser_cvs(filename, fields_jsons):
    """esta funcion lista con un diccionario con la configuracion"""

    with open(filename, "r") as conf_file:
        readfilecsv = conf_file.readlines()

    diccionario_json = []

    # print readfilecsv

    # Recorro la lineas de csv
    for read_line in readfilecsv:

        # Omitir la linea por comentarios
        if read_line.startswith("#"):
            continue

        # Sila linea esta vacia
        if read_line.strip() == "":
            continue

        # separo los campos por comas
        split_read_lines = read_line.split(",")

        # print read_line

        # incialicio el diccionario para ingresarles key and value
        row_json = {}

        # Recorrer los atributos del json
        indice = 0

        # print len(fields_jsons),

        # for field_json in fields_jsons:
        for value_field in split_read_lines:

            if value_field.strip() == '""':
                value_field = ""

            #row_json[field_json] = split_read_line[indice].strip()
            row_json[fields_jsons[indice]] = value_field.strip()

            indice = indice + 1

        if row_json:
            diccionario_json.append(row_json)

    return diccionario_json
