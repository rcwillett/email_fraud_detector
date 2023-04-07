# Fraud Email Identifier Project

## Overview

The purpose of this project is to build a machine learning model which can identify if an email is fraud based solely on the text content of that email. First data to train a model on was aquired, cleaned and combined. Next, this data was analyzed and several simple models were built using it. Finally a neural network using transfer learning from a BERT encoding model was built and trained for this identification task.

## Running the Notebooks

In order to run the contents of the notebook files, several steps must be taken. First, the "Anaconda" software must be installed on the host machine. (Currently version 23.1.0 is used for this project) Next, the following command must be run from the command line in the root directory of this project:

`conda create --name capstone --file requirements.txt`

Once this is done, a conda environment should be ready for use with the notebook files. If an error of an unfound kernal is displayed simply select the "capstone" conda environment kernal from the available options.

In order to run the notebooks, the data (located in csv files) will need to be extracted into a "data" folder in the working directory of this project. (Link to files provided if you are given the correct permissions)

The Jupyter notebooks should be ready to be run once this is done.

## Files

This section details the notebooks included in this project and a brief description of what each notebook contains.

### Email_Fraud_Detection_1_Data_Cleaning.ipynb

This notebook contains the analysis and cleaning performed for of the various data sets that were acquired and combined to train resulting machine learning models on.

### Email_Fraud_Detection_2_Data_Analysis.ipynb

This notebook contains an analysis of the final cleaned and combined data set and examines the text content of this data set.

### Email_Fraud_Detection_3_Simple_Modeling.ipynb

This notebook contains the training and evaluation of several simple machine learning algorithms using the data generated from the previous files.

### Email_Fraud_Detection_4_BERT_Build.ipynb

This notebook contains the code used for the generation of a transfer learning model built on a BERT transformer.

### Email_Fraud_Detection_5_BERT_Test.ipynb

This notebook contains an evaluation of the transfer learning model built on the BERT transformer.

## TextTransformers.py

A module used in several notebooks and other files containing functions to transform the text content of emails.

## ContentTransformer.py

A module used in some notebooks and the server with a function to transform text data into a format usable for the simple models created in this project.

## eml_rename.py

A python script used to rename files to ones with a .eml extension (This was necessary for extracting raw email content)

## email_extractor.py

A python script used to extract data from all .eml files in a given directory, and combine this data into a csv file.

## Data Sources

[Kaggle Fraud Email Dataset](https://www.kaggle.com/datasets/pramodgupta92/fraud-email-datasets)
[Phishing Email Data by Type](https://www.kaggle.com/datasets/charlottehall/phishing-email-data-by-type)
[Phishing Academic Torrent](https://academictorrents.com/details/a77cda9a9d89a60dbdfbe581adf6e2df9197995a)
[Apache Spam Assassin Public Corpus](https://spamassassin.apache.org/old/publiccorpus/)