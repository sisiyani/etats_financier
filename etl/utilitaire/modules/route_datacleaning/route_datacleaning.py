# -*- coding: utf-8 i-*-

#Modules
import pandas as pd
import sqlite3
import os

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

     # Aller dans tous les dossiers d'entrée et stockez une version csv propre dans to_csv
     allFolders = listdir(path_in)
     print("allFolders :",allFolders)

     for folderName in allFolders:
          print("---------------------------------------------")
          print("--- DOSSIER : ", folderName)
          folderPath = 'data/input/{}'.format(folderName)
          #print("folderPath :", folderPath)
          allFiles = listdir(folderPath)
          #print("allFiles :", allFiles)

          for inputFileName in allFiles:
               inputFilePath = folderPath + '/' + inputFileName
               #print("inputFilePath :", inputFilePath)
               outputFilePath = path_out + '/' + inputFileName.split('.')[0] + '.csv'
               #print("outputFilePath :", outputFilePath)

               if inputFileName == 'demo.csv' or inputFileName == 'demo.xlsx' or inputFileName == '.gitignore':
                    print("-- FICHIER DE DEMO : ", inputFileName)
               elif inputFileName.split('.')[-1].lower()=='xlsx':
                    utils.convertXLSXtoCSV(inputFilePath, outputFilePath)
                    print('-- FICHIER CONVERTI EN CSV ET AJOUTE: {}'.format(inputFileName))
               elif inputFileName.split('.')[-1].lower()=='csv':
                    df = pd.read_csv(inputFilePath, sep = ';', encoding = 'latin-1')
                    df.to_csv(outputFilePath, index = None, header = True, sep = ';', encoding = 'UTF-8')
                    print('-- FICHIER CSV AJOUTE: {}'.format(inputFileName))
          print("---------------------------------------------")
          print(" ")


def cleanData(path_in):
     """
     Permet de créer de nettoyer les fichiers csv en créant de nouveaux fichiers XXXX_clean.csv

     Paramètres :
     - path_in : Chemin du dossier contenant les fichiers csv à nettoyer
     """

     print("##################")
     print("### CLEAN_CSV ###")
     print("##################")
     print(" ")

     folderPath = path_in
     allFiles = listdir(folderPath)
     print("allFiles : ", allFiles)
     print(" ")

     for File in allFiles:
          if File[-10:] != '_clean.csv':
               print("File to clean : ", File)

               inputFilePath = folderPath + '/' + File
               print('inputFilePath :', inputFilePath)
               outputFilePath = folderPath + '/' + File.split('.')[0] + '_clean.csv'
               print('outputFilePath :', outputFilePath)

               utils.checkIfPathExists(outputFilePath)

               data = pd.read_csv(inputFilePath, sep = ';', encoding = 'UTF-8')
               #print('data :', data)

               df = pd.DataFrame(data)
               #print('df before clean :', df)

               df = utils.cleanSrcData(df)
               print('df after clean :', df)

               df.to_csv(outputFilePath, index = None, header = True, sep = ';', encoding = 'UTF-8')

          print(' ')
