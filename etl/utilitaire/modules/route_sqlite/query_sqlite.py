# -*- coding: utf-8 -*-

def get_query():
     """
     Regroupe l'ensemble des requêtes SQL à executer au sein de la fonction route_sqlite.execute_sql_queries()
     """
     # Fonction qui retourne une liste de requête SQL à executer
     query_list = [
          ("FIR_DECAISSEMENT_2021", 
           """WITH FIR_1 AS (
              SELECT
                   *,
                   CASE
                        WHEN CODE_DESTINATION_RANG_3 = ''
                             THEN CODE_DESTINATION_RANG_2
                        ELSE CODE_DESTINATION_RANG_3
                   END AS CODE_DESTINATION
              FROM FIR_2021_EXECUTION_DG_FIR
              )
              SELECT
                   ccra.CODE_REGION,
                   ccra.LIBELLE_REGION,
                   fedf.EXERCICE,
                   fedf.LIBELLE_ETABLISSEMENT,
                   fedf.SG1,
                   fedf.LIBELLE_DESTINATION_DE_RANG_1,
                   fedf.CODE_DESTINATION_RANG_2,
                   fedf.LIBELLE_DESTINATION_DE_RANG_2,
                   fedf.CODE_DESTINATION_RANG_3,
                   fedf.LIBELLE_DESTINATION_DE_RANG_3,
                   fedf.LIBELLE_ENVELOPPE,
                   fedf.DECAISSEMENTS_CP,
                   fedf.CODE_DESTINATION,
                   fc.CODE_DEPENSE,
                   fc.CODE_ENV_2016 AS CODE_ENVELOPPE,
                   fc.LIBELLE AS LIBELLE_CODE_DESTINATION
              FROM
                   FIR_1 fedf
                   INNER JOIN CORRESP_CODE_REGION_ARS_2021 ccra ON fedf.LIBELLE_ETABLISSEMENT = ccra.LIBELLE_ARS
                   INNER JOIN FIR_2021_CORRESP fc ON fedf.CODE_DESTINATION = fc.CODE_MISSION
                   WHERE fedf.SG1 = 'FIR';"""),

          ("DFAS_DEPENSES_ARS_PERSONNEL_2021",
           """WITH ETAT AS (
              SELECT
                   'EF-AD-45' AS CODE_DEPENSE,
                   'DEPENSES_DE_PERSONNEL_DE_FONCTIONNEMENT_ET_D_INVESTISSEMENT_DES_ARS' AS LIBELLE_DEPENSE,
                   def.ARS_2021 AS ARS,
                   def.DEPENSES_DE_PERSONNEL_DE_FONCTIONNEMENT_ET_D_INVESTISSEMENT_DES_ARS_PART_ETAT AS MONTANT,
                   'ETAT' AS LIBELLE_FINANCEUR,
                   'EF-CE-2-1' AS CODE_FINANCEUR,
                   'programme 124 "Conduite et soutien des politiques sanitaires et sociales" (données partielles)' AS TEST2,
                   '2021' AS ANNEE
              FROM DFAS_ETATS_FINANCIERS_2021 def
              WHERE def.ARS_2021 != 'TOTAL'
              ),
              AM AS (
              SELECT
                   'EF-AD-45' AS CODE_DEPENSE,
                   'DEPENSES_DE_PERSONNEL_DE_FONCTIONNEMENT_ET_D_INVESTISSEMENT_DES_ARS' AS LIBELLE_DEPENSE,
                   def.ARS_2021 AS ARS,
                   def.DEPENSES_DE_PERSONNEL_DE_FONCTIONNEMENT_ET_D_INVESTISSEMENT_DES_ARS_PART_ASSURANCE_MALADIE AS MONTANT,
                   'AM' AS LIBELLE_FINANCEUR,
                   'EF-AM-2-6' AS CODE_FINANCEUR,
                   'programme 124 "Conduite et soutien des politiques sanitaires et sociales" (données partielles)' AS TEST2,
                   '2021' AS ANNEE
              FROM DFAS_ETATS_FINANCIERS_2021 def
              WHERE def.ARS_2021 != 'TOTAL'
              )
              SELECT *
              FROM ETAT
              UNION
              SELECT *
              FROM AM
              ORDER BY LIBELLE_FINANCEUR DESC;"""),

          ("DFAS_FRAIS_JURY_2021",
           """WITH DFAS as (
              SELECT *
              FROM DFAS_DREETS_124_CREDITS_FRAIS_DE_JURY_2021
              WHERE DREETS_124_2021 NOT IN ('TOTAL', 'TOTAL METROPOLE', 'TOTAL OUTRE MER')
              )
              SELECT
                   'EF-AD-4' AS CODE_DEPENSE,
                   '' AS LIBELLE_DEPENSE,
                   ccra.CODE_REGION,
                   DFAS.DREETS_124_2021 AS ARS,
                   DFAS.ORGANISATION_LOGISTIQUE_DES_JURYS_HORS_VAE_ET_VAE_CP AS MONTANT,
                   'ETAT' AS LIBELLE_FINANCEUR,
                   'EF-CE-2-1' AS CODE_FINANCEUR,
                   '' AS TEST,
                   '2021' AS ANNEE
              FROM DFAS
                   LEFT JOIN CORRESP_CODE_REGION_ARS_2021 ccra ON DFAS.DREETS_124_2021 = ccra.LIBELLE_REGION;""")      
     ]

     return query_list       
                
          
