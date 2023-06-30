# -*- coding: utf-8 -*-

# MODULES
import sqlite3
import csv
import os
import pandas as pd

from os import listdir
from utils import *
from .query_sqlite import *

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


def insert_into_db(db_path, files_path):
     """
     Crée une table dans une base de données SQLite à partir d'un fichier CSV
     et y insère les données du fichier.
     Le nom de la table est le nom du fichier CSV sans l'extension.
     
     Paramètres :
        - files_path : Chemin du dossier où sont enregistrés les fichiers CSV à insérer au sein de la base de données
        - db_path : Chemin de connexion à la base de données SQLite
     """

     # Récupération des fichiers présents au sein du dossier source "files_path"
     files = []
     
     for file in os.listdir(files_path):
          if file.split('/')[-1] != 'demo.csv':
               print('file :', file)
               files.append(files_path + '/' + file)

     print("")
     print("files :", files)
     print("")   

     # Connexion à la base de données
     db_path = sqlite3.connect(db_path)

     for file in files:
          # Récupère le nom du fichier CSV sans l'extension pour le nom de la table
          nom_fichier = os.path.splitext(os.path.basename(file))[0]  
          nom_table = nom_fichier.replace(' ', '_')
          print('nom table : ', nom_table)

          # Crée un curseur pour la base de données
          curseur = db_path.cursor()

          # Ouvre le fichier CSV
          with open(file, 'r') as fichier_csv:
               # Lit le contenu du fichier CSV avec la bibliothèque csv
               contenu_csv = csv.reader(fichier_csv, delimiter = ';')
               #print('contenu_csv :', contenu_csv)

               # Récupère la première ligne du fichier CSV comme noms de colonnes
               colonnes = next(contenu_csv)
               print('colonnes :', colonnes)        
               nom_colonnes = ", ".join(colonnes)
               print(" ")

               # Supprime les données existantes de la table si elle existe déjà
               curseur.execute(f"DROP TABLE IF EXISTS {nom_table}")

               # Créer la table
               curseur.execute(f"CREATE TABLE IF NOT EXISTS {nom_table} ({nom_colonnes})")

               # Insère les données dans la table
               valeurs = []
               for ligne in contenu_csv:
                    print('ligne :', ligne)
                    valeurs.append(tuple(ligne))
               
               print('compte_valeurs :', utils.compter_valeurs(valeurs[0]))
          
               curseur.executemany(f"INSERT OR REPLACE INTO {nom_table} ({nom_colonnes}) VALUES ({', '.join(['?'] * len(colonnes))})", valeurs)
               print(" ")

          # Enregistre les modifications dans la base de données
          db_path.commit()

     db_path.close()


def execute_sql_queries(query_list, db_file, output_folder, target_year):
    """
    Execute les requêtes SQL présentes au sein de la liste query_list (voir le fichier query_sqlite.py)

    Paramètres :
        - query_list : Liste des requêtes à executer.
        - db_file : Base de données où executer les requêtes.
        - output_folder : Dossier où exporter sous format csv les résultats des requêtes
        - target_year : Année cible pour les données à extraire
    """
    years = [target_year, target_year - 1, target_year - 2]
        
    # Connexion à la base de données
    conn = sqlite3.connect(db_file)

    # Pour chaque requête SQL dans la liste
    for i, (query_name, query) in enumerate(query_list):
        print(f"Exécution de la requête {i+1}/{len(query_list)} : {query_name}")
        

        # DataFrame pour stocker les résultats de chaque requête
        dfs = []

        for year in years:
            query_with_year_constraint = query.replace("{{YEAR}}", str(year))
            #print('query_with_year_constraint :', query_with_year_constraint)

            # Exécution de la requête SQL
            df = pd.read_sql(query_with_year_constraint, conn)

            # Ajout du DataFrame à la liste
            dfs.append(df)

        # Concaténation des DataFrames
        result_df = pd.concat(dfs)

        # Enregistrement du résultat dans un fichier CSV
        output_file = f"RESULT_{query_name}_{target_year}.csv"
        output_path = os.path.join(output_folder, output_file)
        result_df.to_csv(output_path, sep=";", index=False, encoding='utf-8')
        print(f"Fichier {output_file} créé correctement et enregistré dans {output_folder}")

    # Fermeture de la connexion à la base de données
    conn.close()



