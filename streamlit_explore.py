import streamlit as st
import pandas as pd
import numpy as np
import time

# ================================================== DOWNLOAD DATA ================================================== #
#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
# client = Socrata("data.cityofchicago.org", None)

# Example authenticated client (needed for non-public datasets):

Domain = "data.cityofnewyork.us"
MyAppToken = "sImMGfdNFQ3dR1fQm1vr7nMTS"

client = Socrata(Domain,
                 MyAppToken)

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
raw = client.get("833y-fsy8", limit=50000)

# Convert to pandas DataFrame
raw_df = pd.DataFrame.from_records(raw)
processed_df = raw_df

# split year value out of year string and put it in a new column
processed_year = processed_df['occur_date'].str.split('-', n=1, expand=True)[0].astype(int)
processed_df.insert(1, 'OCCUR_YEAR', processed_year)

# convert longitude and latitude from string to int
processed_df['latitude'] = processed_df['latitude'].astype(float)
processed_df['longitude'] = processed_df['longitude'].astype(float)

# ================================================== OUTPUT ON SCREEN ================================================== #

# ========== SIDE BAR ========== #

# multiselect in sidebar
year_selected = st.sidebar.selectbox('choose year', processed_year.unique())

# ========== MAIN WINDOW ========== #

if st.sidebar.checkbox('Show raw data'):
    raw_df

if st.sidebar.checkbox('Show processed data'):
    processed_df

# ========== MAP ========== #

rows_index_selected = processed_df['OCCUR_YEAR'] == year_selected
processed_df_selected = processed_df[rows_index_selected]
st.map(processed_df_selected.loc[:,'latitude':'longitude'])