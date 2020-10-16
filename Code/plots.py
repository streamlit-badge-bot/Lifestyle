import plotly.io as pio
import plotly.express as px
pio.templates.default = 'plotly_white'

from dataframes import DF_body, DF_meals

from variables import *
from others import *

colors = {
    'Weight': 'gray', 

    'Calories': 'black', 
    'Proteins': 'magenta', 
    'Carbohydrates': 'yellow', 
    'Lipids': 'cyan', 
    'Alcohol': 'white', 

    'Calories_/': 'black', 
    'Proteins_/': 'magenta', 
    'Carbohydrates_/': 'yellow', 
    'Lipids_/': 'cyan', 
    'Alcohol_/': 'white', 

    'Calories_iifmm': 'black', 
    'Proteins_iifmm': 'magenta', 
    'Carbohydrates_iifmm': 'yellow', 
    'Lipids_iifmm': 'cyan', 

    'Calories_%': 'black', 
    'Proteins_%': 'magenta', 
    'Carbohydrates_%': 'yellow', 
    'Lipids_%': 'cyan', 
}

groups = {
    'Weight': 'Weight', 

    'Calories': 'Calories', 
    'Proteins': 'Macros', 
    'Carbohydrates': 'Macros', 
    'Lipids': 'Macros', 
    'Alcohol': 'Macros', 

    'Calories_/': 'Calories', 
    'Proteins_/': 'Macros', 
    'Carbohydrates_/': 'Macros', 
    'Lipids_/': 'Macros', 
    'Alcohol_/': 'Macros', 

    'Calories_iifmm': 'Calories', 
    'Proteins_iifmm': 'Macros', 
    'Carbohydrates_iifmm': 'Macros', 
    'Lipids_iifmm': 'Macros', 
    'Alcohol': 'Macros', 

    'Calories_%': 'Calories', 
    'Proteins_%': 'Macros', 
    'Carbohydrates_%': 'Macros', 
    'Lipids_%': 'Macros', 
    'Alcohol_%': 'Macros', 
}

line_dash = {
    'Value': 'solid', 
    'Value_roll': 'dot', 
}

def get_df_plot(df, cols_to_plot, rolling_window):

    df = (df
        .melt(
            value_vars=cols_to_plot, 
            var_name='Variable', 
            value_name='Value_raw', 
            ignore_index=False, 
            )

        .assign(**{
            'Value_roll': lambda df: df.groupby('Variable').Value_raw.transform(lambda s: s.rolling(rolling_window, center=True, min_periods=1).mean())
            })
        
        .melt(
            id_vars=['Variable'], 
            value_vars=['Value_raw', 'Value_roll'], 
            var_name='Roll', 
            value_name='Value', 
            ignore_index=False, 
            )

        .assign(**{
            'Group': lambda df: df.Variable.map(groups)
            })

    )

    return(df)

def get_fig(df_plot, title):
    fig = (
        px.line(
            df_plot, 
            x=df_plot.index, 
            y='Value', 
            color='Variable', 
            line_group='Roll', line_dash='Roll', 
            facet_row='Group', 
            color_discrete_map=colors, 
            line_dash_map=line_dash, 
            title=title, 
            labels={'x': 'Date'}, 
            range_x=[date_range_min, date_range_max], 
            )
        .update_yaxes(
            matches=None, 
            #rangemode='tozero', 
            )
        .update_layout(
          showlegend=False, 
          )
    )
    return(fig)

def Plot_body(rolling_window):
    df_plot = DF_body().copy()

    cols_to_plot = ['Weight']

    df_plot = get_df_plot(df_plot, cols_to_plot, rolling_window)

    fig = get_fig(df_plot, 'Body')

    return(fig)

def Plot_nutrition(nutrition_information_kind, rolling_window):
    df_plot = DF_meals().copy()
    df_plot = df_plot.pipe(select_level, 2)

    cols_to_plot = nutrition_information_kinds[nutrition_information_kind]

    df_plot = get_df_plot(df_plot, cols_to_plot, rolling_window)

    fig = get_fig(df_plot, 'Nutrition')

    return(fig)