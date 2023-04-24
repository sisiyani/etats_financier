# -*- coding: utf-8 -*-

# MODULES
import argparse
import pandas as pd
import sqlite3
import os

from modules import route_sqlite, route_datacleaning
from modules.route_sqlite import query_sqlite
from utils import utils
from os import listdir


# COMMANDES
def __main__(args):
     if args.commande == "init_database":
          init_db()
     elif args.commande == "create_csv":
          create_clean_csv()
     elif args.commande == "load_to_db":
          create_table_and_insert_into()
     elif args.commande == "execute_sql":
          execute_sql()
     elif args.commande == "all":
          all_functions()
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


def create_clean_csv():
     # Récupération des paramètres nécessaires depuis le fichier settings.json
     param_input = utils.read_settings("settings/settings.json", dict = "path_data", elem = "input")
     param_to_csv = utils.read_settings("settings/settings.json", dict = "path_data", elem = "to_csv")
     
     # Création des fichiers csv à partir des fichiers sources 
     route_datacleaning.create_csv(param_input["path"], param_to_csv["path"])
     # Uniformisation des données des fichiers csv
     route_datacleaning.cleanData(param_to_csv["path"])
     
     return


def create_table_and_insert_into(): 
     # Récupération des paramètres nécessaires depuis le fichier settings.json
     param_database = utils.read_settings("settings/settings.json", dict = "sqlite_db", elem = "LOCAL SERVER")
     param_file = utils.read_settings("settings/settings.json", dict = "path_data", elem = "to_csv")
     
     db_path = sqlite3.connect(param_database['database'])

     # Liste les fichiers à insérer au sein de la bdd
     files = []
     files_path = param_file['path']
    
     for file in os.listdir(files_path):
          if file.split('/')[-1] != "demo.csv":
               print('file :', file)
               files.append(files_path + '/' + file)
     
     print(" ")
     print('files :', files)
     print(" ")

     # Boucle créant les tables et introduisant les données au sein de la bdd
     for file in files:
          route_sqlite.creer_table_csv(file, db_path)

     db_path.close()


def execute_sql():
     query_list = query_sqlite.get_query()
     #print("query list : ", query_list)

     db_file = "data/database/etats_financier.db"
     output_folder = "data/output"

     route_sqlite.execute_sql_queries(query_list, db_file, output_folder)
 

def all_functions():
     init_db()
     create_clean_csv()
     create_table_and_insert_into()
     execute_sql()
     return


# Initialisation du parsing
parser = argparse.ArgumentParser()
parser.add_argument("commande", type = str, help = "Commande à exécuter")
args = parser.parse_args()

# Core
if __name__ == "__main__":
     __main__(args)



