import pandas as pd


class DataCollection:

    def __init__(self):
        pass

    def get_symbol(self):
        symbol1 = pd.read_csv("input/companylist1.csv")
        symbol2 = pd.read_csv("input/companylist2.csv")
        print list(symbol1), list(symbol2)


DataCollection().get_symbol()