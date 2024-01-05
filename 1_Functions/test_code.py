#### Test Code, for Getting Git Repo Carbon Estimates ####

# What the code does : Sets Up the config file, and pulls necessary repo.
# To Run Code : change name_repo to be name of target repo and username to be target repo's owner

#### Global Variables ####

root_dir = 'C:/Users/Chees/Documents/GitHub/cloud_computing_emissions/'

username = 'dmlc'
name_repo = 'xgboost'

#### Library ####

import easygui
import os.path
from pathlib import Path
import pandas as pd
import numpy as np
import requests
import sys
import re
import os
import json
import streamlit as st

#### Setup ####

with open(root_dir + "/1_Functions/setup.py", "rb") as source_file:
    code = compile(source_file.read(), root_dir + "/1_Functions/setup.py", "exec")
exec(code)

#### Getting Repo ####

# Getting all Workflows

df = get_all_workflows_from_repo(token, username, name_repo)

# Getting Jobs

df_jobs = get_jobs_from_run(token, username, name_repo, df)

# Cleaning Data

df_jobs['started_at'] = pd.to_datetime(df_jobs['started_at'])
df_jobs['completed_at'] = pd.to_datetime(df_jobs['completed_at'])
df_jobs['duration'] = df_jobs['completed_at'] - df_jobs['started_at']
df_jobs['duration'] = pd.to_timedelta(df_jobs['duration'])/ pd.Timedelta(hours=1)

# Getting Carbon Emissions Estimates

df_jobs = get_co2_emissions_from_jobs(df_jobs)

# Export
df.to_csv(root_dir + '/0_Data/' + name_repo + '_w_emissions.csv')
