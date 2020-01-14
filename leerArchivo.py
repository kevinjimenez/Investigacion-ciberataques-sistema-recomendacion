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
path_datos_raiting = fileDir + '/datos-prueba/dataSets.data'
path_datos_nombre_categoria = fileDir + '/datos-prueba/Movie_Id_Titles.csv'

# leer archivo de ratings por usuario y pelicula
df = pd.read_csv(path_datos_raiting, sep='\t', names=['nombre','descripcion','rating','descripcion'])
# listar 10 primeros registros del archivo de ratings
df.head(10)
