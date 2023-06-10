# -*- coding: utf-8 -*-


import bs4 as bs
import requests
import pandas as pd


# Llamada a la página web. Se traen las tablas, cada una contine datos de 1 libro
# Dos columnas, la de la izquierda con el nombre de los datos (categorías), la derecha con los datos
# Cada fila es una lista con dos elementos ([0] categorías; [1] datos). 28 filas por tabla

data = []


for i in range(1, 400):
    url = 'http://catalogo.bibliotecas.gob.ar/pergamo/opac/cgi-bin/pgopac.cgi?VDOC=1.' + \
        str(i) + '#Ejemplares'
    resp = requests.get(url)

    resp = resp.text
    soup = bs.BeautifulSoup(resp, 'html.parser')
    table = soup.find('table', class_='wsTableGrid', id='tbGeneral')

    if table is None:
        continue
    for row in (table.find_all('tr')):
        data.append(row.find_all('td'))

len(data)

# Creamos un diccionario para agrupar los datos según el nombre de cada uno. Y luego pasamos los datos agrupados a listas
# Resulta una lista (result) de 28 listas (cada una contiene los datos de las categorías de las tablas)
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

# De las 399 iteraciones, quedan 299 puesto que en medio había listas vacías
len(result[4])

# Se crea una función para pasar los elementos de las listas de 'td' HTML a text


def pass_to_text(list_):
    text_list = []
    for tag in list_:
        text_list.append(tag.get_text())

    return (text_list)


# Se llama a la función para iterar sobre las listas con los datos que nos interesan
isbn = pass_to_text(result[0])
tipo_texto = pass_to_text(result[1])
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

# Se crea un DataFrame con pandas
df = pd.DataFrame(list(zip(isbn, tipo_texto, titulo, autor, editorial, fecha_edicion, lugar_edicion, materia, fecha_alta)),
                  columns=['ISBN', 'Tipo_Texto', 'Título', 'Autor', 'Editorial', 'Fecha_Edición', 'Lugar_Edición', 'Materia', 'Fecha_Alta'])
df = df.reset_index(drop=True)
df

len(df)

# Se exportan los datos a archivos csv y xlsx

df.to_csv('D:\codoacodo 14\library_scraping\library_catalog.csv', index=True)

df.to_excel(
    "D:\codoacodo 14\library_scraping\library_catalog.xlsx", index=False)
