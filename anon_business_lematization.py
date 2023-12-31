# -*- coding: utf-8 -*-
""" from Anonymous_Business lemmatization.ipynb """
""" Jorge Zamora """

""" Dependencias y librerías """

#instalamos e importamos lo necesario:
!pip install spacy
!python -m spacy download "es_dep_news_trf"

import pandas as pd
import spacy
#cargamos el modelo para el español de spacy
nlp=spacy.load("es_dep_news_trf")

""" Preprocesamiento """

#leemos el archivo csv con pandas
anon=pd.read_csv("/content/AnonBusiness_Tier5.csv", encoding="latin1", sep=";")
print(anon)

#convertimos la columna que nos interesa lematizar en una lista
lista1=list(anon["columna1"])
#comprobamos el número de celdas o elementos que tendría la lista para asegurarnos de que el producto final se corresponde con lo inicial, y para hacer el slicing
len(lista1)

#dividimos la lista en fragmentos para poder procesarlos más rápido, en este caso los números indicados son la repartición que hice del len() anterior
#sustituir los números y añadir tantas listas como sean necesarias según la longitud de la lista anterior
a1=lista1[:19902]
a2=lista1[19902:39805]
a3=lista1[39805:59707]
a4=lista1[59707:79609]
a5=lista1[79609:]

""" Lematización """

#creamos dos listas vacías que contendrán en las flexionadas la lista inicial, y en las lematizadas el lema de estas, pero en este caso
#solo lematizaremos verbos y toda palabra singular, ya que las que son plurales en ocasiones pueden cambiar el significado o derivar a
#una etiqueta u otra del modelo de ML que estamos entrenando
flex=[]
lem=[]

#por cada elemento en la lista, esto es, el contenido de lo que sería una celda en el archivo .csv inicial
for x in a5: #iremos cambiando a5 al nombre de cada una de las slice en las que se ha dividido la lista inicial, lematizando así cada una
  #etiquetamos ese elemento, que vendría a ser algo parecido a una oración
  l2=nlp(x)
  #creamos dos str vacías que iremos llenando con las palabras (flex2) y lemas (lem2) que vayamos encontrando en el elemento
  #básicamente es como reescribir cada elemento para luego añadirlo a las listas anteriores
  flex2=""
  lem2=""

  #por cada token en el elemento/oración etiquetado, vamos a buscar los verbos y palabras singulares con variación de género gramatical
  for y in l2:
    if y.pos_=="VERB" or y.pos_=="AUX": #si es verbo y tiene forma infinitiva vamos a conservar su forma original, no es necesario el lema
      if y.morph.get("VerbForm")=="Inf":
        flex2=f"{flex2}{y.text} "
        lem2=f"{lem2}{y.text} "
      else:
        flex2=f"{flex2}{y.text} " #en caso diferente, obtenemos el lema y lo guardamos en la variable ya mencionada, lem2
        lem2=f"{lem2}{y.lemma_} "
    elif y.pos_=="NOUN" or y.pos_=="DET" or y.pos_=="ADJ": #si es una palabra que puede variar en gén. gram. y es singular, guardamos su lema
      if y.morph.get("Number")=="Sing":
        flex2=f"{flex2}{y.text} "
        lem2=f"{lem2}{y.lemma_} "
      else: #en caso diferente, conservamos su forma original
        flex2=f"{flex2}{y.text} "
        lem2=f"{lem2}{y.text} "
    else: #si es un adverbio, preposición u otro tipo de unidad léxica, conservamos su forma original
      flex2=f"{flex2}{y.text} "
      lem2=f"{lem2}{y.text} "
  #finalmente añadimos el elemento reescrito con sus lemas a las listas iniciales
  flex.append(flex2)
  lem.append(lem2)
#creamos un dataframe con las listas creadas con la forma original y la forma lematizada y lo imprimimos para comprobar el resultado de la lematización
lemma1=pd.DataFrame({"Flexionadas":flex, "Lemas":lem}, index=None, columns=["Flexionadas", "Lemas"])
print(lemma1)
#Convertimos en csv el archivo que acabamos de lematizar en cuestión
lemma1.to_csv("Tier5_AnonBusiness_lemas99.csv", encoding="latin1", sep=";")

""" Unión de archivos csv """

#Leemos con pandas cada uno de los archivos obtenidos de la lematización
a = pd.read_csv("Tier5_AnonBusiness_lemas19.csv", encoding="latin1", sep=";")
b = pd.read_csv("Tier5_AnonBusiness_lemas39.csv", encoding="latin1", sep=";")
c = pd.read_csv("Tier5_AnonBusiness_lemas59.csv", encoding="latin1", sep=";")
d = pd.read_csv("Tier5_AnonBusiness_lemas79.csv", encoding="latin1", sep=";")
e = pd.read_csv("Tier5_AnonBusiness_lemas99.csv", encoding="latin1", sep=";")

#los unimos con pandas, quitamos posibles espacios en blanco que dejase la unión e imprimimos para comprobar el resultado
ab1=pd.concat([a,b,c,d,e])
ab1.columns.str.strip()
print(ab1)

#convertimos el archivo unido a csv
ab1.to_csv("AB_lemas_def.csv", encoding="latin1", sep=";")
