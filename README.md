# LotteryScraping-RD Lotería 

Este proyecto es una aplicación de web scraping que extrae información sobre las loterías dominicanas desde el sitio web [Loterías Dominicanas](https://loteriasdominicanas.com/). Proporciona una API para buscar y filtrar información sobre las loterías y sus resultados.

para el funcionamiento de este cargamos un archivo **json** de la siguiente manera:

``` python
	with open('lottery.json') as file:
		json_data = file.read()
		data = json.loads(json_data)
```
Aunque tambien lo pudemos hacer de manera dirrecta:

``` python
	json_data = json_data = '''
	[
		{
			"id": 1,
			"name": "La Primera Día"
		},
		{
			"id": 2,
			"name": "Anguila Mañana"
		},
		# ... otros elementos ...
	]
	'''

	data = json.loads(json_data)
```

Dicho **Json** se utiliza para filtrar y seleccionar las distintas loterías de la página web, permitiendo devolver únicamente las loterías específicas que se deseen. Cada entrada en el JSON posee un identificador (ID) que es empleado para establecer un orden dentro de la estructura, y el nombre en el JSON debe coincidir con el nombre de la lotería según se presenta en la página [Loterías Dominicanas](https://loteriasdominicanas.com/)

## Características

- Obtención de datos de loterías en tiempo real.
- Búsqueda y filtrado por nombre de lotería y fecha.
- Filtar entre consorcio de loterias ej:Nacional, leisa, americana etc

## Requisitos

- Python 3.x
- Bibliotecas: Flask, Flask-CORS, BeautifulSoup4

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/CarlsRemy/LotteryScraping-RD.git
```
