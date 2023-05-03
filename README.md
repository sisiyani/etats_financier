# Etats_financier

Automatisation du calcul des états-financier annuels des ARS.

## Architecture
README.md
.gitignore
etl
|__utilitaire
   |__ main.py
   |__ data
      |__ _database
         |__ demo.db
         |__ etats_financier.db
      |__ input
         |__ CORRESP
            |__ demo.xlsx
         |__ DFAS
         |__ DGOS
         |__ DSS
         |__ FIR
         |__ FMIS
      |__ to_csv
      |__ output
      |__ _modules
         |__ route_sqlite
            |__ __init__.py
            |__ route_sqlite.py
      |__ _settings
         |__ .gitignore
         |__ settings.json
         |__ settings_demo.json
      |__ utils
         |__ __init__.py
         |__ utils.py

