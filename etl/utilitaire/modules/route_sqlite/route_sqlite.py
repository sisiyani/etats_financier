# -*- coding: utf-8 -*-

# MODULES
import sqlite3
import csv

from os import listdir

def deploy_database(database = "database"):
     """
     Déploiement de la database 
   
     Paramètre : 
          - database : Adresse où déployer la database
     """

     try:     
          conn = sqlite3.connect(database = database)
          cursor = conn.cursor()
          print("--- BASE DE DONNEES ETATS_FINANCIER CREE CORRECTEMENT ET CONNECTEE A SQLITE ---")

          sql = "SELECT sqlite_version();"
          cursor.execute(sql)
          res = cursor.fetchall()
          print("--- VERSION DE SQLITE : ", res)
          
          cursor.close()
          conn.close()
          print("--- CONNEXION SQLITE FERMEE ---")

     except sqlite3.Error as error:
          print("--- ERREUR LORS DE LA CONNEXION A SQLITE : ", error) 


def create_table_insert_csv_to_sqlite(path, db_path):
     """
     Insert les données issues des fichiers csv au sein de la bdd sqlite.

     Paramètres : 
     - csv_file_path : Fichier csv à insérer
     - table_name : Nom de la table à créer
     - database : Nom de la base de données où insérer les données
     """
     # Connect to the SQLite database
     conn = sqlite3.connect(db_path)
     #cursor = conn.cursor()

     file_list = []

     files = listdir(path)
     for name in files:
          if name[-9:] == 'clean.csv':
               file_list.append(path + '/' + name)

     # Pour chaque fichier CSV dans la liste
     for file in file_list:
          # Récupère le nom de la table à partir du nom du fichier CSV
          file_name1 = file.split('.')[0]
          print("file_name1 :", file_name1)
          file_name2 = file_name1.split('/')[-1]
          print("file_name2 :", file_name2)
          table_name = 'table_' + file_name2

          # Création d'une nouvelle table pour le fichier CSV
          with open(file, 'r') as f:
               reader = csv.reader(f)
               headers = next(reader)
               columns = ', '.join([f'{h} TEXT' for h in headers])
               conn.execute(f"""CREATE TABLE {table_name} ({columns})""")

          # Import les données au sein d'une nouvelle table de la base de données
          with open(file, 'r') as f:
               reader = csv.reader(f)
               next.executemany(f'INSERT INTO {table_name} VALUES ({",".join("?"*len(headers))})', reader)

     conn.commit()
     conn.close()
