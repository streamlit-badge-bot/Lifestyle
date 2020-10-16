import streamlit as st

import pandas as pd

from variables import dates_range
from others import get_aliment, agg_by_levels

def load_sheet(file_name, sheet_name):
    df = pd.read_excel(
        io='Data/{}.xlsx'.format(file_name), 
        sheet_name=sheet_name, 
        )
    return(df)

@st.cache()
def DF_body():
    df_body = (
        load_sheet('database', 'Body')

        .set_index(['Date'])
        .reindex(dates_range)

        [[
            'Weight', 
        ]]
    )
    return(df_body)

@st.cache()
def DF_aliments():
    """df_aliments = (
        load_sheet('database', 'Aliments')

        .set_index('EAN')
    )"""
    EANs = load_sheet('database', 'Meals').EAN.dropna().unique()
    df_aliments = {ean: get_aliment(str(ean)) for ean in EANs}
    df_aliments = (
      pd.DataFrame.from_dict(df_aliments, orient='index')
      )
    return(df_aliments)

@st.cache()
def DF_iifmm():
    df_iifmm = (
        load_sheet('database', 'Iifmm')

        .set_index(['Date'])
        .reindex(dates_range, method='ffill')

        .join(DF_body())
        .assign(**{
            'Proteins': lambda df: df.Proteins*df.Weight, 
            'Lipids': lambda df: df.Lipids*df.Weight, 
            'Carbohydrates': lambda df: (df.Calories - 4*df.Proteins - 9*df.Lipids) / 4, 
        })

        [[
            'Proteins', 'Carbohydrates', 'Lipids', 'Calories', 
        ]]
    )
    return(df_iifmm)

@st.cache()
def DF_meals():

    df_meals = (
        load_sheet('database', 'Meals').filter(['Date', 'Meal', 'EAN', 'Quantity'], axis='columns').dropna(subset=['EAN'])
        .assign(**{
            'Date': lambda df: df.Date.ffill(), 
            'Meal': lambda df: df.Meal.ffill(), 
            })

        .join(DF_aliments(), on='EAN')
        .assign(**{
            #'Aliment': lambda df: df.apply(lambda row: '{} ({})'.format(row.Aliment, row.Brand), axis=1)
            })

        #.drop_duplicates(subset=['Date', 'Meal', 'Aliment'], keep='last')
        .set_index(['Date', 'Meal', 'Aliment'])
        #.reindex(dates_range, level='Date')

        .assign(**{
            'Proteins': lambda df: df.Proteins_ref * df.Quantity/100, 
            'Carbohydrates': lambda df: df.Carbohydrates_ref * df.Quantity/100, 
            'Lipids': lambda df: df.Lipids_ref * df.Quantity/100, 
            'Alcohol': lambda df: df.Alcohol_ref * df.Quantity/100, 
            'Calories': lambda df: df.Calories_ref * df.Quantity/100, 
            })

        .pipe(agg_by_levels)

        .assign(**{
            'Proteins_/': lambda df: 100 * 4*df.Proteins / df.Calories, 
            'Carbohydrates_/': lambda df: 100 * 4*df.Carbohydrates / df.Calories, 
            'Lipids_/': lambda df: 100 * 9*df.Lipids / df.Calories, 
            'Alcohol_/': lambda df: 100 * 7*df.Alcohol / df.Calories, 
            })

        .join(DF_iifmm(), on='Date', rsuffix='_iifmm')
        .assign(**{
            'Proteins_%': lambda df: 100 * df.Proteins / df.Proteins_iifmm, 
            'Carbohydrates_%': lambda df: 100 * df.Carbohydrates / df.Carbohydrates_iifmm, 
            'Lipids_%': lambda df: 100 * df.Lipids / df.Lipids_iifmm, 
            'Calories_%': lambda df: 100 * df.Calories / df.Calories_iifmm, 
            })

        [[
            'Proteins_ref', 'Carbohydrates_ref', 'Lipids_ref', 'Alcohol_ref', 'Calories_ref', 
            'Proteins', 'Carbohydrates', 'Lipids', 'Alcohol', 'Calories', 
            'Proteins_/', 'Carbohydrates_/', 'Lipids_/', 'Alcohol_/', 
            'Proteins_iifmm', 'Carbohydrates_iifmm', 'Lipids_iifmm', 'Calories_iifmm', 
            'Proteins_%', 'Carbohydrates_%', 'Lipids_%', 'Calories_%', 
        ]]
    )
    return(df_meals)

@st.cache()
def DF_calisthenics():
    df_calisthenics = (
        load_sheet('database', 'Calisthenics')
        .assign(**{
            'Date': lambda df: df.Date.ffill(), 
            'Split': lambda df: df.Split.ffill(), 
            'Attribute': lambda df: df.Attribute.ffill(), 
            'Type': lambda df: df.Type.ffill(), 
            })

        .set_index(['Date', 'Split', 'Attribute', 'Type', 'Pattern'])
        .reindex(dates_range, level='Date')

        .drop('Notes', axis='columns')

    )
    return(df_calisthenics)
