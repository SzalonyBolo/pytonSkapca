#!/usr/bin/env python3
import urllib
import urllib.request
import sys
import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup
from tabulate import tabulate

class webscrapper:
  def getPage(self, address):
    html = urllib.request.urlopen(address).read()
    return html

class PPL(webscrapper):
  title = "Planeswalker"
  def createLink(self, card):
    leftURL = "http://planeswalker.pl/szukaj?controller=search&orderby=price&orderway=asc&search_query="
    rightURL = "&submit_search="
    return createLink(card, leftURL, rightURL)

  def parsePage(self, page, card):
    soup = BeautifulSoup(page, features="html.parser")
    containers = soup.find_all("div", class_="product-container")
    result = []
    for container in containers:
      price = container.find("span", class_="product-price")
      quantityGrid = container.find("span", class_="qty_grid")
      name = container.find("a", class_="product-name")
      if (quantityGrid is None):
        continue
      quantity = quantityGrid.text[1:]
      if quantity.endswith("+"):
        quantity = quantity[:-1]
      if int(quantity) > 0 and card.lower() in name.text.strip().lower():
        result.append(price.text.strip())
      else:
        result.append("BRAK")
    if len(result) == 0:
      result.append("BRAK")
    return result

class FG(webscrapper):
  title = "Flamberg"
  def createLink(self, card):
    leftURL = "https://www.flamberg.com.pl/advanced_search_result.php?keywords="
    return createLink(card, leftURL, "")

  def parsePage(self, page, card):
    soup = BeautifulSoup(page, features="html.parser")
    tables = soup.find_all('table')
    if len(tables) == 1:
      return ["BRAK"]
    table = tables[1]
    trs = table.find_all('tr')
    result = []
    for tr in trs:
      tds = tr.find_all('td')
      if len(tds) > 5:
        price = tds[3].text
        quantity = tds[4].text
        if int(quantity) > 0:
          result.append(price[:-2].strip())
        else:
          result.append("BRAK")
    return result

class Alledrogo:
  title = "Allegro"
  kurwasikret = "M2QwYzhlODRiNzA4NGYxNDkzOWFmNDlhYWRkNmU2YzE6dVN0WGJpY3RNSkFvMFFuVFBFUTl4b1htUUcwZ1dBQUl1aGdPVzNLbTZUMzJ1UExQRGduQmVxSmFMVFdtWE9yMA=="
  token = ""
  actualCard = ""

  def __init__(self):
    r = requests.post("https://allegro.pl/auth/oauth/token?grant_type=client_credentials", headers={"Authorization": "Basic " + self.kurwasikret})
    c = json.loads(r.text)
    self.token = c.get('access_token')

  def createLink(self, card):
      leftURL = "https://api.allegro.pl/offers/listing?phrase="
      rightURL = "&category.id=6066"
      self.actualCard = card
      return createLink(card, leftURL, rightURL)

  def parsePage(self, page, card):
    card = card
    j = json.loads(page)
    items = j.get("items")
    regular = items.get("regular")
    result = []
    for item in regular:
      if card in item["name"]:
        result.append(item["sellingMode"]["price"]["amount"].strip())
    if len(result) == 0:
      result.append("BRAK")
    return result

  def getPage(self, address):
    r = requests.get(address, headers={'Authorization' : "Bearer " + self.token, 'Accept' : "application/vnd.allegro.public.v1+json"})
    return r.text
      

def createLink(card, leftURL, rightURL):
  return leftURL + urllib.parse.quote(str(card)) + rightURL

class EngineManager:
  engines=[]

  def __init__(self):
    self.engines.append(FG())
    self.engines.append(PPL())
    self.engines.append(Alledrogo())

  def searchAllEngines(self, card):
    searchResult = []
    searchResult.append(card)
    for engine in self.engines:
      link = engine.createLink(card)
      page = engine.getPage(link)
      result = engine.parsePage(page, card)
      minPrice = min(result)
      searchResult.append(minPrice)
    return searchResult

  def displyResults(self, results):
    titleRow = []
    titleRow.append("Card")
    for engine in self.engines:
      titleRow.append(engine.title)
    results.insert(0, titleRow)
    print(tabulate(results, headers="firstrow"))

def main():
  argLen = len(sys.argv)
  if argLen < 2:
    print('You should pass file with card list in first argument')
    sys.exit()

  eng = EngineManager()
  cardsResult = []
  my_file = Path(sys.argv[1])
  if my_file.is_file():
    f = open(str(my_file), "r")
    lines = f.readlines()
    for line in lines:
      cardsResult.append(eng.searchAllEngines(line.strip()))
    f.close()
  eng.displyResults(cardsResult)
    

if __name__ == "__main__":
  main()