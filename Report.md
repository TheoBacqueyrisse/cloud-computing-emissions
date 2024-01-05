# Predicting the Carbon Cost of Cloud Computing
Project 10: Continuous Integration Carbon Footprint - Théo Bacqueyrisse & Benjamin Rocheteau

## Table of Contents

1. [Introduction](#introduction)
2. [GitHub API](#github-api)
3. [Climatiq API](#climatiq-api)
4. [The Code](#the-code)
5. [The App](#the-app)

## Introduction

Nowadays, a lot of different projects are created by developpers and are made open source through a Python package for example, to be usable by any programmer or data sceintist. These projects enable the user to solve efficiently a problematic in his specific use case. For example, a project like Matplotlib, which is Open-Source and hosted on Github, is very well known to perform data vizualisation tasks efficiently.

Such projects are also made public to be continuously improved, with bug corrections and new features implementation for example. Such changes can be proposed by the programming community that can bring a lot of new ideas, be part of relevant discussions and detect problems very quickly. They can also be part of the project by proposing the changes to be made to a project. In this way, the programming comunity can activly participate in the conception and improvement of a project. 

This process is called Continuous Integration, making the changes made to a shared repository very efficient and open to new ideas.  It is a huge asset for the progress of programming possibilities in our opinion, which has been exponential for a few years and will surely yield incredible new features into the world in the future.

But we also know that the growth of this area present some major drawbacks, one of which being the carbon dioxyde emissions made by the energy consumed by the variety of elements related to these activities. For example, for a data scientist, training a deep learning model can take an important amount of time, which can consume a lot of electricity, especially with the use of Graphical Processing Units (GPU) and servers. 

But a tremendous part of the emissions come from the servers on which are stored any programming object such as datasets or projects. In the frame of Continuous Integration, the projects available on GitHub that are updated regularly are srotred in servers, and fixing these projects come at a cost, that is electricity emission from the unit that performs the update during the necessary runtime, that in turn induces a carbon emission. Because the projects are numerous, and the updates are regular and possibily long, the carbon emissions coming from Continuous Integration are important to consider. Indeed, in our climate crisis context, controlling carbon emissions from every possible aspect is crucial to limit global warming. 

We believe that the technological progress made in the field of programming can be a huge source of value to help tackle these climate challenges, but having an overview of the costs of this progress is important, as it may give insights on the source of highest emissions for example, so that the processes could be optimized in the future in term of carbon emissions.

In this project, we develop a solution to estimate the carbon emissions from a GitHub repository using Continuous Integration, and we present some insights of these emissions using a Streamlit app.

## GitHub API

### Collect the Worflow runs from a repository

The cloud computing emissions for a project hosted on GitHub come from the workflows of changes made to this GitHub repository. These workflows can be found in the *GitHub Actions* tab of an **open-source** repository. If the chosen repository is working with Continuous Integration, a list of runs will be displayed describing what are the changes that were made to the repository, ranked by dates of updates.

The first process to be created is the collection of these workflows in Python, which can be done by using the GitHub Rest API, that enable us to collect various data from GitHub. This collection needs a GitHub token giving access to the workflow runs of an open-source repository. Such a token can be created by any GitHub user in his *Developer Settings*. 

First of all, in order to collect the runs for a given repository, we have to use the *user_name* and the *name_repo* of the repository, as well as define our GitHub token value : 

Here is an example if choosing to collect the runs from the Pandas repository.

```python
username = "pandas-dev"
name_repo = "pandas"
token = "************************"
```

Using the GitHub Rest API, **only 100 runs can be collected per API call**. This is why we defined our process using two functions :

- First, we coded a function to obtain 100 runs from a repository. Since the runs are organized by page, we use a parameter $page_number$ to be given in the function call. Then, by displaying 100 runs by page, we collect the runs of the given $page_number$. Here is the python code for this function :


```python
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
```

This function first define the url where to recover the runs from. We see that we set here the parameter *per_page=100* and the *page = page_nb*. Then, we execute a command line, which connects to the GitHub Rest API with our GitHub token, and recovers the dataframe located at the specified url with a *requests.get*. The obtained data is in json format, and we return it in form of a Pandas dataframe for the second function.

- Then, using this first function, we coded another function that calls the first function for every page number until the first empty page of runs, so when the last run has been collected. The function thus sends a Pandas dataframe at each API call composed of 100 rows / runs, and this dataframe is concatenated with a general Pandas dataframe at each step. This process can take a long time for heavy repositories. Indeed, we for example collected the runs for the *Numpy* repository composed of around 100,000 runs, and the function took around 4 hours to run in colab. A lighter repository, *Tidyverse*, took around 5 minutes to obtain. Here is the code we used :

```python
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
```
```python
df = get_all_workflows_from_repo(token, username, name_repo)
```

This is how the dataset obtained looks like for the *Pandas* repository: 

<p>
<img src="images/pandas_runs.png" alt="Alt text">
</p>

This dataset contains :

- The run_id to identify the different runs 
- The event of the run (can be a pull request for example)
- The duration of the update
- The result of the modification
- Branches information as the modification can have been testes in a sub-branch before being pushed on the main branch
- Other information


At the end of this function, we added an option to send this dataset containing all the runs from the chosen repository to our [Google Drive file](https://drive.google.com/drive/folders/16rD7bP4xZZ5GKvw-5t8xnh3eD2T3TxSt).

This file will be used for our later Streamlit application, and it is useful to save our file to avoid re-running this piece of code.

### Collect the Jobs that were performed in each Run

The next step for our estimation was to try to go deeper into the tasks that are performed during each run. In GitHub, these tasks are called Jobs, and detail the different steps in a Run that brings a change to a given repository. The jobs are available for recovery using the GitHub Rest API again, using a similar process than for the runs. 

However, we did not find a way to recover the jobs using a batched API call. This means that our current method is performing an API call for each of the runs in a repository. So when working with *Numpy* for example, we would have to make more than 100,000 API calls to recover the jobs. When trying to do so, we faced a computational issue making the jobs recovery very hard for big repositories. 

This is the function that we used for our attempt : 

```python
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
        continue

    df_jobs = pd.concat([df_jobs, pd.DataFrame(run_id_jobs['jobs'])], axis = 0)
  return df_jobs
```
This function first defines the url to get the jobs from. We see that in this parameter we have to specify the *run_id* to be analyzed, which is responsible for the fact that we can recover jobs from only one run with 1 API call. Then, it executes a command line to connect to GitHub Rest using the GitHub token, and collecting the searched dataset from the url in form of a json dataframe that we convert into a pandas dataframe. We then concatenate the obtained data with a general dataset at each step. 

We tried two different approaches with this method : 

- First, we tried to recover all the jobs at once by just running the function.

- Then, we tried to perform batches of recovery using slices of indexes of the datasets containing the runs.

Unfortunately, both approaches failed for big repositories, due to memory issues or API calls limitaition. This process may be possible to optimize, first by making sort each step does not perform a concatenation of datasets that use a big amount of memory in the process. This optimization may be part of a next step for this project.

For the *Tidyverse* on the contrary, we were able to recover the jobs for the mearly 350 runs in the repository. Here is what the obtained dataset looks like : 

<p>
<img src="images/tidyverse_wo_co2.png" alt="Alt text">
</p>

This data contains information on :

- The *run_id* related to the job
- The git branch on which the change is being made
- Details on the job
- The status of the specific change of the job, that is completed or not 
- The success (or not) of the update 
- The duration of the update 
- The runners from which the update comes from, so the operating system of the developer that started the change (Ubuntu, Windows, macOS)
- Other information are provided

In fact, for carbon emission estimations, the duration of the Jobs or Runs is what we are most interested in, and additional information will help us to understand the details of these emissions.

## Climatiq API

Once we have the job durations and runners, we can proceed to try and get estimates for the carbon emissions generated by those jobs. To do so, we use the Climatiq API, which we are able to access as university students. 

## The Code

We automate the collection of these estimates using the followinng Python script. 

```python

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

```

The script adds two columns to our dataset : `co2_emission` and `unit`, which gives us the carbon emission estimate for each run. 

## The App
