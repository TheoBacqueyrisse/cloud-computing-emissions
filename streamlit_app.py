import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

custom_css = """
.css-1l02zno {
    padding-left: 15px !important;
    padding-right: 15px !important;
}
"""

# Inject custom CSS
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

st.title("Carbon Emissions from Cloud Computing")
st.write("Hello, this is a Streamlit app for our Data Mining Project for our Masters 2 Diploma at TSE.")

st.markdown("<hr>", unsafe_allow_html=True)

# SideBar Configuration

st.sidebar.image('images_app/TSE_Logo_2019.png', width=300)
st.sidebar.markdown("""
Benjamin Rocheteau - Théo Bacqueyrisse
""")

st.sidebar.markdown("""
**Choose a GitHub Repository :**
""")

options = ['Numpy', 'Pandas', 'Tidyverse']
selected_option = st.sidebar.selectbox('Sélectionnez une option', options)


if selected_option:

  if selected_option == 'Tidyverse':
    # Load the Data
    df = pd.read_csv('/content/drive/MyDrive/Data Mining Data/tidyverse_data_with_Co2.csv')

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


    st.write(f"**Global KPI for the {selected_option} repository**")
    st.markdown(f"""
      - Number of Runs : {nb_runs}
      - Number of Jobs : {nb_jobs}
      - Mean Number of Jobs per Run : {mean_jobs_per_run}
      - Mean Carbon Emission by Run : {mean_co2_byrun} KgEqCO2
      - Mean Run Duration : {mean_duration} minutes
    """)

    st.markdown("""**Here is the evolution of Carbon emissions across time for Tidyverse**""")
    st.line_chart(data = df, x = None, y = 'co2_emission', color='#FFFFFF', width=150, height=400, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
  
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Run status distribution**")

        value_counts = df['conclusion'].value_counts().reset_index()
        value_counts.columns = ['Value', 'Count']

        st.bar_chart(data=value_counts, x='Count', y='Value', color='#FF7F7F', width=150, height=400, use_container_width=True)

        
    st.write(f"**Duration Variable Distribution**")

    st.area_chart(data = df, x = None, y = 'duration', color='#FF7F7F', width=150, height=400, use_container_width=True)
    st.line_chart(data = df, x = None, y = 'co2_emission', color='#000000', width=150, height=400, use_container_width=True)

    runners = np.where(len(df['labels'])>0).apply(lambda x: x.split('-'))[0]
    
    fig, ax = plt.subplots()
    sns.set(style="whitegrid")
    sns.barplot(x=df['labels'], y='Category', data=df, ax=ax)
    ax.set_title('Horizontal Bar Plot Example')
    st.pyplot(fig)
