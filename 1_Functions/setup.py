#### Start-Up Code ####

# What this code does:
# How to use:
# What goes in:
# What comes out:

#### Library ####

import easygui
import os.path
from pathlib import Path

#### Setting Up Config File ####

#We get root path
root_dir = Path(__file__).resolve().parent

# We check if config.txt exists - if not, we create
f = open(root_dir/"0_Data/config.txt", 'a')

# We read the contents of config.txt
f_lines = file.readlines()

# We split it into name and token
f_list = [i.split(': ', 1) for i in f_lines]


#### Setting Up Global Variables ####

#### Sourcing Code ####
