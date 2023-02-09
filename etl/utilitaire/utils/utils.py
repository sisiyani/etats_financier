# coding: utf-8

# MODULES
import json
import logging
import os

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
     logging.info("Lecture param config " + path_in ".")
     return param_config 
