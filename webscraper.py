#!/usr/bin/env python3
import urllib
import sys
from pathlib import Path
from bs4 import BeautifulSoup

def getPage(address):
  html = urllib.request.urlopen(address).read()
  return html

def createPLLink(card):
  leftURL = "http://planeswalker.pl/szukaj?controller=search&orderby=position&orderway=desc&search_query="
  rightURL = "&submit_search="
  return createLink(card, leftURL, rightURL)

def createFGLink(card):
  leftURL = ""
  cardURL = urllib.parse.urlencode(card)
  rightURL = ""
  return createLink(card, leftURL, rightURL)

def createLink(card, leftURL, rightURL):
  return leftURL + urllib.parse.urlencode(card) + rightURL

def parsePage(page):
  result = []
  soup = BeautifulSoup(page)
  soup.find_all('')

def searchAllEngines(card):
  

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
