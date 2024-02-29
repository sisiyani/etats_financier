# -*- coding: utf-8 -*-

# MODULES
import json
import logging
import os
import pandas as pd
import re
import sqlite3

from unidecode import unidecode


def read_settings(path_in, dict, elem):
     """
     Permet de lire le document settings et retourne les informations souhaitées au format dictionnaire

     Paramètres : 
        - path_in : Chemin du dossier settings où sont stockées les informations.
        - dict : Dictionnaire contenant les informations que l'on recherche.
        - elem : Elément au sein du dictionnaire dont on souhaite retourner les informations.
     """
     with open(path_in) as f:
          dict_ret = json.load(f)
     L_ret = dict_ret[dict]
     param_config = {}
     for param in L_ret:
          if param["name"] == elem:
               param_config = param.copy()
     logging.info("Lecture param config " + path_in + ".")
     return param_config 


def checkIfPathExists(file):
     """
     Permet de vérifier le fichier 

     Paramètre :
        - file : Fichier à vérifier
     """
     if os.path.exists(file):
          os.remove(file)
          print("Ancier fichier", file, "écrasé")


def convertXLSXtoCSV(inputExcelFilePath, outputCsvFilePath):
     """
     Permet de convertir les fichiers XLSX en fichier Excel

     Paramètres :
        - inputExcelFIlePath = Chemin du dossier où sont enregistrés les fichiers Excel 
        - outputCsvFilePath = Chemin du dossier où enregistrer les fichiers convertis en CSV
     """
     try:
          excelFile = pd.read_excel(inputExcelFilePath, header = 0, engine = 'openpyxl')
          checkIfPathExists(outputCsvFilePath)

          excelFile.to_csv(outputCsvFilePath, index = None, header = True, sep = ";", encoding = 'utf-8-sig')
          return outputCsvFilePath
     
     except ValueError as err:
          print(err)
          return str(err)


def cleanTitle(filename):
     """
     Permet d'uniformiser le nom d'un fichier.

     Paramètre :
        - filename : Nom du fichier à uniformiser.
     """
     filename = unidecode(filename.upper(), 'utf-8')

     chars_to_replace = [',', ' ', ';', '-', ","]

     for c in chars_to_replace:
          filename = filename.replace(c, '_')
 
     return filename


def cleanTxt(text):
     """
     Uniformise les colonnes d'un fichier.
     
     Paramètre : 
        - text : Texte à uniformiser.
     """
     print("Text-----", text)
     text=text.rstrip()
     if text == 'Mnt_Realise_Rembourse':
          text='Mnt_Realise'
     try:
          text = unidecode(text.lower(), 'utf-8')
     except (TypeError, NameError):
               pass

     text = unidecode(text.upper())
     text = text.encode('ascii', 'ignore')
     text = text.decode('utf-8')
     text = text.replace(",","")
     text = text.replace(" - ", "_")
     text = text.replace(" -", "_")
     text = text.replace("- ","_")
     text = text.replace("-","_")
     text = text.replace(" ", "_")
     text = text.replace("'", "_")
     text = text.replace("/", "_")
     text = text.replace("(", "_").replace(")", "")
     text = text.replace("%", "POURCENT")

     text = text.replace("__", "_")
     text = text.replace("___", "_")

     text = re.sub('\[] +', '_', text)
     text = re.sub('\[^0-9a-zA-Z_-]', '',text) 
     return str(text)


def cleanSrcData(df):
     """
     Permet d'enlever les caractères spéciaux, accents, espace (_)
     
     Paramètre :
        - df : Dataframe à uniformiser
     """
     
     df.columns = [cleanTxt(i) for i in df.columns.values.tolist()]
     return df


def compter_valeurs(var):
     """  
     Compte le nombre de valeurs dans une variable.
        - param var : La variable à compter.
        - return : Le nombre de valeurs dans la variable.
     """  
     if isinstance(var, (list, tuple, set)):
          return len(var)
     elif isinstance(var, dict):
          return len(var.values())
     elif isinstance(var, str):
          return len(var.split())
     else:
          return 1


def delete_files(path):
     """
     Supprime les fichiers au sein du dossier sélectionné (sauf fichier de démo).

     Paramètre :
        - path : Chemin du dossier où supprimer les fichiers.
     """
     for filename in os.listdir(path):
          if not filename.startswith('demo'):
               os.remove(os.path.join(path, filename))
               print('Fichier supprimé :', filename)


def delete_tables(database_path):
     """
     Supprime les tables au sein de la base de données sélectionnée.

     Paramètre :
        - database_path : Chemin de la base de données où supprimer les tables.
     """
     conn = sqlite3.connect(database_path)
     cursor = conn.cursor()

     # Récupère le nom des tables de la bdd
     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
     tables = cursor.fetchall()

     # Supprime chaque table de la bdd
     for table in tables:
          cursor.execute(f"DROP TABLE {table[0]};")
          print("Table supprimée :", table)

     conn.commit()
     conn.close()
