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
     return query_list
