import pandas as pd
import numpy as np
import requests
import os
import json
import streamlit as st
import subprocess

# fct to get 100 runs
def get_workflows_from_repo(token, user_name, name_repo, page_nb):

  url = f'https://api.github.com/repos/{user_name}/{name_repo}/actions/runs?per_page=100&page={page_nb}'

  cmd = 'curl -G -H f"Authorization: token {token_git}" {url}'
  os.system(cmd.format(token_git = token, url = url))

  headers = {'Authorization': f'token {token}'}
  response = requests.get(url, headers=headers)

  if response.status_code == 200:
      workflows_data = response.json()
  else:
      print(f"Échec de la requête avec le code d'état {response.status_code}")

  return pd.DataFrame(workflows_data['workflow_runs'])


  # fct to get all runs from a repo
def get_all_workflows_from_repo(token, username, name_repo):

  df_final = pd.DataFrame()
  page_nb = 1
  while True:
    df = get_workflows_from_repo(token, username, name_repo, page_nb)

    if df.empty :
      break

    page_nb += 1
    df_final = pd.concat([df_final, df], axis = 0)

  return df_final


# fct to get all jobs for the runs of a repo
def get_jobs_from_run(token, username, name_repo, df_runs):

  df_jobs = pd.DataFrame()

  for i in df_runs['id']:

    url = f'https://api.github.com/repos/{username}/{name_repo}/actions/runs/{i}/jobs'

    cmd = f'curl -L \
      -H "Accept: application/vnd.github+json" \
      -H f"Authorization: Bearer {token}" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      {url}'

    os.system(cmd)

    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        run_id_jobs = response.json()
    else:
        print(f"Échec de la requête avec le code d'état {response.status_code}")

    df_jobs = pd.concat([df_jobs, pd.DataFrame(run_id_jobs['jobs'])], axis = 0)
    df_jobs['started_at'] = pd.to_datetime(df_jobs['started_at'])
    df_jobs['completed_at'] = pd.to_datetime(df_jobs['completed_at'])
    df_jobs['duration'] = df_jobs['completed_at'] - df_jobs['started_at']
    df_jobs['duration'] = pd.to_timedelta(df_jobs['duration'])/ pd.Timedelta(hours=1)

  return df_jobs


  # fct to get Carbon Emissions from Jobs with Climatiq API
def get_co2_emissions_from_jobs(df_jobs):
  climatiq_url = 'https://beta4.api.climatiq.io/compute/azure/cpu'
  co2_ems = []
  for i in range(len(df_jobs)):
    dur_job = df_jobs.iloc[i]['duration']

    data = {
    "cpu_count": 1,
    "region": "west_us",
    "duration": dur_job,
    "duration_unit": "h",
    }

    data = json.dumps(data)

    header = {
        'Authorization': f'Bearer {apikey_climatiq}',
    }

    response = requests.post(climatiq_url, headers=header, data=data)

    if response.status_code == 200:
        api_response = response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(response.text)
    co2_ems.append(api_response['co2e'])

  df_jobs['co2_emission'] = co2_ems
  df_jobs['unit'] = 'kg'

  return df_jobs