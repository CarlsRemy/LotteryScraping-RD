# LotteryScraping-RD
LotteryScraping-RD es un proyecto de web scraping diseñado para extraer datos en tiempo real de los resultados de loterías en la República Dominicana. Los datos extraídos incluyen un id, números ganadores, fecha de los sorteos y nombres de las loterías en formato JSON.


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

Dicho **Json** se utiliza para filtrar y seleccionar las distintas loterías de la página web, permitiendo devolver únicamente las loterías específicas que se deseen. Cada entrada en el JSON posee un identificador (ID) que es empleado para establecer un orden dentro de la estructura, y el nombre en el JSON debe coincidir con el nombre de la lotería según se presenta en la página [loteriasdominicanas](https://loteriasdominicanas.com/)
