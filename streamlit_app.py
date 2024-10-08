import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st

st.set_page_config(layout="wide")
custom_css = """
.css-1l02zno {
    padding-left: 15px !important;
    padding-right: 15px !important;
}
"""
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

st.title("Carbon Emissions from Cloud Computing")
st.write("Hello, this is a Streamlit app for our Data Mining Project for our Masters 2 Diploma at TSE.")

st.markdown("<hr>", unsafe_allow_html=True)

# SideBar
st.sidebar.image('assets/TSE_Logo_2019.png', width=300)
st.sidebar.markdown("""Benjamin Rocheteau - Théo Bacqueyrisse""")
st.sidebar.markdown("""**Choose a GitHub Repository :**""")

options = ['Tidyverse', 'Numpy', 'Pandas']
selected_option = st.sidebar.selectbox('Sélectionnez une option', options)


if selected_option:

  if selected_option == 'Tidyverse':
    
    st.markdown(f"## Chosen Repository : {selected_option}", unsafe_allow_html=True)

    # Load the Data
    df = pd.read_parquet('data/tidyverse_data_with_co2.parquet')
    df = df.iloc[::-1].reset_index()
      
    # Parameters to plot
    sum_em_repo = df['co2_emission'].sum()
    sum_em_repo = "{:.3f}".format(sum_em_repo)

    nb_runs = len(df['run_id'].unique())
    nb_jobs = len(df)

    mean_jobs_per_run = len(df) // len(df['run_id'].unique())

    mean_co2_byrun = np.mean(df['co2_emission'])
    mean_co2_byrun = "{:.5f}".format(mean_co2_byrun)

    mean_duration = np.mean(df['duration'])
    mean_duration = 60 * mean_duration #to get minutes
    mean_duration = "{:.3f}".format(mean_duration)

    runners = df['labels']
    runners = [runners[i].split('-')[0][2:] for i in range(len(runners))]  
    df_runners = pd.DataFrame()
    df_runners['runners'] = runners
    df_runners['runners'] = [str.lower(df_runners['runners'][i]) for i in range(len(df_runners))] 
    value_counts = df_runners['runners'].value_counts().reset_index()
    value_counts.columns = ['Valeur', 'Comptage']
    df['labels'] = [str.lower(df['labels'][i]) for i in range(len(df))] 

    df_job_count = pd.DataFrame()
    df_job_count['jobs'] = df['workflow_name']
    count_jobs = df_job_count['jobs'].value_counts().reset_index()
    count_jobs.columns = ['Valeur', 'Comptage']

    df['duration'] = 60*df['duration']
      
    # Content
    st.markdown(f"<h3>Global KPI :</h3>", unsafe_allow_html=True)
    st.markdown(f"""
      - Total Co2 Emissions: {sum_em_repo} KgEqCO2
      - Number of Runs : {nb_runs}
      - Number of Jobs : {nb_jobs}
      - Mean Number of Jobs per Job : {mean_jobs_per_run}
      - Mean Carbon Emission by Job : {mean_co2_byrun} KgEqCO2
      - Mean Job Duration : {mean_duration} minutes
    """)

    st.markdown("""<h3 style='text-align: center;'>Here is the evolution of Carbon emissions across time for Tidyverse </h3>""", unsafe_allow_html=True)
    st.line_chart(data = df, x = None, y = 'co2_emission', color='#FFFFFF', width=150, height=400, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
  
    col1, col2 = st.columns(2)

    with col1:

      st.markdown("<h3 style='text-align: center;'>Operating Systems Distribution</h3>", unsafe_allow_html=True)

      custom_labels = ['Ubuntu', 'None', 'Windows', 'macOS']
      custom_colors = ['#011f4b', '#03396c', '#005b96', '#6497b1']

      fig = px.pie(value_counts, values='Comptage', names=custom_labels, color_discrete_sequence=custom_colors)
      fig.update_layout(height=250, margin=dict(l=30, r=30, t=5, b=5), autosize=False)

      st.plotly_chart(fig, width=150, height=250, use_container_width=True)

      st.scatter_chart(
        df,
        y='co2_emission',
        color='labels',
      )

    with col2:

      st.markdown("<h3 style='text-align: center;'>Job Performed Distribution</h3>", unsafe_allow_html=True)

      custom_labels = ['R-CMD-check', 'Commands', 'pkgdown', 'pages build and deployment', 'test-coverage', 'lint']
      custom_colors = ['#011f4b', '#03396c', '#005b96', '#6497b1', '#b3cde0', '#ffffff']

      fig = px.pie(count_jobs, values='Comptage', names=custom_labels, color_discrete_sequence=custom_colors)
      fig.update_layout(height=250, margin=dict(l=30, r=30, t=5, b=5), autosize=False)

      st.plotly_chart(fig, width=150, height=250, use_container_width=True)

      st.scatter_chart(
        df,
        y='co2_emission',
        color='workflow_name',
      )

    st.markdown("<h3 style='text-align: center;'>Sample of obtained Estimations</h3>", unsafe_allow_html=True)
    st.dataframe(df[['id', 'run_id', 'run_url', 'labels', 'workflow_name', 'duration', 'co2_emission', 'unit']].sort_values(by = 'co2_emission', ascending = False).head())

  else : 
    st.markdown(f"## Chosen Repository : {selected_option}", unsafe_allow_html=True)

    st.markdown(f"Sorry, emission data for {selected_option} is not yet available", unsafe_allow_html=True)