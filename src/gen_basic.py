# -*- coding: utf-8 -*-
from lib_csv import parser_cvs


def generator(config, args, head_config):
    """Esta funcion general el archivo para la configuracion router"""
    # seccion_config =

    fields_template = config.get(head_config, "fields_template").split(",")
    fields_template = map(lambda s: s.strip(), fields_template)

    path_template = config.get(head_config, "template")
    with open(path_template, "r") as template:
        read_template = template.read()

    seccion_config = read_template.split("\n")
    head = seccion_config.pop(0)
    footer = seccion_config.pop()

    ouput_file_config = head

    read_template = read_template.replace(head, "")
    read_template = read_template.replace(footer, "")

    parser_cvs_data = parser_cvs(config.get(head_config, "csv"), fields_template)

    # Secuenciador id de entrada
    secuenciador = int(args.router_static_id)

    for router in parser_cvs_data:

        clean_read_template = read_template

        for field in fields_template:
            # Recorro las var
            clean_read_template = clean_read_template.replace(field, router[field])

        clean_read_template = clean_read_template.replace("$id", str(secuenciador))

        secuenciador = secuenciador + 1

        ouput_file_config = ouput_file_config + clean_read_template

    ouput_file_config = ouput_file_config + footer + "\n"
    return ouput_file_config
