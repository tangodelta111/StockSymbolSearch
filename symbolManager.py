import sqlite3 as lite
import json
import sys
import requests


dataURL = "http://oatsreportable.finra.org/OATSReportableSecurities-SOD.txt"

r = requests.get(dataURL)

datalist = [tuple(str(s.strip()).split('|')) for s in r.text.splitlines()]

datalist.pop(0)
datalist.pop()

con = lite.connect("symbols.db")

with con:
	cur = con.cursor()
	cur.executemany("INSERT OR IGNORE INTO Companies VALUES(?, ?, ?)", datalist)

con.close()