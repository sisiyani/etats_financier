# -*- coding: utf-8 i-*-

#Modules
import pandas as pd
import sqlite3
import os
import csv
import unicodedata
import chardet

from utils import *
from os import listdir



def create_csv(path_in, path_out):
     """
     Permet de convertir les fichiers xlsx en fichier csv.

     Paramètres :
     - path_in : chemin du dossier où se trouvent les fichiers à convertir
     - path_out : chemin du dossier où enregistrer les fichiers convertis
     """
     print("##################")
     print("### CREATE_CSV ###")
     print("##################")
     print(" ")

     # Aller dans tous les dossiers d'entrée et stocker une version csv propre dans to_csv
     allFolders = os.listdir(path_in)
     print("allFolders :", allFolders)

     for folderName in allFolders:
          print("---------------------------------------------")
          print("--- DOSSIER : ", folderName)
          folderPath = 'data/input/{}'.format(folderName)
          #print("folderPath :", folderPath)
          allFiles = os.listdir(folderPath)
          allFiles = [f for f in allFiles if f not in ["demo.csv", "demo.xlsx", ".gitignore"]]
          #print("allFiles :", allFiles)

          for inputFileName in allFiles:
               inputFilePath = folderPath + '/' + inputFileName
               print("inputFilePath :", inputFilePath)
               newName = folderName + '_' + inputFileName.split('.')[0]
               newName = utils.cleanTitle(newName)

               # read file and uniformize data
               if inputFileName.split('.')[-1].lower() == 'xlsx':
                    df = pd.read_excel(inputFilePath, header=0)
               elif inputFileName.split('.')[-1].lower() == 'csv':
                    df = pd.read_csv(inputFilePath, sep=';', encoding='utf-8')

               df.columns = [col.upper().replace("É", "E").replace("È", "E").replace("À", "A").replace("Ç", "C").replace("Ô", "O").replace("Û", "U").replace("Ù", "U").replace("'", " ").replace("–", "-") for col in df.columns]
               df = df.applymap(lambda x: str(x).upper().replace("É", "E").replace("È", "E").replace("À", "A").replace("Ç", "C").replace("Ô", "O").replace("Û", "U").replace("Ù", "U").replace("'", " ").replace("–", "-"))

               outputFilePath = path_out + '/' + newName + '.csv'
               print("outputFilePath :", outputFilePath)
               utils.checkIfPathExists(outputFilePath)

               # write file
               df.to_csv(outputFilePath, index=None, header=True, sep=';', encoding='utf-8-sig')

               print('-- FICHIER CSV AJOUTE: {}'.format(inputFileName))
               print(" ")

          print("---------------------------------------------")
          print(" ")


def cleanData(path):
     """
     Permet de nettoyer les données des fichiers csv situés au sein du dossier path.

     Paramètres :
     - path : Chemin du dossier contenant les fichiers à nettoyer
     """

     print("##################")
     print("### CLEAN_CSV ###")
     print("##################")
     print(" ")
     
     # Récupération des fichiers csv au sein de path_in (sauf demo.csv et .gitignore)
     path = path
     allFiles = listdir(path)
     allFiles = [f for f in allFiles if f not in ["demo.csv", ".gitignore"]]
     print("allFiles : ", allFiles)
     print(" ")

     # Boucle permettant de nettoyer le titre et les données fichier par fichier
     for File in allFiles:

          print("File to clean : ", File) # Nom du fichier dans la boucle

          FilePath = path + '/' + File # Chemin d'origine du fichier à nettoyer
          print('FilePath :', FilePath)

          data = pd.read_csv(FilePath, sep = ';', encoding = 'UTF-8') # Import des données à nettoyer
          #print('data :', data)

          df = pd.DataFrame(data)
          #print('df before clean :', df)

          df = utils.cleanSrcData(df) # Nettoyage des données
          print('df after clean :', df)
          
          #utils.checkIfPathExists(FilePath) # Test si le fichier existe déjà

          df.to_csv(FilePath, index = None, header = True, sep = ';', encoding = 'UTF-8')

          print(' ')



