import requests

def update_database():
    file_url = 'https://drive.google.com/file/d/1sVITrwQY4Fgeb9-9AOyegBdZOcDVCkvV/view?usp=sharing'
    file_id = file_url.split('/')[-2]
    download_url = 'https://drive.google.com/uc?export=download&id=' + file_id
    r = requests.get(download_url, allow_redirects=True)
    open('Data/database.xlsx', 'wb').write(r.content)

import numpy as np
import pandas as pd
import openfoodfacts
import re

def get_aliment_from_openfoodfacts(ean):
    import time
    time.sleep(1e-3)

    match = openfoodfacts.products.get_product(ean, locale='france')
    row_aliment = dict()
    if match['status']:
      match = match['product']

      row_aliment['Aliment'] = match.get('product_name')
      row_aliment['Brand'] = match.get('brands')

      row_aliment['Calories_ref'] = match.get('nutriments').get('energy-kcal_100g', 0.24*match.get('nutriments').get('energy_100g'))
      row_aliment['Proteins_ref'] = match.get('nutriments').get('proteins_100g')
      row_aliment['Carbohydrates_ref'] = match.get('nutriments').get('carbohydrates_100g')
      row_aliment['Lipids_ref'] = match.get('nutriments').get('fat_100g')
      row_aliment['Fibers_ref'] = match.get('nutriments').get('fiber_100g', 0)
      row_aliment['Alcohol_ref'] = match.get('nutriments').get('alcohol_100g', 0)

    return(row_aliment)

DF_ciqual = pd.read_excel('Data/Table Ciqual 2020_FR_2020 07 07.xls')\
    .assign(**{'alim_code': lambda df: df.alim_code.astype(str)})\
    .applymap(lambda x: '0' if x=='traces' else x)\
    .set_index('alim_code')

def clean_ciqual(string):
    string = re.sub(r'\,', '.', string)
    string = re.sub(r'[^\d\.]*', '', string)
    try:
        string = float(string)
    except: 
        string = np.nan
    return(string)

def get_aliment_from_ciqual(ean):
    row_aliment = dict()

    match = DF_ciqual.loc[ean]

    row_aliment['Aliment'] = match['alim_nom_fr']
    row_aliment['Brand'] = 'Ciqual'

    row_aliment['Calories_ref'] = clean_ciqual(match['Energie, Règlement UE N° 1169/2011 (kcal/100 g)'])
    row_aliment['Proteins_ref'] = clean_ciqual(match['Protéines, N x facteur de Jones (g/100 g)'])
    row_aliment['Carbohydrates_ref'] = clean_ciqual(match['Glucides (g/100 g)'])
    row_aliment['Lipids_ref'] = clean_ciqual(match['Lipides (g/100 g)'])
    row_aliment['Fibers_ref'] = clean_ciqual(match['Fibres alimentaires (g/100 g)'])
    row_aliment['Alcohol_ref'] = clean_ciqual(match['Alcool (g/100 g)'])
    return(row_aliment)

def get_aliment(ean):
    if len(ean)==15 or len(ean)==9:
        row_aliment = get_aliment_from_openfoodfacts(ean)
    else:
        row_aliment = get_aliment_from_ciqual(ean)
    return(row_aliment)

def agg_by_levels(df):
    df = pd.concat([

        df.reset_index()

        .assign(**{
            level: '' for level in df.index.names[k+1:]
            })

        .groupby(df.index.names).agg(lambda df: df.sum(skipna=False, min_count=1))

        for k in range(df.index.nlevels)

    ]).sort_index()

    return(df)

def select_level(df, level):
    for _ in range(level):
        df = df.xs('', level=-1)
    return(df)