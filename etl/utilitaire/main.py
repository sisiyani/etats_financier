# -*- coding: utf-8 -*-


# MODULES
import argparse

from modules.route_sqlite import route_sqlite
from utils import utils

# COMMANDES
def __main__(args):
     if args.commande == "init_database":
          init_db()
     elif args.commande == "test":
          print("test")
     return


def init_db():
     print("###############")
     print("### INIT_DB ###")
     print("###############")
     print(" ")

     print("--- RECUPERATION DES PARAMETRES ---")
     param_config = utils.read_settings("settings/settings.json", dict = "sqlite_db", elem = "LOCAL SERVER")
     print(" --- PARAM_CONFIG : ", param_config, " ---")
     print(" ")

     print(" --- DEPLOIEMENT DE LA BDD ---")
     route_sqlite.deploy_database(database = param_config["database"])
     print(" ")
     return

# Initialisation du parsing
parser = argparse.ArgumentParser()
parser.add_argument("commande", type = str, help = "Commande à exécuter")
args = parser.parse_args()

# Core
if __name__ == "__main__":
     __main__(args)



