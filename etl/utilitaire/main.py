# --coding:Latin-1 -


# MODULES
import argparse

from modules import route_sqlite
from utils import utils

# COMMANDES
def __main__(args):
     if args.commande == "init_database":
          init_db()
     return


def init_db():
     print("###############")
     print("### INIT_DB ###")
     print("###############")



