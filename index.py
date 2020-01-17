# Web Scrapping

import os
import re
import csv
import pickle
import requests
from bs4 import BeautifulSoup


link = "http://localhost:8000/index.html"


def data_extract(cb):
    str_name = cb.find('span', class_='car_name').text

    str_cylinders = cb.find('span', class_='cylinders').text

    cylinders = int(str_cylinders)
    assert cylinders > 0, f"Waiting cylinders are positive and not {cylinders}"

    str_weight = cb.find('span', class_='weight').text

    weight = int(str_weight.replace(',', ''))
    assert weight > 0, f"Waiting that weight are positive and not {weight}"

    acceleration = float(cb.find('span', class_='acceleration').text)
    assert acceleration > 0, f"Waiting acceleration to be positive"

    line = dict(name=str_name, cylinders=cylinders,
                weight=weight, acceleration=acceleration)

    return line


def proccess_car_blocks(soup):
    car_blocks = soup.find_all('div', class_='car_block')

    lines = []

    for cb in car_blocks:
        line = data_extract(cb)
        lines.append(line)

    print("\nFind {} lines".format(len(lines)))

    print("\nFirst Line: \n{}".format(lines[0]))
    print("\nLast Line: \n{}".format(lines[-1]))

    print("\n")

    with open("dados_copiados_v1.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=line.keys())
        writer.writeheader()
        writer.writerows(lines)


if __name__ == "__main__":
    file = 'dados_copiados_v1.pickle'

if os.path.exists(file):
    with open(file, 'rb') as f:
        print("\nLoading cache from file {}".format(file))
        res = pickle.load(f)
else:
    print("\nCopying data from page {}".format(link))
    res = requests.get(link)
    with open(file, 'wb') as f:
        print("\nGravando o cache em {}".format(file))
        pickle.dump(res, f)

assert res.status_code == 200, f"Status: {res.status_code}, check your connetion!"

web_text = res.text

soup = BeautifulSoup(web_text, "html.parser")

proccess_car_blocks(soup)
