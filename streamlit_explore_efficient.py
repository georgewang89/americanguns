# ================================================== DOWNLOAD AND IMPORT PACKAGES ================================================== #
# !/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy
# pip install streamlit

import streamlit as st
from pandas.io.json import json_normalize
import json
import requests

# ================================================== GET DATA FROM API ================================================== #

# URL and auth are standard API parameters. But the 'params' parameter is unique to every web service that the API is calling.
# For example, Socrata (where OpenData is hosted) has a $query parameter that tells you how to use it. This is built into this example.
#https://dev.socrata.com/docs/queries/query.html

# ========== OPTION 1 ========== #
URL = 'https://data.cityofnewyork.us/resource/833y-fsy8.json'
payload = {'$select':'occur_date, latitude, longitude', '$limit':'50000'}
raw = requests.get(url=URL, params=payload, auth=('oddqm5a1h906snethsz3yxxy', '5z3gwa8zfaxtjdcxn67yqptce7h6ra2nhdka92o0wjsu9d63bw'))

# ========== OPTION 2 ========== #
# URL = 'https://data.cityofnewyork.us/resource/833y-fsy8.json?$select= occur_date,latitude,longitude&$limit=50000'
# raw = requests.get(url=URL, auth=('oddqm5a1h906snethsz3yxxy', '5z3gwa8zfaxtjdcxn67yqptce7h6ra2nhdka92o0wjsu9d63bw'))

# ========== CONVERT INTO DATAFRAME ========== #
# raw.content
raw_json = json.loads(raw.content)
raw_df = json_normalize(raw_json)

# ================================================== PROCESS DATA ================================================== #
processed_df = raw_df

# split year value out of year string and put it in a new column
processed_year = processed_df['occur_date'].str.split('-', n=1, expand=True)[0].astype(int)
processed_df.insert(1, 'OCCUR_YEAR', processed_year)

# convert longitude and latitude from string to int
processed_df['latitude'] = processed_df['latitude'].astype(float)
processed_df['longitude'] = processed_df['longitude'].astype(float)

# ================================================== OUTPUT ON SCREEN ================================================== #

# ========== SIDE BAR ========== #

# select in sidebar for YEAR
year_selected = st.sidebar.selectbox('choose year', processed_year.unique())

# mu
# year_selected = st.sidebar.selectbox('choose year', processed_year.unique())

# ========== MAIN WINDOW ========== #

if st.sidebar.checkbox('Show raw data'):
    raw_df

if st.sidebar.checkbox('Show processed data'):
    processed_df

# ========== MAP ========== #

rows_index_selected = processed_df['OCCUR_YEAR'] == year_selected
processed_df_selected = processed_df[rows_index_selected]
st.map(processed_df_selected.loc[:,'latitude':'longitude'])

# ========== CHARTS ========== #

# mplo