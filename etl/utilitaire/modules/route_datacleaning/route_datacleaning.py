# -*- coding: utf-8 i-*-

#Modules
import pandas as pd
import sqlite3
import os
import csv
import unicodedata
import chardet
import numpy
from utils import *
from os import listdir
from datetime import datetime


def create_csv(path_in, path_out,annee):
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

     
     print("---------------------------------------------")
     print("--- DOSSIER : KEYRUS")
     folderPath = 'data/01_INPUT/KEYRUS'

     allFiles = os.listdir(folderPath)
     allFiles = [f for f in allFiles if f not in ["demo.csv", "demo.xlsx", ".gitignore"]]
     #print("allFiles :", allFiles)
     colonnes_et_types = {'COD_DEPENSE':str,'COD_REGION':str,'LIB_REGION':str,'MNT_REALISE':float,'COD_FINANCEUR':str,'COD_ENVELOPPE':str,'ANNEE':str,'Fichier Source':str}
     df_res=pd.DataFrame(columns=colonnes_et_types.keys())
     
     for inputFileName in allFiles:
          inputFilePath = folderPath + '/' + inputFileName
          #print("inputFilePath :", inputFilePath)
          print("inputFileName :", inputFileName)
          #newName = inputFileName.split('.')[0]
          #newName = utils.cleanTitle(newName)

          # read file and uniformize data
          if inputFileName.split('.')[-1].lower() == 'xlsx':
               df = pd.read_excel(inputFilePath, header=0)
          elif inputFileName.split('.')[-1].lower() == 'csv':
               df = pd.read_csv(inputFilePath, sep=';', encoding='utf-8')
          if inputFileName.split('.')[0]== 'EF_ARS_ATIH_2022':
               df_tmp=pd.read_excel('data/01_INPUT/Correspondance/transco_ATIH.xlsx')
               df = pd.merge(df, df_tmp, on='Cod_Depense', how='left')
               df['Cod_Depense'] = df['NEW_CODE_DEPENSE'].combine_first(df['Cod_Depense'])

          df = utils.cleanSrcData(df)
          
          new_df=df[['COD_DEPENSE','COD_REGION', 'LIB_REGION','MNT_REALISE','COD_FINANCEUR', 'COD_ENVELOPPE','ANNEE']]
          new_df['Fichier Source']=inputFileName
          
          df_res=pd.concat([df_res, new_df], ignore_index=True)

     print(df_res.dtypes)

     df_res['COD_REGION'] = df_res['COD_REGION'].fillna('SSA')
     df_res['COD_REGION'] = df_res['COD_REGION'].apply(lambda x: str(x).split('.')[0] if '.' in str(x) else str(x))
     df_res['COD_REGION'] = df_res['COD_REGION'].apply(lambda x: ("0"+str(x)) if (len(str(x)) == 1)  else str(x))
     df_res['COD_REGION'] = df_res['COD_REGION'].apply(lambda x: 'SSA' if (len(str(x)) == 0)  else str(x))
     df_res['COD_REGION'] = df_res['COD_REGION'].replace('','SSA')
     df_res['MNT_REALISE'] = df_res['MNT_REALISE'].replace('-   ', 0)
     df_res['MNT_REALISE']=df_res['MNT_REALISE'].fillna(0)
     df_res=df_res.astype(colonnes_et_types)

     outputFilePath = path_out + '/keyrus.csv'
     print(df['COD_REGION'].isna().sum())
     print("outputFilePath :", outputFilePath)
     utils.checkIfPathExists(outputFilePath)

     # write file
     df_res.to_csv(outputFilePath, index=None, header=True, sep=';', encoding='utf-8-sig')

     print('-- FICHIER CSV AJOUTE: keyrus')
     print(" ")

     print("---------------------------------------------")
     print(" ")
     folderPath = 'data/01_INPUT/Correspondance'

     allFiles = os.listdir(folderPath)
     allFiles = [f for f in allFiles if f not in ["demo.csv", "demo.xlsx", ".gitignore"]]
     #print("allFiles :", allFiles)
   
     for inputFileName in allFiles:
          inputFilePath = folderPath + '/' + inputFileName
          #print("inputFilePath :", inputFilePath)
          print("inputFileName :", inputFileName)
          newName = inputFileName.split('.')[0]
          #newName = utils.cleanTitle(newName)

          # read file and uniformize data
          if inputFileName.split('.')[-1].lower() == 'xlsx' or inputFileName.split('.')[-1].lower() == 'xls':
               df = pd.read_excel(inputFilePath, header=0)
          elif inputFileName.split('.')[-1].lower() == 'csv':
               df = pd.read_csv(inputFilePath, sep=';', encoding='utf-8')
          
          df = utils.cleanSrcData(df)
          

          outputFilePath = path_out + '/'+newName+'.csv'
          print("outputFilePath :", outputFilePath)
          utils.checkIfPathExists(outputFilePath)
          print(df.columns)
          # write file
          df.to_csv(outputFilePath, index=None, header=True, sep=';', encoding='utf-8-sig')

          print('-- FICHIER CSV AJOUTE:',outputFilePath)
          print(" ")

          print("---------------------------------------------")
          print(" ")
     
     df=pd.DataFrame({'ANNEE': [annee, annee-1, annee-2]})
     outputFilePath = path_out + '/REF_ANNEE.csv'
     print("outputFilePath :", outputFilePath)
     utils.checkIfPathExists(outputFilePath)
     print(df.columns)
     # write file
     df.to_csv(outputFilePath, index=None, header=True, sep=';', encoding='utf-8-sig')

     print('-- FICHIER CSV AJOUTE:',outputFilePath)
     print(" ")

     print("---------------------------------------------")
     print(" ")

def uniformiser_csv_dossier(dossier):
     """
     Permet d'uniformiser les données des fichiers csv présents au sein d'un dossier spécifique (hors demo.csv)

     Paramètre :
        - dossier : Dossier où sont situées les fichiers csv à uniformiser.
     """
     for fichier in os.listdir(dossier):
          if fichier.endswith('.csv') and fichier != 'demo.csv':
               print("File :", fichier)
               chemin = os.path.join(dossier, fichier)
               df = pd.read_csv(chemin, sep = ';')
               df.columns = [col.upper().replace("É", "E").replace("È", "E").replace("À", "A").replace("Ç", "C").replace("Ô", "O").replace("Û", "U").replace("Ù", "U") for col in df.columns]
               df = df.applymap(lambda x: str(x).upper().replace("É", "E").replace("È", "E").replace("À", "A").replace("Ç", "C").replace("Ô", "O").replace("Û", "U").replace("Ù", "U"))
               df.to_csv(chemin, index=False, sep=';')
               print("Fichier corrigé :", fichier)


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
