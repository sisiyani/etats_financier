# -*- coding: utf-8 -*-

# MODULES
import sqlite3
import csv
import os

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
     nom_table = 'table_' + nom_fichier_csv.replace(' ', '_')
     print('nom table : ', nom_table)

     # Crée un curseur pour la base de données
     curseur = connexion_base_donnees.cursor()

     # Ouvre le fichier CSV
     with open(chemin_fichier_csv, 'r') as fichier_csv:
          # Lit le contenu du fichier CSV avec la bibliothèque csv
          contenu_csv = csv.reader(fichier_csv, delimiter = ';')
          print('contenu_csv :', contenu_csv)
          #for ligne in contenu_csv:
               #print('ligne contenu_csv :', ligne)

          # Récupère la première ligne du fichier CSV comme noms de colonnes
          colonnes = next(contenu_csv)
          print('colonnes :', colonnes)        
          nom_colonnes = ", ".join(colonnes)
          print('nom_colonnes :', nom_colonnes)
          nom_colonnes = nom_colonnes.replace(";", ",")
          #print('nom_colonnes :', nom_colonnes)
          curseur.execute(f"CREATE TABLE IF NOT EXISTS {nom_table} ({nom_colonnes})")

          # Insère les données dans la table
          valeurs = []
          print('contenu_csv :', contenu_csv)
          for ligne in contenu_csv:
               print('ligne :', ligne)
               valeurs.append(tuple(ligne))
          print('compter_valeurs :', compter_valeurs(valeurs[1]))
          print('valeur : ', valeurs[1])

          curseur.executemany(f"INSERT INTO {nom_table} ({nom_colonnes}) VALUES ({', '.join(['?'] * len(colonnes))})", valeurs)

     # Enregistre les modifications dans la base de données
     connexion_base_donnees.commit()
