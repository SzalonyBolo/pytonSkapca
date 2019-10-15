#!/usr/bin/env python3
import urllib
import sys
from pathlib import Path
from bs4 import BeautifulSoup`

def getPage(address):
  html = urllib.request.urlopen(address).read()
  return html

def PPL:
  def createLink(card):
    leftURL = "http://planeswalker.pl/szukaj?controller=search&orderby=position&orderway=desc&search_query="
    rightURL = "&submit_search="
    return createLink(card, leftURL, rightURL)

  def parsePage(page):
		soup = BeautifulSoup(page)
  	containers = soup.find_all("div", class_="product-container")
    result = []
    for container in containers:
      price = container.find("span", class_="product-price")
			quantityGrid = container.find("span", class="qty_grid")
			quantity = quantityGrid.text[1:]
		  if quantity.endswith("+")
			
      if (quantity[:]

def FG:
  def createLink(card):
    leftURL = ""
    cardURL = urllib.parse.urlencode(card)
    rightURL = ""
    return createLink(card, leftURL, rightURL)
  
  def parsePage(page):
		soup = BeautifulSoup(page)
		tables = soup.find_all('table')
		table = tables[1]
    tds = table.find_all('td')
    result = []
    for td in tds:
       if td.text.endswith('zl')
         result.append(td.text[:-2])
    return result


def createLink(card, leftURL, rightURL):
  return leftURL + urllib.parse.urlencode(card) + rightURL

def parsePage(page):
  result = []
  soup = BeautifulSoup(page)
  soup.find_all('')

def searchAllEngines(card):
  engines = []
	engines.append(PPL())
	engines.append(FG))

  for engine in engines:
    link = engine.create(card)
		page = getPage(link)
    result = parsePage(page)

def main():
  argLen = len(sys.argv)
  if argLen == 0 or argLen > 1:
    print('You should pass card name or file with card list in first argument')
    sys.exit()
  
	my_file = Path(sys.argv[0])
  if my_file.is_file():
    with open(...) as f:
      for line in f:
	      searchAllEngines()

if __name__ == "__main__":
  main()
