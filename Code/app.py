import streamlit as st

import pandas as pd

from variables import date_range_min, date_range_max, nutrition_detail_levels, nutrition_information_kinds

from dataframes import DF_body, DF_iifmm, DF_aliments, DF_meals, DF_calisthenics
from plots import Plot_body, Plot_nutrition

from others import *

def main():

    update_database()

   # Sidebar
    st.sidebar.title('Options')

    date_min, date_max = st.sidebar.slider(
        label='Date range', 
        min_value=date_range_min, 
        max_value=date_range_max, 
        value=(date_range_max, date_range_max), 
        step=None, 
        format='YYYY-MM-DD'
        )
    dates = pd.date_range(start=date_min, end=date_max, freq='D')

    rolling_window = st.sidebar.number_input(
        'Rolling window', 
        min_value=1, 
        max_value=7, 
        value=1, 
        step=2, 
        )

    st.sidebar.header('Body')

    st.sidebar.header('Nutrition')
    nutrition_detail_level = st.sidebar.selectbox(
        label='Detail level', 
        options=['Day', 'Meal', 'Aliment'], 
        index=0, 
        )
    nutrition_information_kind = st.sidebar.selectbox(
        label='Information kind', 
        options=['Raw', 'Reference', 'Proportion', 'Iifmm', 'Percentage'], 
        index=0, 
        )

    st.sidebar.header('Calisthenics')
    st.sidebar.info('Calisthenics options: TO DO.')

    # Page
    st.title('Lifestyle')

    st.dataframe(DF_body()
        .loc[dates]
        .style
            .set_na_rep('-')
            .set_precision(1)
        )

    """st.dataframe(DF_aliments()
        )"""

    """st.dataframe(DF_iifmm()
        .loc[dates]
    )"""

    st.dataframe(DF_meals()
        .loc[dates]
        .pipe(select_level, nutrition_detail_levels[nutrition_detail_level])
        [nutrition_information_kinds[nutrition_information_kind]]
        )

    st.dataframe(DF_calisthenics()
        .loc[dates]
        )

    st.plotly_chart(
        Plot_body(rolling_window), 
        use_container_width=True, 
        )
    st.plotly_chart(
        Plot_nutrition(nutrition_information_kind, rolling_window), 
        use_container_width=True, 
        )

if __name__ == '__main__':

    st.beta_set_page_config(
        page_title='Lifestyle', 
        page_icon=None, 
        layout='wide', 
        initial_sidebar_state='auto'
        )

    main()