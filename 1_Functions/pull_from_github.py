#### Pulling from GitHub API ####


#### Getting a Page of Workflow from Target Repo ####

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

#### Getting all Workflows from Target Repo ####

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

#### Getting Jobs from Workflow Run ####

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
  return df_jobs
