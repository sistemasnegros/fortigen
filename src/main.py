# -*- coding: utf-8 -*-
import logging
import argparse
import sys

from lib_sysblack.lib_mail import send_mail
from lib_sysblack.lib_config import load_config

# Ruta de archivos estaticos
from unipath import Path

# Modulos de aplicacion
from module_router import gen_static_router
from gen_basic import generator

NAMEAPP = "fortigen"
NAMEFILELOG = "%s.log" % (NAMEAPP)
NAMEFILECONFIG = "%s.cfg" % (NAMEAPP)


PROJECT_DIR = Path(__file__).ancestor(1)
ATTACHMENT_DIR = PROJECT_DIR.child('attachment')
ID_DEFAULT = 1


def loading_args():
    """Argumento de ejecucion"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Mostrar información en consola.", action="store_true")
    parser.add_argument("-c", "--config", help="Nombre de archivo de configuracion.", default=NAMEFILECONFIG)
    parser.add_argument("-d", "--debug", help="Mostrar información de depuración.", action="store_true")
    parser.add_argument("-t", "--test", help="Tirar una prueba del comando.", action="store_true")

    parser.add_argument("--router-static", help="routic static habilitar router gen.", action="store_true")
    parser.add_argument("--router-static-csv", help="routic static ruta csv.")
    parser.add_argument("--router-static-id", help="routic static id.", default=ID_DEFAULT)
    parser.add_argument("-o", "--output", help="Salida de archivo de configuracion.")

    args = parser.parse_args()

    return args


def log_configuration(args):
    """Configurando los log"""

    level_log = logging.INFO

    if args.debug:
        level_log = logging.DEBUG

    logformat = "%(asctime)s %(levelname)s: %(message)s"

    logging.basicConfig(filename=NAMEFILELOG, filemode='w', format=logformat, level=level_log)

    if args.verbose:
        fh = logging.StreamHandler()
        logFormatter = logging.Formatter(logformat)
        fh.setFormatter(logFormatter)
        logging.getLogger().addHandler(fh)


def fun_write_file(name, data, new=False):

    if new:
        mode = "w"
    else:
        mode = "a"

    with open(name, mode) as archivo:
        archivo.write(data)


def main():
    """Funcion Principal"""

    # Cargando variables pasadas como argumentos
    args = loading_args()

    # Set la configuracion de los logs
    log_configuration(args)

    # Cargando File configuracion
    config = load_config(args.config)

    logging.debug("Inicio de modo de depuracion.")

    # Nombre de archivo de salida
    output = config.get("GENERAL", "output").strip()

    fun_write_file(output, "", True)

    if config.get("FIREWALL-ADDRESS", "enable") == "yes":
        generada = generator(config, args, "FIREWALL-ADDRESS")
        fun_write_file(output, generada)

    if config.get("FIREWALL-ADDRESS-CIDR", "enable") == "yes":
        generada = generator(config, args, "FIREWALL-ADDRESS-CIDR")
        fun_write_file(output, generada)

    if config.get("FIREWALL-VIP", "enable") == "yes":
        generada = generator(config, args, "FIREWALL-VIP")
        fun_write_file(output, generada)

    if config.get("ROUTER-STATIC", "enable") == "yes":
        generada = generator(config, args, "ROUTER-STATIC")
        fun_write_file(output, generada)

if __name__ == '__main__':
    main()
