# -*- coding: utf-8 -*-

def get_query():
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
                   JOIN CORRESP_CODE_REGION_ARS_2021 ccra ON fedf.LIBELLE_ETABLISSEMENT = ccra.LIBELLE_ARS
                   JOIN FIR_2021_CORRESP fc ON fedf.CODE_DESTINATION = fc.CODE_MISSION
                   WHERE fedf.SG1 = 'FIR';""")
     ]

     return query_list       
                
          
