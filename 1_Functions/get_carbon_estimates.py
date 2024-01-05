#### Getting Carbon Estimates using Climatiq API ####

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
