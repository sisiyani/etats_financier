# -*- coding: utf-8 -*-

def create_table_query():
     querylist=["""CREATE TABLE IF NOT EXISTS valeur AS
               select  ra.ANNEE ,rr.COD_REGION ,t.LIBELLE,tc.CODE, (WITH pere(PERE_COD_DEPENSE,COD_DEPENSE)  AS (
						SELECT PERE_COD_DEPENSE,COD_DEPENSE
						FROM REF_DEPENSE
						WHERE  COD_DEPENSE IS tc.CODE
						UNION ALL
						SELECT r.PERE_COD_DEPENSE,r.COD_DEPENSE
						FROM   REF_DEPENSE r, pere p
						WHERE  r.PERE_COD_DEPENSE = p.COD_DEPENSE 
						)
					SELECT sum(k.MNT_REALISE) AS VALEUR
					FROM  pere p, keyrus k
					where  k.COD_DEPENSE =p.COD_DEPENSE and k.ANNEE=ra.ANNEE and k.COD_REGION is rr.COD_REGION ) as "valeur"
               from REF_REGION rr ,REF_ANNEE ra ,titre_code tc, titre t
               where t.ID=tc.ID ;""",
               """CREATE TABLE IF NOT EXISTS finance AS
               select  ra.ANNEE ,rr.COD_REGION ,t.LIBELLE,tc.CODE, (WITH pere(PERE_COD_ENVELOPPE,COD_ENVELOPPE)  AS (
						SELECT PERE_COD_ENVELOPPE,COD_ENVELOPPE
						FROM REF_ENVELOPPE
						WHERE  COD_ENVELOPPE IS tc.CODE
						UNION ALL
						SELECT r.PERE_COD_ENVELOPPE,r.COD_ENVELOPPE
						FROM   REF_ENVELOPPE r, pere p
						WHERE  r.PERE_COD_ENVELOPPE = p.COD_ENVELOPPE 
						)
					SELECT sum(k.MNT_REALISE) AS FINANCE
					FROM  pere p, keyrus k
					where  k.COD_ENVELOPPE =p.COD_ENVELOPPE and k.ANNEE=ra.ANNEE and k.COD_REGION is rr.COD_REGION ) as "finance"
               from REF_REGION rr ,REF_ANNEE ra ,titre_code_financeur tc, titre_financeur t
               where t.ID=tc.ID ;"""
     ]
     return querylist

def get_query(annee):
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
     

     # Liste des requêtes de second niveau utilisées afin de créer le rapport final à partir des fichiers créés au sein de OUTPUT_1 
    
     query_list = {"destination_FRANCE":
               """select t.ID,v.LIBELLE ,
          ROUND((SUM(CASE WHEN v.ANNEE  = '{}' THEN v.valeur ELSE 0 END)/1000000.00),2) AS 'Réalisé année {} en National',
          ROUND((SUM(CASE WHEN v.ANNEE  = '{}' THEN v.valeur ELSE 0 END)/1000000.00),2) AS 'Réalisé année {} en National',
          ROUND((SUM(CASE WHEN v.ANNEE  = '{}' THEN v.valeur ELSE 0 END)/1000000.00),2) AS 'Réalisé année {} en National' 
          from valeur v, titre t
          where v.LIBELLE =t.LIBELLE 
          group by t.ID ,v.LIBELLE 
          order by t.ID;
          """.format(annee-2,annee-2,annee-1,annee-1,annee,annee),
          "destination_REGION":
               """select t.ID,v.LIBELLE ,
          ROUND((SUM(CASE WHEN v.ANNEE  = '{}' THEN v.valeur ELSE 0 END)/1000000.00),2) AS 'Réalisé année {}',
          ROUND((SUM(CASE WHEN v.ANNEE  = '{}' THEN v.valeur ELSE 0 END)/1000000.00),2) AS 'Réalisé année {}',
          ROUND((SUM(CASE WHEN v.ANNEE  = '{}' THEN v.valeur ELSE 0 END)/1000000.00),2) AS 'Réalisé année {}' 
          from valeur v, titre t
          where v.LIBELLE =t.LIBELLE and v.COD_REGION ='PARAM_REGION'
          group by t.ID ,v.LIBELLE 
          order by t.ID;
          """.format(annee-2,annee-2,annee-1,annee-1,annee,annee),
          "financeur_FRANCE":
               """select t.ID,v.LIBELLE ,
          ROUND((SUM(CASE WHEN v.ANNEE  = '{}' THEN v.valeur ELSE 0 END)/1000000.00),2) AS 'Réalisé année {} en National' 
          from finance v, titre_financeur t
          where v.LIBELLE =t.LIBELLE 
          group by t.ID ,v.LIBELLE 
          order by t.ID;
          """.format(annee,annee),
          "destination_REGION":
               """select t.ID,v.LIBELLE ,
          ROUND((SUM(CASE WHEN v.ANNEE  = '{}' THEN v.valeur ELSE 0 END)/1000000.00),2) AS 'Réalisé année {}' 
          from finance v, titre_financeur t
          where v.LIBELLE =t.LIBELLE and v.COD_REGION ='PARAM_REGION'
          group by t.ID ,v.LIBELLE 
          order by t.ID;
          """.format(annee,annee)}
     

   
     return query_list
