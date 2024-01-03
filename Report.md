# Predicting the Carbon Cost of Cloud Computing
Project 10: Continuous Integration Carbon Footprint - Théo Bacqueyrisse & Benjamin Rocheteau

## Table of Contents

1. [Introduction](#introduction)
2. [GitHub API](#github_api)
3. [Climatiq API](#climatiq_api)
4. [The Code](#the_code)
5. [The App](#the_app)

## Introduction

Nowadays, a lot of different projects are created by developpers and are made open source through a Python package for example, to be usable by any programmer or data sceintist. These projects enable the user to solve efficiently a problematic in his specific use case. For example, a project like Matplotlib, which is Open-Source and hosted on Github, is very well known to perform data vizualisation tasks efficiently.

Such projects are also made public to be continuously improved, with bug corrections and new features implementation for example. Such changes can be proposed by the programming community that can bring a lot of new ideas, be part of relevant discussions and detect problems very quickly. They can also be part of the project by proposing the changes to be made to a project. In this way, the programming comunity can activly participate in the conception and improvement of a project. 

This process is called Continuous Integration, making the changes made to a shared repository very efficient and open to new ideas.  It is a huge asset for the progress of programming possibilities in our opinion, which has been exponential for a few years and will surely yield incredible new features into the world in the future.

But we also know that the growth of this area present some major drawbacks, one of which being the carbon dioxyde emissions made by the energy consumed by the variety of elements related to these activities. For example, for a data scientist, training a deep learning model can take an important amount of time, which can consume a lot of electricity, especially with the use of Graphical Processing Units (GPU) and servers. 

But a tremendous part of the emissions come from the servers on which are stored any programming object such as datasets or projects. In the frame of Continuous Integration, the projects available on GitHub that are updated regularly are srotred in servers, and fixing these projects come at a cost, that is electricity emission from the unit that performs the update during the necessary runtime, that in turn induces a carbon emission. Because the projects are numerous, and the updates are regular and possibily long, the carbon emissions coming from Continuous Integration are important to consider. Indeed, in our climate crisis context, controlling carbon emissions from every possible aspect is crucial to limit global warming. 

We believe that the technological progress made in the field of programming can be a huge source of value to help tackle these climate challenges, but having an overview of the costs of this progress is important, as it may give insights on the source of highest emissions for example, so that the processes could be optimized in the future in term of carbon emissions.

In this project, we develop a solution to estimate the carbon emissions from a GitHub repository using Continuous Integration, and we present some insights of these emissions using a Streamlit app.

## GitHub API

The cloud computing emissions for a project hosted on GitHub come from the workflows of changes made to this GitHub repository. These workflows can be found in the *GitHub Actions* tab of an **open-source** repository. If the chosen repository is working with Continuous Integration, a list of runs will be displayed describing what are the changes that were made to the repository, ranked by dates of updates.

The first process to be created is the collection of these workflows in Python, which can be done by using the GitHub Rest API, that enable us to collect various data from GitHub. This collection needs a GitHub token giving access to the workflow runs of an open-source repository. Such a token can be created by any GitHub user in his *Developer Settings*. 

## Climatiq API

## The Code

## The App
