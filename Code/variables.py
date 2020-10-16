import pandas as pd

date_range_min = pd.to_datetime('2020-06-03').date()
date_range_max = pd.to_datetime('today').date()
dates_range = pd.date_range(start=date_range_min, end=date_range_max, freq='D')

nutrition_detail_levels = {
    'Day': 2, 
    'Meal': 1, 
    'Aliment': 0
}

nutrition_information_kinds = {
    'Reference': ['Proteins_ref', 'Carbohydrates_ref', 'Lipids_ref', 'Alcohol_ref', 'Calories_ref'], 
    'Raw': ['Proteins', 'Carbohydrates', 'Lipids', 'Alcohol', 'Calories'], 
    'Proportion': ['Proteins_/', 'Carbohydrates_/', 'Lipids_/', 'Alcohol_/'],
    'Iifmm': ['Proteins_iifmm', 'Carbohydrates_iifmm', 'Lipids_iifmm', 'Calories_iifmm'], 
    'Percentage': ['Proteins_%', 'Carbohydrates_%', 'Lipids_%', 'Calories_%'], 
}

