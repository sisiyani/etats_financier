# -*- coding: utf-8 -*-

def get_query(level):
     """
     Regroupe l'ensemble des requêtes SQL à executer au sein du programme via 
     la fonction route_sqlite.execute_sql_queries().

     Paramètre :
        - level : Permet de déterminer la liste de requêtes SQL que l'on souhaite utiliser
                  Si level = 1 : Liste des requêtes à utiliser afin de créer les fichiers intermédiaires (03_OUTPUT_1)
                                 (anciens fichiers Keyrus) à partir des fichiers sources (02_TO_CSV)
 
                  Si level = 2 : Liste des requêtes à utiliser afin de créer le rapport final (04_OUTPUT_2) 
                                 à partir des fichiers intermédiaires (03_OUTPUT_1)

     ATTENTION : Afin de prendre en compte l'année demandée via la requête "python main.py execute_sql --annee XXXX",
                 il est nécessaire de noter l'année au sein de la requête sous la forme suivante : "{{YEAR}}"    
     """
     # Fonction qui retourne une liste de requête SQL à executer afin de créer les fichiers intermédiaires au sein de OUTPUT_1
     # à partir des fichiers sources (INPUT)
     if level == '1':
          query_list = [
              ("FIR_DECAISSEMENT", 
               """SELECT
                       fcf.CODE_DEPENSE as COD_DEPENSE,
                       fsb.CODE_REGION as COD_REGION,
                       fsb.LIB_REGION as LIB_REGION,
                       fsb.CP_CONSOMMES as MNT_REALISE,
                       'FIR' as COD_FINANCEUR,
                       fcf.CODE_ENV_2016 as COD_ENVELOPPE,
                       fsb.EXERCICE as ANNEE
                  FROM
                       FIR_SIBC_BUDGET fsb
                       INNER JOIN FIR_CORRESP_FIR fcf on fcf.CODE_MISSION = fsb.CODE_DESTINATION and fcf.EXERCICE = fsb.EXERCICE
                  WHERE fsb.EXERCICE = "{{YEAR}}";"""),

              ("DFAS_FRAIS_JURY",
               """SELECT
	               ddja.CODE_REGION,
	               ddja.REGION,
	               ddja.ORGANISATION_LOGISTIQUE_DES_JURYS_HORS_VAE_ET_VAE_CP,
	               ddjap.CODE_FINANCEUR,
	               ddjap.CODE_ENVELOPPE,
	               ddjap.CODE_DEPENSE,
	               ddja.EXERCICE 
                  FROM 
	               DFAS_DEPENSES_JURY_ARS ddja, DFAS_DEPENSES_JURY_ARS_PARAMETRAGE ddjap
	          WHERE ddja.EXERCICE = "{{YEAR}}";""")
          ]

     # Liste des requêtes de second niveau utilisées afin de créer le rapport final à partir des fichiers créés au sein de OUTPUT_1 
     elif level == '2':
          query_list = [
               ("TEST",
                """SELECT
                        *
                   FROM RESULT_DFAS_FRAIS_JURY_2021 dfas
                   WHERE dfas.EXERCICE = "{{YEAR}}";""")
          ]

     else:
          print("Merci de préciser quelle liste de requêtes SQL vous souhaitez utiliser au sein de la fonction get_query() appelée dans main.py")
     
     #print("query_list :", query_list)

     return query_list
