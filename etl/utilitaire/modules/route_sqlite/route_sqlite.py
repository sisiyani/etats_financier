# -*- coding: utf-8 -*-

# MODULES
import sqlite3

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
          print("--- VERSION DE SQLITE : ", res, " ---")
          
          cursor.close()
          conn.close()
          print("--- CONNEXION SQLITE FERMEE ---")

     except sqlite3.Error as error:
          print("--- ERREUR LORS DE LA CONNEXION A SQLITE : ", error) 

