
    FROM continuumio/conda-ci-linux-64-python3.8 AS base
    USER root
    COPY . .
    RUN conda config --add channels conda-forge
    RUN conda env create -f requirements.yml && conda activate capstone

    FROM base AS server
    RUN python ./server.py

    FROM base AS notebook
    RUN python -m notebook