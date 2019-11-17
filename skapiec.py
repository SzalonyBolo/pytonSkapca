#!/usr/bin/env python3
import urllib
import urllib.request
import sys
from pathlib import Path
from bs4 import BeautifulSoup

def getPage(address):
  html = urllib.request.urlopen(address).read()
  return html

class PPL:
  title = "Planeswalker"
  def createLink(self, card):
    leftURL = "http://planeswalker.pl/szukaj?controller=search&orderby=position&orderway=desc&search_query="
    rightURL = "&submit_search="
    return createLink(card, leftURL, rightURL)

  def parsePage(self, page):
    soup = BeautifulSoup(page, features="html.parser")
    containers = soup.find_all("div", class_="product-container")
    result = []
    for container in containers:
      price = container.find("span", class_="product-price")
      quantityGrid = container.find("span", class_="qty_grid")
      if (quantityGrid is None):
        continue
      quantity = quantityGrid.text[1:]
      if quantity.endswith("+"):
        quantity = quantity[:-1]
      if int(quantity) > 0:
        result.append(price.text)
      else:
        result.append("BRAK")
    if len(result) == 0:
      result.append("BRAK")
    return result

class FG:
  title = "Flamberg"
  def createLink(self, card):
    leftURL = "https://www.flamberg.com.pl/advanced_search_result.php?keywords="
    return createLink(card, leftURL, "")

  def parsePage(self, page):
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
          result.append(price[:-2])
        else:
          result.append("BRAK")
    return result

def createLink(card, leftURL, rightURL):
  return leftURL + urllib.parse.quote(str(card)) + rightURL

class EngineManager:
  engines=[]

  def __init__(self):
    self.engines.append(FG())
    self.engines.append(PPL())

  def searchAllEngines(self, card):
    searchResult = []
    for engine in self.engines:
      link = engine.createLink(card)
      page = getPage(link)
      result = engine.parsePage(page)
      minPrice = min(result)
      searchResult.append(minPrice)
    return searchResult

  def displayTableHeader(self):
    #print("\t", end='')
    for engine in self.engines:
      print("\t" + engine.title, end="")
    print("")

def main():
  argLen = len(sys.argv)
  if argLen < 2:
    print('You should pass card name or file with card list in first argument')
    sys.exit()

  eng = EngineManager()
  my_file = Path(sys.argv[1])
  if my_file.is_file():
    f = open(str(my_file), "r")
    lines = f.readlines()
    eng.displayTableHeader()
    for line in lines:
        cardResult = eng.searchAllEngines(line)
        print(line, end="")
        lenthMap = map(len, cardResult)
        lenthMap = list(lenthMap)
        maxLen = max(lenthMap) - 1
        print("\t", end="")
        for i in range(0, len(cardResult) - 1):
          print("\t" + cardResult[i],end="")
          # for j in range(0, len(cardResult[i]) - 1):
          #   if j <= len(cardResult[i]) - 1:
          #     print("\t" + str(cardResult[i][j]), end="")
          #   else:
          #     print("\t ", end="")

          print("")
        print("")
    f.close()
  else:
    print("Can't open " + my_file)

if __name__ == "__main__":
  main()