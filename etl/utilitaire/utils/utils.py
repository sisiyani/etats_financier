# -*- coding: utf-8 -*-

# MODULES
import json
import logging
import os
import pandas as pd
import re

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

     inputExcelFIlePath = 
     outputCsvFilePath = 
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

     """

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

     text = text.replace("__", "_")
     text = text.replace("___", "_")

     text = re.sub('\[] +', '_', text)
     text = re.sub('\[^0-9a-zA-Z_-]', '',text) 
     return str(text)


def cleanSrcData(df):
     """
     Permet d'enlever les caractères spéciaux, accents, espace (_)
     """

     df.columns = [cleanTxt(i) for i in df.columns.values.tolist()]
     return df


def compter_valeurs(var):
     """
     Compte le nombre de valeurs dans une variable.
     :param var: La variable à compter.
     :return: Le nombre de valeurs dans la variable.
     """
     if isinstance(var, (list, tuple, set)):
          return len(var)
     elif isinstance(var, dict):
          return len(var.values())
     elif isinstance(var, str):
          return len(var.split())
     else:
          return 1


def uniformize_csv_files(directory):
    """
    Uniformise les données de tous les fichiers CSV d'un dossier (sauf demo.csv)
    en assurant une bonne gestion des accents et des caractères spéciaux.

    :param directory: Le chemin d'accès au dossier contenant les fichiers CSV à uniformiser
    """
    # Liste tous les fichiers CSV du dossier
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv') and f != 'demo.csv']

    # Uniformise chaque fichier CSV
    for csv_file in csv_files:
        csv_file_path = os.path.join(directory, csv_file)

        # Charge le fichier CSV en utilisant l'encodage UTF-8
        csv_data = pd.read_csv(csv_file_path, sep=';', encoding='utf-8')

        # Uniformise les données en enlevant les espaces en début et fin de chaîne et en convertissant en majuscules
        csv_data = csv_data.applymap(lambda x: x.strip().upper() if isinstance(x, str) else x)

        # Écrit le fichier CSV uniformisé en utilisant l'encodage UTF-8 et le séparateur ';'
        csv_data.to_csv(csv_file_path, sep=';', index=False, encoding='utf-8-sig')

        print('csv_file clean :', csv_file)
