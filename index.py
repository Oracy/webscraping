# Web Scrapping

import os
import re
import csv
import pickle
import requests
from bs4 import BeautifulSoup


link = "http://www.google.com"


if __name__ == "__main__":
    file = 'dados_copiados_v1.pickle'

    if os.path.exists(file):
        with open(file, 'rb') as f:
            print(f"\nLoading cache from file {}".format(file))
            res = pickle.load(f)
    else:
        print(f"\nCopying data from page {}".format(link))
        res = requests.get(link)
        with open(file, 'wb') as f:
            print(f"\nGravando o cache em {}".format(file))
            pickle.dump(res, f)
    
    assert res.status_code == 200, f"Status: {res.status_code}, check your connetion!"

    web_text = res.text

    soup = BeautifulSoup(web_text, "html.parser")

    proccess_