# -*- coding: utf-8 -*-

import bs4 as bs
import requests
import pandas as pd

#Llamada a la página web. Se traen las tablas, cada una contine datos de 1 libro
#Dos columnas, la de la izquierda con el nombre de los datos (categorías), la derecha con los datos
#Cada fila es una lista con dos elementos ([0] categorías; [1] datos). 28 filas por tabla

data = []


for i in range(1,400):
    url = 'http://catalogo.bibliotecas.gob.ar/pergamo/opac/cgi-bin/pgopac.cgi?VDOC=1.'+str(i) + '#Ejemplares'
    resp = requests.get(url)

    resp = resp.text
    soup = bs.BeautifulSoup(resp, 'html.parser')
    table = soup.find('table', class_='wsTableGrid', id='tbGeneral')

    if table is None:
        continue
    for row in (table.find_all('tr')):
        data.append(row.find_all('td'))

len(data)

#Creamos un diccionario para agrupar los datos según el nombre de cada uno. Y luego pasamos los datos agrupados a listas
#Resulta una lista (result) de 28 listas (cada una contiene los datos de las categorías de las tablas)
d = {}
for subl in data:
    try:
        if subl[0] in d:
            d[subl[0]].append(subl[1])
        else:
            d[subl[0]] = [subl[1]]
    except IndexError:
        continue
result = list(d.values())

len(d)

len(data)

len(result)

#De las 399 iteraciones, quedan 299 puesto que en medio había listas vacías
len(result[4])

#Se crea una función para pasar los elementos de las listas de 'td' HTML a text
def pass_to_text(list_):
    text_list = []
    for tag in list_:
        text_list.append(tag.get_text())

    return(text_list)

#Se llama a la función para iterar sobre las listas con los datos que nos interesan
isbn = pass_to_text(result[0])
tipo_texto=pass_to_text(result[1])
titulo = pass_to_text(result[4])
autor = pass_to_text(result[7])
editorial = pass_to_text(result[10])
fecha_edicion = pass_to_text(result[11])
lugar_edicion = pass_to_text(result[13])
materia_0 = pass_to_text(result[26])
fecha_alta = pass_to_text(result[27])

# Limpiamos los strings de la lista materia_0 para que sólo quede el nombre de la materia
# sin perden elementos vacios

materia = []
for elem in materia_0:
    if elem:
        new_elem = ''.join(caracter
                           for caracter in elem
                           if caracter.isalpha() or
                           caracter.isspace() or
                           caracter == '-')
        materia.append(new_elem)
    else:
        materia.append(elem)

#Se crea un DataFrame con pandas
df = pd.DataFrame(list(zip(isbn,tipo_texto, titulo, autor, editorial, fecha_edicion, lugar_edicion, materia,fecha_alta)),
                  columns=['ISBN','Tipo_Texto', 'Título', 'Autor','Editorial','Fecha_Edición','Lugar_Edición','Materia','Fecha_Alta'])
df = df.reset_index(drop=True)
df

len(df)

#Se exportan los datos a archivos csv y xlsx

df.to_csv('library_catalog.csv', index=False)

df.to_excel("library_catalog.xlsx", index=False)

# Creamos diccionarios para unificar datos repetidos y agregar id sobre las columnas que nos interesan
autores = {autor: i for i, autor in enumerate(df['Autor'].unique(), start=1)}
editoriales = {editorial: i for i,
               editorial in enumerate(df['Editorial'].unique(), start=1)}
materias = {materia: i for i, materia in enumerate(df['Materia'].unique(), start=1)}


# Copiamos los datos de la tabla original y mapeamos los datos de las columnas que nos interesan por su id
df2 = df.copy()
df2['Autor'] = df2['Autor'].map(autores)
df2['Editorial'] = df2['Editorial'].map(editoriales)
df2['Materia'] = df2['Materia'].map(materias)
df2


# Creamos nuevas tablas con id
autores_df = pd.DataFrame(list(autores.items()), columns=['Autor', 'ID'])
editoriales_df = pd.DataFrame(
    list(editoriales.items()), columns=['Editorial', 'ID'])
materias_df = pd.DataFrame(list(materias.items()), columns=['Materia', 'ID'])


# Se exportan los datos a archivos csv y xlsx

autores_df.to_csv('author_table.csv', index=False)

autores_df.to_excel("author_table.xlsx", index=False)


editoriales_df.to_csv('editorials_table.csv', index=False)

editoriales_df.to_excel("editorials_table.xlsx", index=False)


materias_df.to_csv('subjects_table.csv', index=False)

materias_df.to_excel("subjects_table.xlsx", index=False)
