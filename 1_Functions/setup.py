#### Start-Up Code ####

# What this code does: Sets everything up to get carbon estimates from github repos
# Code needs: Global Variable root_dir, string path to root of repo
# What comes out: config.txt

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

#### Setting Up Config File & Setting up Global Variables ####

global token
global apikey_climatiq

# We check if config.txt exists - if not, we create
f = open(root_dir + "0_Data/config.txt", 'a+')
f.seek(0)

# We read the contents of config.txt
f_lines = f.readlines()

# We split it into name and token
f_list = [re.sub('[\s+]', '', i).split('=', 1) for i in f_lines]

# We check which tokens are in the config file, and get the rest

for i in f_list:

    if i[0] == 'token':
        token = i[1]
    elif i[0] == 'apikey_climatiq':
        apikey_climatiq = i[1]

# Getting Variables not in Config & adding them to config.txt

if 'token' not in globals() or 'token' == '':
    token = easygui.enterbox("GitHub PAT Token:")
    f.write("token = " + token + "\n")

if 'apikey_climatiq' not in globals() or 'apikey_climatiq' == '':
    apikey_climatiq = easygui.enterbox("Climatiq API Key:")
    f.write("apikey_climatiq = " + apikey_climatiq + "\n")

f.close()

print('Config Complete')

#### Sourcing Code ####

sys.path.append(os.path.abspath(root_dir + '1_Functions/'))

from get_carbon_estimates import *
from pull_from_github import *

print('Sourcing Complete')
