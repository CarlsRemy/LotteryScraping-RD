from flask import Flask,jsonify
from flask_cors import CORS, cross_origin
import re
import urllib.request
from bs4 import BeautifulSoup
import os
import json


def load_html():
	url1 = "https://loteriasdominicanas.com/"
	# esta Segunda Url es porque en la Pag. principal no aparecen las Loterias Anguila
	url2 = "https://loteriasdominicanas.com/anguila" 
        
	# Crea una lista para almacenar los elementos de ambos soups
	games_blocks = []

	try:
		html1 = urllib.request.urlopen(url1).read()
		html2 = urllib.request.urlopen(url2).read()
                
		soup1 = BeautifulSoup(html1, "html.parser")
		soup2 = BeautifulSoup(html2, "html.parser")
                
		# Encuentra los elementos deseados del soup y agrégalos a la lista
		blocks1 = soup1.find_all("div", class_="game-block")
		games_blocks.extend(blocks1)

		# Encuentra los elementos del soup y agrégalos a la lista
		blocks2 = soup2.find_all("div", class_="game-block")
		games_blocks.extend(blocks2)
	except:
		return []

	return games_blocks


def scraping():
	data = []
	loteries_parser = []
  # Cargar JSON en un Archivo
	with open('lottery.json') as file:
		json_data = file.read()
		data = json.loads(json_data)

	# Load HTML 
	games_blocks = load_html()

	for game_block in games_blocks:
		block = {}
		title = game_block.find("a", "game-title").getText().strip().lower()

		filtered_data = [item for item in data if item["name"].lower() == title]
		if len(filtered_data) == 0:
			continue  

		pather_score = game_block.find_all("span", "score")
		pather_date = game_block.find("div", "session-date").getText().strip()
		score = "-".join(span.text.strip() for span in pather_score)

		block['id'] = filtered_data[0]["id"]
		block['name'] = filtered_data[0]["name"]
		block['date'] = pather_date
		block['number'] = score
		loteries_parser.append(block)

	return sorted(loteries_parser, key=lambda k:k["id"])


app = Flask(__name__)
CORS(app)
port = int(os.environ.get("PORT", 5000))
@app.route("/")
def search_lotery():
  return jsonify(scraping())

app.run(port=port)