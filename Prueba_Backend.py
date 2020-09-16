#!/usr/bin/env python
# coding: utf-8
import requests,json,random, sqlite3
import pandas as pd
from hashlib import sha1
from time import time
from keys import headers

url = "https://restcountries-v1.p.rapidapi.com/all"

def regions_api_rest(url, headers):
    result = requests.request("GET", url, headers=headers).json()

    without_region =[]
    regions = []
    
    for item in result:
     #Bouvet island and Mcdonald Island  >> 'N/A'
    	if item['region']=='':
        	item['region'] = 'N/A'
        	without_region.append(item)

    	if item['region'] not in regions:
        	regions.append(item['region'])
    return regions, without_region


def country_regions(regions, without_region):
    reg =[]
    city = [] 
    lang = []
    time_ejec = []
    
    df = pd.DataFrame(columns=('Region', 'City name', 'Language', 'Time(ms)'), index=None)
    
    if isinstance(regions, list):
        for region in regions:
            if isinstance(region, str):
            
                if region != 'N/A':
                    t_i = time()
                    url = "https://restcountries.eu/rest/v2/region/" + region
                    countries = requests.request("GET", url).json()
                    
                    
                    country_select = random.choice(countries)
                
                    for lang_data in country_select['languages']:
                        language_name = sha1(lang_data['name'].encode('utf-8')).hexdigest()
                    reg.append(region)
                    city.append(country_select['name'])
                    lang.append(language_name) 
                    t_f = time()
                    time_ejec.append(float("%.2f" % ((t_f-t_i)*1000)))
                elif region == 'N/A':
                    t_i2 = time()
                    country_select = random.choice(without_region)
                    #bouvet island >>N/A
                    if country_select['languages']== []:
                        country_select['languages'] = 'N/A'
                    
                    #encrypts
                    for lang_data in country_select['languages']:
                        language_name = sha1(lang_data.encode('utf-8')).hexdigest()
                    reg.append(region)
                    city.append(country_select['name'])
                    lang.append(language_name)
                    t_f2 = time()
                    time_ejec.append(float("%.2f" % ((t_f2-t_i2)*1000)))
                    df['Region'] = reg
                    df['City name'] = city
                    df['Language'] = lang
                    df['Time(ms)'] = time_ejec
                    #6 times
                    time_max = df['Time(ms)'].max()
                    time_min = df['Time(ms)'].min()
                    time_total = df['Time(ms)'].sum()
                    time_average = df['Time(ms)'].mean()
                    return df, time_max, time_min, time_total, time_average
                else:
                    print('No es una opcion')
            else:
                print('Tipo de dato no valido: {0}. ingrese un valor tipo String.'.format(type(op)))
    else:
        print('ingrese la lista de regiones')
              
def sqlite_insert(table_data):
    conn = sqlite3.connect('resultado_Prueba.db')
    table_data.to_sql(name='Tabla_Regiones', con=conn, if_exists='replace')
    table_data.to_json('data.json')

[regions, without_region] = regions_api_rest(url, headers)
[table_data, time_max, time_min, time_total, time_average] = country_regions(regions, without_region)
#7.Save Result and 8 generate Json
sqlite_insert(table_data)

print(table_data)

print(f"tiempo total {time_total:.2f}\ntiempo promedio {time_average:.2f}\ntiempo minimo {time_min:.2f}\ntiempo maximo {time_max:.2f}")
