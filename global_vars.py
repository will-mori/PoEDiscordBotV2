# Globals.py
# This file is meant to store values that are constant across all functions and modules of this
#   repository

CURRENCY_DICT = {"c": "Chaos Orb", "ex": "Exalted Orb", "woke": "Awakener's Orb", 
                "esex": "Elevated Sextant","anc": "Ancient Orb", "annul":"Orb of Annulment",
                "deck": "Stacked Deck", "asex": "Awakened Sextant", "od": "Orb of Dominance",
                "oc": "Orb of Conflict", "ec": "Eldritch Chaos Orb", "eex": "Eldritch Exalted Orb", 
                "eoa": "Eldritch Orb of Annulment", "do": "Divine Orb", "unmake": "Orb of Unmaking", 
                "fuse": "Orb of Fusing", "tcat": "Tempering Catalyst", "fcat": "Fertile Catalyst",
                "gcp": "Gemcutter's Prism", "alt": "Orb of Alteration", "alch": "Orb of Alchemy",
                "vaal": "Vaal Orb", "mirror": "Mirror of Kalandra" }
URL = "http://trade.maximumstock.net/trade"




if __name__ == "__main__":
    print("""This module just stores 'immutable' global values.  These could technically be put  
    in dotenv, but this is a slightly more practical solution""")
