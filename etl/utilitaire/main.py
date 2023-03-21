# -*- coding: utf-8 -*-


# MODULES
import argparse
import pandas as pd

from modules import route_sqlite, route_datacleaning
from utils import utils
from os import listdir


# COMMANDES
def __main__(args):
     if args.commande == "init_database":
          init_db()
     elif args.commande == "create_csv":
          create_clean_csv()
     elif args.commande == "load_to_db":
          loadCsvToDb()
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
     route_datacleaning.create_csv("data/input", "data/to_csv")
     route_datacleaning.cleanData("data/to_csv")
     
     return



def loadCsvToDb():
     dbname = utils.read_settings('settings/settings.json', 'sqlite_db', 'name')
     print("dbname :", dbname)
     #allCsv = listdir('data/to_csv')
     #print("allCsv :", allCsv)
     #conn = connDb(dbname)
     #print("conn :", conn)
     
     print(" ")
     #for inputCsvFilePath in allCsv:
          #print("inputCsvFilePath :", inputCsvFilePath)
          #importSrcData(
          #     utils.cleanSrcData(
          #          utils.csvReader('data/to_csv' + inputCsvFilePath)),
          #          inputCsvFilePath.split('/')[-1].split('.')[0],
          #          conn,
          #          dbname)
          #print('-- FICHIER AJOUTE A LA BASE DE DONNEES: {}'.format(inputCsvFilePath))
     
     #return

 

def all_functions():
     init_db()
     create_clean_csv()
     loadCsvToDb()
     return

# Initialisation du parsing
parser = argparse.ArgumentParser()
parser.add_argument("commande", type = str, help = "Commande à exécuter")
args = parser.parse_args()

# Core
if __name__ == "__main__":
     __main__(args)



