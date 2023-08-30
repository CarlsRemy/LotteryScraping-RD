import datetime
from flask import Flask,jsonify
from flask_cors import CORS, cross_origin
import re
import urllib.request
from bs4 import BeautifulSoup
import os
import json


def load_html(search_date=None):

	url1 = "https://loteriasdominicanas.com/"
	# esta Segunda Url es porque en la Pag. principal no aparecen las Loterias Anguila
	url2 = "https://loteriasdominicanas.com/anguila" 

	# Agregar el parámetro date a la URL si existe
	if search_date:
		url1 += f"?date={search_date}"
		url2 += f"?date={search_date}"
        
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


def load_html_name(search_name,search_date=None):
	url1 = f"https://loteriasdominicanas.com/{search_name}"

	# Agregar el parámetro date a la URL si existe
	if search_date:
		url1 += f"?date={search_date}"
        
	# Crea una lista para almacenar los elementos de ambos soups
	games_blocks = []

	try:
		html1 = urllib.request.urlopen(url1).read()      
		soup1 = BeautifulSoup(html1, "html.parser")
                
		# Encuentra los elementos deseados del soup y agrégalos a la lista
		blocks1 = soup1.find_all("div", class_="game-block")
		games_blocks.extend(blocks1)
	except:
		return []

	return games_blocks

def scraping(search_date=None):
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


def scrapingByName(search_name,search_date=None):
	data = []
	loteries_parser = []
  # Cargar JSON en un Archivo
	with open('lottery.json') as file:
		json_data = file.read()
		data = json.loads(json_data)

	# Load HTML 
	games_blocks = load_html_name(search_name,search_date)

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


@app.route("/search")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	if not search_query:
		return jsonify({"error": "Missing 'name' parameter"}), 400
	
	filtered_lotteries = [lottery for lottery in scraping(search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries




@app.route("/loteria-gana-mas")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("loteria-nacional/gana-mas",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries



@app.route("/loteria-primera")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("la-primera",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries

@app.route("/loteria-primera-12am")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("la-primera/quiniela-medio-dia",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


@app.route("/loteria-primera-noche")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("la-primera/quiniela-noche",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


@app.route("/loteria-nueva-york")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("nueva-york",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries

@app.route("/loteria-la-suerte")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("la-suerte-dominicana",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


@app.route("/loteria-la-suerte-12am")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("la-suerte-dominicana/quiniela",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries

@app.route("/loteria-la-suerte-tarde")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("la-suerte-dominicana/quiniela-tarde",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


@app.route("/loteria-lotedom")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("lotedom",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


@app.route("/loteria-anguila")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("anguila",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


@app.route("/loteria-nacional")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("loteria-nacional",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries

@app.route("/loteria-quiniela-nacional")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("loteria-nacional/quiniela",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


@app.route("/loteria-gana-mas")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("loteria-nacional/gana-mas",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


@app.route("/loteria-leidsa")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("leidsa", search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries

    
@app.route("/loteria-real")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("loto-real", search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


@app.route("/loteria-loteka")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name", '')
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("loteka", search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


@app.route("/loteria-americana")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("americanas",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


@app.route("/loteria-florida-tarde")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("americanas/florida-tarde",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


@app.route("/loteria-florida-noche")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("americanas/florida-noche",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


@app.route("/loteria-new-york-12am")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("americanas/new-york-medio-dia",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries

@app.route("/loteria-new-york-noche")
def search_lotery_by_name():
	search_query = urllib.request.args.get("name")
	search_date = urllib.request.request.args.get("date", datetime.datetime.now().strftime("%d-%m-%Y"))
	
	filtered_lotteries = [lottery for lottery in scrapingByName("americanas/new-york-noche",search_date) if search_query.lower() in lottery["name"].lower()]
	
	return filtered_lotteries


app.run(port=port)