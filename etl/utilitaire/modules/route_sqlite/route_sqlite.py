# -*- coding: utf-8 -*-

# MODULES
import sqlite3
import csv
import os
import pandas as pd
import numpy as np
import shutil
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
          print(file)
          nom_fichier = os.path.splitext(os.path.basename(file))[0]  
          nom_table = nom_fichier.replace(' ', '_')
          print('nom table : ', nom_table)

          # Crée un curseur pour la base de données
          curseur = db_path.cursor()

          # Ouvre le fichier CSV
          with open(file, 'r', encoding='utf-8-sig') as fichier_csv:
               # Lit le contenu du fichier CSV avec la bibliothèque csv
               contenu_csv = csv.reader(fichier_csv, delimiter = ';')
               #print('contenu_csv :', contenu_csv)

               # Récupère la première ligne du fichier CSV comme noms de colonnes
               colonnes = next(contenu_csv)
               #print('colonnes :', colonnes)        
               nom_colonnes = ", ".join(colonnes)
               print(" ")

               # Supprime les données existantes de la table si elle existe déjà
               s="DROP TABLE IF EXISTS "+nom_table
               print(s)
               curseur.execute(s)

               # Créer la table
               curseur.execute(f"CREATE TABLE IF NOT EXISTS {nom_table} ({nom_colonnes})")

               # Insère les données dans la table
               valeurs = []
               for ligne in contenu_csv:
                    #print('ligne :', ligne)
                    valeurs.append(tuple(ligne))
               
               print('compte_valeurs :', utils.compter_valeurs(valeurs[0]))
          
               curseur.executemany(f"INSERT OR REPLACE INTO {nom_table} ({nom_colonnes}) VALUES ({', '.join(['?'] * len(colonnes))})", valeurs)
               print(" ")

          # Enregistre les modifications dans la base de données
          db_path.commit()

     db_path.close()

def create_table(query,db_file,target_year):
     conn = sqlite3.connect(db_file)
     # Crée un curseur pour la base de données
     curseur = conn.cursor()
     # Créer la table
     curseur.execute(query)
     # Enregistre les modifications dans la base de données
     conn.commit()



def execute_sql_queries(queries, db_file, output_folder,target_year):
    """
    Execute les requêtes SQL présentes au sein de la liste query_list (voir le fichier query_sqlite.py)

    Paramètres :
        - query_list : Liste des requêtes à executer.
        - db_file : Base de données où executer les requêtes.
        - output_folder : Dossier où exporter sous format csv les résultats des requêtes
        - target_year : Année cible pour les données à extraire
    """
    years = [target_year, target_year - 1, target_year - 2]
    template=os.path.join(output_folder, "template.xlsx")
    n='Réalisé année {} en National'.format(target_year)
    n_1='Réalisé année {} en National'.format(target_year - 1)
    n_2='Réalisé année {} en National'.format(target_year - 2)
    v='Variation National'+str(target_year - 1)+'/'+str(target_year) 
    nr='Réalisé année {}'.format(target_year)
    nr_1='Réalisé année {}'.format(target_year - 1)
    nr_2='Réalisé année {}'.format(target_year - 2)
    p='Part dans dépenses nationales'
    vr='Variation '+str(target_year - 1)+'/'+str(target_year)   
    # Connexion à la base de données
    conn = sqlite3.connect(db_file)
    query_national=queries["destination_FRANCE"]
    df_national=pd.read_sql(query_national, conn)
    
    df_national[v] = np.where((df_national[n].notna()) & df_national[n_1].notna() &(df_national[n_1] > 0),
                              (df_national[n] - df_national[n_1]) /df_national[n_1],
                              np.nan)
    query_nationalF=queries["destination_FRANCE"]
    df_nationalF=pd.read_sql(query_nationalF, conn)

    #print('----------------------',df_national,df_national.shape[0])
    ref_region=pd.read_excel('data/01_INPUT/Correspondance/REF_REGION.xlsx')
    for index, row in ref_region.iterrows():
     COD_REGION = row['COD_REGION']
     LIB_REGION = row['LIB_REGION']
     print(COD_REGION,LIB_REGION)
     output_file=f"RESULT_{LIB_REGION}_{target_year}.xlsx"
     output_path = os.path.join(output_folder, output_file)
     shutil.copyfile(template, output_path)
     query_regional=queries['destination_REGION'].replace("PARAM_REGION", COD_REGION)
     query_regionalF=queries['financeur_REGION'].replace("PARAM_REGION", COD_REGION)
     #print(query_regional)
     df_regional=pd.read_sql(query_regional, conn)
     df_regionalF=pd.read_sql(query_regionalF, conn)
     #print(df_regional,df_regional.shape[0])
     df_regional[vr] = np.where((df_regional[nr].notna()) & df_regional[nr_1].notna() &(df_regional[nr_1] > 0),
                               (df_regional[nr] - df_regional[nr_1] )/df_regional[nr_1],
                               np.nan)
     
     df_res = pd.merge(df_regional, df_national, on='LIBELLE')
     df_res[p]=np.where((df_res[n].notna()) & df_res[nr].notna(),
                                                       df_res[nr] /df_res[n],
                                                       np.nan)
     df_resF = pd.merge(df_regionalF, df_nationalF, on='LIBELLE')
     df_resF[p]=np.where((df_res[n].notna()) & df_res[nr].notna(),
                                                       df_res[nr] /df_res[n],
                                                       np.nan)
     #print(df_res,df_res.shape[0],df_res.columns)
     columns=['LIBELLE',nr_2,nr_1,nr,vr,p,n_2,n_1,n,v]
     columnsF=['LIBELLE',nr,p,n]
     
     
     # Enregistrement du résultat dans un fichier CSV
     output_file = f"RESULT_{LIB_REGION}_{target_year}.xlsx"
     output_path = os.path.join(output_folder, output_file)
     with pd.ExcelWriter(output_path, mode='a', engine="openpyxl",if_sheet_exists='overlay') as writer:
          df_res.to_excel(writer, sheet_name="Etat financier Destination", encoding='utf-8',startcol=3,startrow=3,index=False,columns=columns)
          df_res.to_excel(writer, sheet_name="Etat financier Financeur", encoding='utf-8',startcol=3,startrow=3,index=False,columns=columns)
     print(f"Fichier {output_file} créé correctement et enregistré dans {output_folder}")

    # Fermeture de la connexion à la base de données
    conn.close()



