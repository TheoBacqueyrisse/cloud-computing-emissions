import pandas as pd
import numpy as np
import requests
import os
import json
import streamlit as st
import subprocess

st.title("Carbon Emissions from Cloud Computing")
st.write("Hello, this is a Streamlit app for our Data Mining Project")
st.write("We are two students of the M2 - D3S at TSE")

# SideBar Configuration

st.sidebar.image('images_app/TSE_Logo_2019.png', width=300)

st.sidebar.write('Choose a GitHub Repository :')

options = ['Numpy', 'Tensorflow', 'Tidyverse']
selected_option = st.sidebar.selectbox('Sélectionnez une option', options)


# if selected_option == 'Numpy':
#   df_jobs_with_co2 = pd.read_csv('/content/cloud_computing_emissions/0_Data/tidyverse_data.csv')

# if selected_option == 'Tensorflow':
#   df_jobs_with_co2 = pd.read_csv('/content/cloud_computing_emissions/0_Data/tidyverse_data.csv')

if selected_option == 'Tidyverse':
  df_jobs_with_co2 = pd.read_csv('/content/cloud_computing_emissions/0_Data/tidyverse_data.csv')

sum_em_repo = df_jobs_with_co2['co2_emission'].sum()
sum_em_repo = "{:.3f}".format(sum_em_repo)

col1, col2 = st.beta_columns(2)

# Content for the first column
with col1:
    st.header(f"Global KPI for the {selected_option} repository")
    st.write(f'Total Co2 emissions : {sum_em_repo}') 
    st.write(f'Number of Runs : {len(df_jobs['run_id'].unique())}')
    st.write(f'Number of Jobs : {len(df_jobs)}')
    st.write(f'Mean Number of Jobs per Run : {len(df_jobs) // len(df_jobs['run_id'].unique())}')

# Content for the second column
with col2:
    st.header("Co2 Emissions across Time")
    plt.figure(figsize=(10, 6))
    plt.plot(df_jobs[''], df_jobs['co2_emission'], color='r')
    plt.xlabel('Date')
    plt.ylabel('Co2 Emission')