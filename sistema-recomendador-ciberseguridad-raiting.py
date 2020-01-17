import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
fileDir = os.path.dirname(os.path.abspath(__file__))
path_datos_raiting = fileDir + '/datos-prueba/raiting_25.csv'
path_datos_ataques = fileDir + '/datos-prueba/datos_valores_25.csv'


raitings = pd.read_csv(path_datos_raiting, sep=',', names=['user_id','item_id','rating'])
print(raitings.head())

items = pd.read_csv(path_datos_ataques)
print(items.head())


ataques_raitings = pd.merge(raitings, items, on='item_id')
print(ataques_raitings.head())

media_ataques_raitings = pd.DataFrame(ataques_raitings.groupby(['name'])['rating'].mean())
print(media_ataques_raitings.head())


media_ataques_raitings['numero_de_rating'] = ataques_raitings.groupby(['name'])['rating'].count()
print(media_ataques_raitings.head())

matriz_usuario_ataque = ataques_raitings.pivot_table(index='user_id', columns='name', values='rating')
print(matriz_usuario_ataque.head())

print(media_ataques_raitings.sort_values('numero_de_rating', ascending=False).head())


print("Ingrese palabra:") 
palabra = input()
print("+++++++++++++++++++++++++++")
print("Palabra Ingresada ===>", palabra)
print("+++++++++++++++++++++++++++")

if palabra != "" :
	try:
		palabra_buscar = palabra.strip()
		user_rating = matriz_usuario_ataque[palabra_buscar]
		user_rating.head()
		recomendacion_similar=matriz_usuario_ataque.corrwith(user_rating)
		recomendacion_similar.head()

		correlacion_recomendaciones = pd.DataFrame(recomendacion_similar, columns=['correlation'])
		correlacion_recomendaciones.dropna(inplace=True)
		correlacion_recomendaciones.head()

		correlacion_recomendaciones = correlacion_recomendaciones.join(media_ataques_raitings['numero_de_rating'],how='left', lsuffix='_left', rsuffix='_right')
		correlacion_recomendaciones.head()

		recomendaciones = correlacion_recomendaciones[correlacion_recomendaciones['numero_de_rating'] > 2].sort_values(by='correlation', ascending=False).head()
		print("*******************************************")
		print("*******************************************")
		print("-------------------------------------------")
		print("LISTA DE RECOMENDACIONES PARA: ", palabra )
		print("-------------------------------------------")		
		print(recomendaciones)
		print("*******************************************")		
		print("*******************************************")		
		print("*******************************************")		
	except KeyError:
		print("Oops!  La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")
else:
	print("Oops!  La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")


