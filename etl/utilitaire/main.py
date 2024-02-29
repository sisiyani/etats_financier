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
          if args.annee is None:
               print("MERCI DE RENSEIGNER L'ANNEE SOUHAITEE")
          create_clean_csv(args.annee)
     elif args.commande == "load_to_db":
          insert_into()
     elif args.commande == "execute_sql":
          #if args.annee is None:
          #     print("MERCI DE RENSEIGNER L'ANNEE SOUHAITEE")
          #else:
          execute_sql()
          #execute_sql_2()
     elif args.commande == "clean_output":
          clean_output()
     elif args.commande == "delete_files":
          delete_files()
     elif args.commande == "delete_tables":
          delete_db()
     elif args.commande == "delete_all":
          delete_all()
     elif args.commande == "all":
          if args.annee is None:
               print("MERCI DE RENSEIGNER L'ANNEE SOUHAITEE")
          else:
               all_functions(args.annee)
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


def create_clean_csv(annee):
     # Récupération des paramètres nécessaires depuis le fichier settings.json
     param_input = utils.read_settings("settings/settings.json", dict = "path_data", elem = "input")
     param_to_csv = utils.read_settings("settings/settings.json", dict = "path_data", elem = "to_csv")
     
     # Création des fichiers csv à partir des fichiers sources 
     route_datacleaning.create_csv(param_input["path"], param_to_csv["path"],annee)
     # Uniformisation des données des fichiers csv
     route_datacleaning.cleanData(param_to_csv["path"])
     
     return


def insert_into(): 
     # Récupération des paramètres nécessaires depuis le fichier settings.json
     param_db = utils.read_settings("settings/settings.json", dict = "db", elem = "etats_financier.db")
     param_files = utils.read_settings("settings/settings.json", dict = "path_data", elem = "to_csv")
     
     route_sqlite.insert_into_db(param_db['path'], param_files['path'])



def execute_sql_1():
     # Récupération des requêtes SQL à utiliser afin de produire les fichiers
     query=query_sqlite.create_table_query()
     # Récupération des paramètres nécessaires à l'execution de execute_sql_queries(query_list, db_file, output_folder, target_year)
     param_db = utils.read_settings("settings/settings.json", dict = "db", elem = "etats_financier.db")
     route_sqlite.create_table(query, param_db["path"], args.annee)



def execute_sql():
      # Récupération des requêtes SQL à utiliser afin de produire les fichiers
     querylist=query_sqlite.create_table_query()
     # Récupération des paramètres nécessaires à l'execution de execute_sql_queries(query_list, db_file, output_folder, target_year)
     param_db = utils.read_settings("settings/settings.json", dict = "db", elem = "etats_financier.db")
     for query in querylist:
          route_sqlite.create_table(query, param_db["path"], args.annee)
     query_list = query_sqlite.get_query(args.annee)
     #print("query_list from main.py :", query_list)
     param_db = utils.read_settings("settings/settings.json", dict = "db", elem = "etats_financier.db")
     param_files = utils.read_settings("settings/settings.json", dict = "path_data", elem = "output")
     route_sqlite.execute_sql_queries(query_list, param_db["path"], param_files["path"], args.annee)

     


def clean_output():
     param_output_1 = utils.read_settings("settings/settings.json", dict = "path_data", elem = "output_1")
     param_output_2 = utils.read_settings("settings/settings.json", dict = "path_data", elem = "output_2")

     route_datacleaning.uniformiser_csv_dossier(param_output_1["path"])
     route_datacleaning.uniformiser_csv_dossier(param_output_2["path"])


def delete_files():
     param_output_1 = utils.read_settings("settings/settings.json", dict = "path_data", elem = "output_1")
     param_output_2 = utils.read_settings("settings/settings.json", dict = "path_data", elem = "output_2")
     param_to_csv = utils.read_settings("settings/settings.json", dict = "path_data", elem = "to_csv")

     utils.delete_files(param_output_1["path"])
     utils.delete_files(param_output_2["path"])
     utils.delete_files(param_to_csv["path"])


def delete_db():
     param_db = utils.read_settings("settings/settings.json", dict = "db", elem = "etats_financier.db")
 
     utils.delete_tables(param_db["path"])


def delete_all():
     param_output_1 = utils.read_settings("settings/settings.json", dict = "path_data", elem = "output_1")
     param_output_2 = utils.read_settings("settings/settings.json", dict = "path_data", elem = "output_2")
     param_to_csv = utils.read_settings("settings/settings.json", dict = "path_data", elem = "to_csv")
     param_db = utils.read_settings("settings/settings.json", dict = "db", elem = "etats_financier.db")

     utils.delete_files(param_output_1["path"])
     utils.delete_files(param_output_2["path"])
     utils.delete_files(param_to_csv["path"])
     utils.delete_tables(param_db["path"])


def all_functions(annee):
     init_db()
     create_clean_csv(annee)
     insert_into()
     #create_table_and_insert_into(annee)
     execute_sql()
     #clean_output()
     delete_db()
     return


# Initialisation du parsing
parser = argparse.ArgumentParser()
parser.add_argument("commande", type = str, help = "Commande à exécuter")
parser.add_argument("--annee", type = int, default=None, help = "Année à générer")
args = parser.parse_args()


# Core
if __name__ == "__main__":
     __main__(args)
