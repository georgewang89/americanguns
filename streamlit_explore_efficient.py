# ================================================== DOWNLOAD AND IMPORT PACKAGES ================================================== #
# !/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy
# pip install streamlit
# pip install matplotlib

import streamlit as st
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import json
import requests
# import matplotlib.pyplot as plt

# ================================================== GET DATA FROM API ================================================== #
def pulldata():

    # URL and auth are standard API parameters. But the 'params' parameter is unique to every web service that the API is calling.
    # For example, Socrata (where OpenData is hosted) has a $query parameter that tells you how to use it. This is built into this example.
    #https://dev.socrata.com/docs/queries/query.html

    # ========== OPTION 1 ========== #
    URL = 'https://data.cityofnewyork.us/resource/833y-fsy8.json'
    payload = {'$select':'occur_date, latitude, longitude, vic_age_group', '$limit':'5000'}
    raw = requests.get(url=URL, params=payload, auth=('oddqm5a1h906snethsz3yxxy', '5z3gwa8zfaxtjdcxn67yqptce7h6ra2nhdka92o0wjsu9d63bw'))

    # ========== OPTION 2 ========== #
    # URL = 'https://data.cityofnewyork.us/resource/833y-fsy8.json?$select= occur_date,latitude,longitude&$limit=50000'
    # raw = requests.get(url=URL, auth=('oddqm5a1h906snethsz3yxxy', '5z3gwa8zfaxtjdcxn67yqptce7h6ra2nhdka92o0wjsu9d63bw'))

    # ========== CONVERT INTO DATAFRAME ========== #
    # raw.content
    raw_json = json.loads(raw.content)
    raw_df = json_normalize(raw_json)
    return raw_df

# ================================================== PROCESS DATA ================================================== #
processed_df = pulldata()

# split year value out of year string and put it in a new column

processed_year = processed_df['occur_date'].str.split('-', n=1, expand=True)[0].astype(int)
year_list = processed_year.unique()
firstyear = min(year_list)
lastyear = max(year_list)


processed_df.insert(1, 'occur_year', processed_year)

# convert longitude and latitude from string to int
processed_df['latitude'] = processed_df['latitude'].astype(float)
processed_df['longitude'] = processed_df['longitude'].astype(float)

# count number of shootings per year
def countfrequencyincol(df, column_name):
    return df.groupby(column_name).size()

def selectrows(df, filter_by, column_name):
    rows_selected = df.loc[df[column_name] == filter_by]
    return rows_selected

agegroup18_24 = selectrows(processed_df, '18-24', 'vic_age_group')

# ================================================== COMPUTING ================================================== #

shootingcount_peryear = countfrequencyincol(processed_df, 'occur_year')
shootingcount_peryear_18_24 = countfrequencyincol(agegroup18_24, 'occur_year')

# ================================================== OUTPUT ON SCREEN ================================================== #

# ========== SIDE BAR ========== #

if st.checkbox('Show raw data'):
    raw_df

if st.checkbox('Show processed data'):
    processed_df


# ========== CHARTS ========== #

shootingcount_peryear = shootingcount_peryear.rename("total")
shootingcount_peryear_18_24 = shootingcount_peryear_18_24.rename("18-24")

shootingsperyear = pd.concat([shootingcount_peryear, shootingcount_peryear_18_24], axis=1)
st.line_chart(shootingsperyear)


# ========== CHARTS BY AGE ========== #

# st.multiselect('victim age group', options={'<18', '18-24', '25-44', '45-64', '65+'})
# st.line_chart(shootingcount_peryear_18_24)

# ========== MAP ========== #

# select in sidebar for YEAR
year_selected = st.selectbox('choose year', processed_df['occur_year'].unique())

rows_index_selected = processed_df['occur_year'] == year_selected
processed_df_selected = processed_df[rows_index_selected]
st.map(processed_df_selected.loc[:,'latitude':'longitude'])

# ========== MAIN WINDOW ========== #




