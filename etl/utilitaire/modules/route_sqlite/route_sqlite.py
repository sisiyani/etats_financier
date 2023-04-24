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


def creer_table_csv(chemin_fichier_csv, connexion_base_donnees):
     """
     Crée une table dans une base de données SQLite à partir d'un fichier CSV
     et y insère les données du fichier.
     Le nom de la table est le nom du fichier CSV sans l'extension.
     :param chemin_fichier_csv: Le chemin complet du fichier CSV
     :param connexion_base_donnees: La connexion à la base de données SQLite
     """
     # Récupère le nom du fichier CSV sans l'extension pour le nom de la table
     nom_fichier_csv = os.path.splitext(os.path.basename(chemin_fichier_csv))[0]
     nom_table = nom_fichier_csv.replace(' ', '_')
     print('nom table : ', nom_table)

     # Crée un curseur pour la base de données
     curseur = connexion_base_donnees.cursor()

     # Ouvre le fichier CSV
     with open(chemin_fichier_csv, 'r') as fichier_csv:
          # Lit le contenu du fichier CSV avec la bibliothèque csv
          contenu_csv = csv.reader(fichier_csv, delimiter = ';')
          #print('contenu_csv :', contenu_csv)
          #for ligne in contenu_csv:
               #print('ligne contenu_csv :', ligne)

          # Récupère la première ligne du fichier CSV comme noms de colonnes
          colonnes = next(contenu_csv)
          print('colonnes :', colonnes)        
          nom_colonnes = ", ".join(colonnes)
          #nom_colonnes = nom_colonnes.replace(";", ", ")
          #print('nom_colonnes :', nom_colonnes)
          print(" ")
          curseur.execute(f"CREATE TABLE IF NOT EXISTS {nom_table} ({nom_colonnes})")

          # Insère les données dans la table
          valeurs = []
          for ligne in contenu_csv:
               print('ligne :', ligne)
               valeurs.append(tuple(ligne))
               
          print('compte_valeurs :', utils.compter_valeurs(valeurs[1]))
          
          curseur.executemany(f"INSERT INTO {nom_table} ({nom_colonnes}) VALUES ({', '.join(['?'] * len(colonnes))})", valeurs)
          print(" ")

     # Enregistre les modifications dans la base de données
     connexion_base_donnees.commit()


def execute_sql_queries(query_list, db_file, output_folder):
     # Connexion à la bdd
     conn = sqlite3.connect(db_file)

     # Pour chaque requête SQL dans la liste
     for i, (query_name, query) in enumerate(query_list):
          print(f"Exécution de la requête {i+1}/{len(query_list)} : {query_name}")

          # Exécution de la requête SQL
          df = pd.read_sql(query, conn)

          # Enregistrement du résultat sous forme de fichier CSV dans le dossier spécifié en argument
          output_file = f"{query_name}.csv"
          df.to_csv(f"{output_folder}/{output_file}", index = False)
          print(f"Fichier {output_file} crée correctement et enregistré au sein de {output_folder}")

     # Fermeture de la connexion à la base de données
     conn.close()
