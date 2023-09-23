import datetime
from flask import Flask,jsonify, Response, request
from flask_cors import CORS, cross_origin
import re
import urllib.request
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET
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

def scraping(search_date=None, search_lotery=None):
	data = []
	loteries_parser = []
  # Cargar JSON en un Archivo
	with open('lottery.json', 'r', encoding='utf-8') as file:
		json_data = file.read()
		data = json.loads(json_data)

	if search_lotery:
		data = [item for item in data if  search_lotery.lower() in item["name"].lower()]
	
	if len(data) == 0:
		return data

	# Load HTML 
	games_blocks = load_html(search_date)

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

def scrapingByName(search_name,search_date=None, search_lotery=None):
	data = []
	loteries_parser = []
  # Cargar JSON en un Archivo
	with open('lottery.json', 'r', encoding='utf-8') as file:
		json_data = file.read()
		data = json.loads(json_data)

	
	if search_lotery:
		data = [item for item in data if  search_lotery.lower() in item["name"].lower()]
	
	if len(data) == 0:
		return data

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

def JsonUFT8(data=None):
	json_string = json.dumps(data,ensure_ascii = False)
	return Response(json_string, content_type='application/json; charset=utf-8')

app = Flask(__name__)
CORS(app)
port = int(os.environ.get("PORT", 5000))

@app.route("/", methods=['GET'])
def search_lotery():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	data = scraping(search_date)
	return JsonUFT8(data)
	 
@app.route("/search", methods=['GET'])
def search_lotery_by_name():
	search_query = request.args.get('name', None)
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))

	if not search_query:
		return jsonify({"error": "Missing 'name' parameter"}), 400
	
	data =  scraping(search_date, search_query) 
	return JsonUFT8(data)

@app.route("/loteria-gana-mas", methods=['GET'])
def search_lotery1():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))

	data = scrapingByName("loteria-nacional/gana-mas",search_date,"Gana Más")
	return JsonUFT8(data)


@app.route("/loteria-primera", methods=['GET'])
def search_lotery2():
	search_query = request.args.get('name', "primera")
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("la-primera",search_date, search_query) 
	return JsonUFT8(data)

@app.route("/loteria-primera-12am", methods=['GET'])
def search_lotery3():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("la-primera/quiniela-medio-dia",search_date, "la primera Día")
	return JsonUFT8(data)


@app.route("/loteria-primera-noche", methods=['GET'])
def search_lotery4():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("la-primera/quiniela-noche",search_date, "Primera Noche")
	return JsonUFT8(data)

@app.route("/loteria-la-suerte", methods=['GET'])
def search_lotery6():
	search_query = request.args.get('name', "La Suerte")
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("la-suerte-dominicana",search_date, search_query)
	return JsonUFT8(data)


@app.route("/loteria-la-suerte-12am", methods=['GET'])
def search_lotery7():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("la-suerte-dominicana/quiniela",search_date, "La Suerte 12:30")
	return JsonUFT8(data)

@app.route("/loteria-la-suerte-tarde", methods=['GET'])
def search_lotery8():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("la-suerte-dominicana/quiniela-tarde",search_date, "La Suerte 18:00")
	return JsonUFT8(data)


@app.route("/loteria-lotedom", methods=['GET'])
def search_lotery9():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("lotedom",search_date, "Quiniela LoteDom")
	return JsonUFT8(data)


@app.route("/loteria-anguila", methods=['GET'])
def search_lotery10():
	search_query = request.args.get('name', "Anguila")
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("anguila",search_date, search_query)
	return JsonUFT8(data)

@app.route("/loteria-anguila-10am", methods=['GET'])
def search_loteryAng():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("anguila/anguila-manana",search_date, "Anguila Mañana")
	return JsonUFT8(data)

@app.route("/loteria-anguila-12am", methods=['GET'])
def search_loteryAng12():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("anguila/anguila-medio-dia",search_date, "Anguila Medio Día")
	return JsonUFT8(data)

@app.route("/loteria-anguila-6pm", methods=['GET'])
def search_loteryAng6pm():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("anguila/anguila-tarde",search_date, "Anguila Tarde")
	return JsonUFT8(data)

@app.route("/loteria-anguila-9pm", methods=['GET'])
def search_loteryAng9pm():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("anguila/anguila-noche",search_date, "Anguila Noche")
	return JsonUFT8(data)

@app.route("/loterias-nacionales", methods=['GET'])
def search_lotery11():
	search_query = request.args.get('name', None)
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("loteria-nacional",search_date, search_query)	
	return JsonUFT8(data)

@app.route("/loteria-nacional", methods=['GET'])
def search_lotery12():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("loteria-nacional/quiniela",search_date, "Lotería Nacional")
	return JsonUFT8(data)


@app.route("/loteria-leidsa", methods=['GET'])
def search_lotery13():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("leidsa", search_date, "Quiniela Leidsa")
	return JsonUFT8(data)

@app.route("/loteria-real", methods=['GET'])
def search_lotery14():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("loto-real", search_date, "Quiniela Real")
	return JsonUFT8(data)


@app.route("/loteria-loteka", methods=['GET'])
def search_lotery15():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("loteka", search_date, "Quiniela Loteka")
	return JsonUFT8(data)


@app.route("/loteria-americana", methods=['GET'])
def search_lotery16():
	search_query = request.args.get('name', None)
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("americanas",search_date, search_query)
	return JsonUFT8(data)

@app.route("/loteria-florida-tarde", methods=['GET'])
def search_lotery17():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("americanas/florida-tarde",search_date, "Florida Día")
	return JsonUFT8(data)

@app.route("/loteria-florida-noche", methods=['GET'])
def search_lotery18():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("americanas/florida-noche",search_date, "Florida Noche")
	return JsonUFT8(data)	

@app.route("/loteria-new-york-12am", methods=['GET'])
def search_lotery19():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("americanas/new-york-medio-dia",search_date, "New York Tarde")
	return JsonUFT8(data)

@app.route("/loteria-new-york-noche", methods=['GET']) 
def search_lotery20():
	search_date = request.args.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
	
	data = scrapingByName("americanas/new-york-noche",search_date, "New York Noche")
	return JsonUFT8(data)

app.run(port=port)