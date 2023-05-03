# Etats_financier

Automatisation du calcul des états-financier annuels des ARS.

## Architecture

_Documentation
|__ _Data
    |__ _00_transformation_python
    |__ _01_data_source
    |__ _02_table_dim
    |__ _03_table_fait
|__ _Spécifications
_ETL
|__ _Utilitaire
    |__ _main.py
    |__ _data_test
        |__ _commune2022.csv
    |__ _modules
        |__ _decrypt
            |__ ___init__.py
            |__ _decrypt.py
        |__ _route_postgre
            |__ ___init__.py
            |__ _route_postgre.py        
        |__ _transform
            |__ ___init__.py
            |__ _transform.py
            |__ _transform_sqlquery.py
    |__ _settings
    |__ _utils
_Librairies
_Python
_python_venv
_VSCode
_README.md
_.gitignore
