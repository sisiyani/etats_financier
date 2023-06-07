# -*- coding: utf-8 -*-

def get_query():
     """
     Regroupe l'ensemble des requêtes SQL à executer au sein de la fonction route_sqlite.execute_sql_queries()
     """
     # Fonction qui retourne une liste de requête SQL à executer
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
              WHERE fsb.EXERCICE >= "{{YEAR}}" - 2 AND fsb.EXERCICE <= "{{YEAR}}";""")
     ]

     return query_list
