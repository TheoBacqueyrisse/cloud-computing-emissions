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
import os
import json
import streamlit as st

#### Setting Up Config File ####

# We check if config.txt exists - if not, we create
f = open(root_dir/"0_Data/config.txt", 'a')

# We read the contents of config.txt
f_lines = file.readlines()

# We split it into name and token
f_list = [i.split(': ', 1) for i in f_lines]


#### Setting Up Global Variables ####

#### Sourcing Code ####

sys.path.append(os.path.abspath(root_dir + '1_Functions/')

import get_carbon_estimates
import pull_from_github
