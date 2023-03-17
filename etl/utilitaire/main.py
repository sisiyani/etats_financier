# -*- coding: utf-8 -*-


# MODULES
import argparse

from modules import route_sqlite
from utils import utils
from os import listdir

# COMMANDES
def __main__(args):
     if args.commande == "init_database":
          init_db()
     elif args.commande == "create_csv":
          create_csv()
     elif args.commande == "load_to_db":
          loadCsvToDb
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


def create_csv():
     print("##################")
     print("### CREATE_CSV ###")
     print("##################")
     print(" ")
    
     # Aller dans tous les dossiers d'entrée et stockez une version csv propre dans to_csv
     allFolders = listdir('data/input')

     for folderName in allFolders:
          if folderName != '.gitignore':
               print("--- ENTREE DANS LA BOUCLE ---")
               folderPath = 'data/input/{}'.format(folderName)
               allFiles = listdir(folderPath)
          
               for inputFileName in allFiles:
                    inputFilePath = folderPath + '/' + inputFileName
                    outputFilePath = 'data/to_csv/' + inputFileName.split('.')[0] + '.csv'
          
               if inputFileName == 'demo.csv' or inputFileName == 'demo.xlsx' or inputFileName == '.gitignore':
                    print("-- FICHIER DE DEMO --")
               elif inputFileName.split('.')[-1].lower()=='xlsx':
                    utils.convertXLSXtoCSV(inputFilePath, outputFilePath)
                    print('-- FICHIER CONVERTI EXCEL ET AJOUTE: {}'.format(inputFileName))
               elif inputFileName.split('.')[-1].lower()=='csv':
                    df = pd.read_csv(inputFilePath, sep = ';', encoding = 'latin-1')
                    df.to_csv(outputFilePath, index = None, header = True, sep = ';', encoding = 'UTF-8')
                    print('-- FICHIER CSV AJOUTE: {}'.format(inputFileName))
     return


def loadCsvToDb():
     dbname = utils.read_settings('settings/settings.json', 'db', 'name')
     allCsv = listdir('data/to_csv')
     conn = connDb(dbname)

     for inputCsvFilePath in allCsv:
          importSrcData(
               utils.cleanSrcData(
                    utils.csvReader('data/to_csv' + inputCsvFilePath)),
                    inputCsvFilePath.split('/')[-1].split('.')[0],
                    conn,
                    dbname)
          print('-- FICHIER AJOUTE A LA BASE DE DONNEES: {}'.format(inputCsvFilePath))
     
     return

 

def all_functions():
     init_db()
     create_csv()
     loadCsvToDb()
     return

# Initialisation du parsing
parser = argparse.ArgumentParser()
parser.add_argument("commande", type = str, help = "Commande à exécuter")
args = parser.parse_args()

# Core
if __name__ == "__main__":
     __main__(args)



