# Fraud Email Identifier Project

## Overview

The purpose of this project is to build a machine learning model which can identify if an email is fraud based solely on the text content of that email. First data to train a model on was aquired, cleaned and combined. Next, this data was analyzed and several simple models were built using it. Finally a neural network using transfer learning from a BERT encoding model was built and trained for this identification task.

## Files

This section details the notebooks included in this project and a brief description of what each notebook contains.

### Data_Cleaning.ipynb

This file contains the analysis and cleaning performed for of the various data sets that were acquired and combined to train resulting machine learning models on.

### Data_Analysis.ipynb

This file contains an analysis of the final cleaned and combined data set and examines the text content of this data set.

### Simple_Modeling.ipynb

This file contains the training and evaluation of several simple machine learning algorithms using the data generated from the previous files.

### BERT_Model_Build.ipynb

This file contains the code used for the generation of a transfer learning model built on a BERT transformer.

### BERT_Test.ipynb

This file contains an evaluation of the transfer learning model built on the BERT transformer.


## Data Sources

[Kaggle Fraud Email Dataset](https://www.kaggle.com/datasets/pramodgupta92/fraud-email-datasets)
[Phishing Email Data by Type](https://www.kaggle.com/datasets/charlottehall/phishing-email-data-by-type)
[Phishing Academic Torrent](https://academictorrents.com/details/a77cda9a9d89a60dbdfbe581adf6e2df9197995a)
[Apache Spam Assassin Public Corpus](https://spamassassin.apache.org/old/publiccorpus/)