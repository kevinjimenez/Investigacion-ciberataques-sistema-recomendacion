# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
fileDir = os.path.dirname(os.path.abspath(__file__))
path_datos_raiting = fileDir + '/datos-prueba/u.data'
path_datos_nombre_categoria = fileDir + '/datos-prueba/Movie_Id_Titles.csv'

# leer archivo de ratings por usuario y pelicula
df = pd.read_csv(path_datos_raiting, sep='\t', names=['user_id','item_id','rating','timestamp'])
# listar 10 primeros registros del archivo de ratings
df.head(10)


# leer archivo de titulos de peliculas con su id
titulos_peliculas = pd.read_csv(path_datos_nombre_categoria)
# listar 10 primeros registros del archivo de titulos de peliculas
titulos_peliculas.head(10)


# union de los dataframes de ratings con los titulos de peliculas con su id  
df = pd.merge(df, titulos_peliculas, on='item_id')
df.head(20)

# los raitings agrupados por titulo y calculando 
# la media x su raiting media o promedio de cada pelicula
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings.head(10)

ratings['numero_de_rating'] = df.groupby('title')['rating'].count()
ratings.head()

matriz_pelicula = df.pivot_table(index='user_id', columns='title', values='rating')
matriz_pelicula.head(10)


ratings.sort_values('numero_de_rating', ascending=False).head(10)


print("Ingrese palabra:") 
palabra = input()

print("Palabra Ingresada", palabra)

if palabra != "" :
	try:
		palabra_buscar = palabra.strip()
		user_rating = matriz_pelicula[palabra_buscar]
		user_rating.head()
		similar=matriz_pelicula.corrwith(user_rating)
		similar.head()

		corr = pd.DataFrame(similar, columns=['correlation'])
		corr.dropna(inplace=True)
		corr.head()

		corr = corr.join(ratings['numero_de_rating'],how='left', lsuffix='_left', rsuffix='_right')
		corr.head(10)

		items_similares = corr[corr['numero_de_rating'] > 100].sort_values(by='correlation', ascending=False).head(10)
		print(items_similares)
	except KeyError:
		print("Oops!  La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")
else:
	print("Oops!  La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")


