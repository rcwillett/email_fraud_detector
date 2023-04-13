
FROM --platform=linux/amd64 ubuntu:latest AS base
RUN  apt-get update \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/*
    
RUN wget https://repo.anaconda.com/archive/Anaconda3-2023.03-Linux-x86_64.sh
RUN bash Anaconda3-2023.03-Linux-x86_64.sh -b -p $HOME/anaconda3 &&\
    echo 'export PATH=$PATH:$HOME/anaconda3/bin' >>~/.bash_profile

# USER root
COPY . .
SHELL ["bash", "-lc"]
RUN conda config --add channels conda-forge &&\
    conda env create -f requirements.yml

FROM base AS server
CMD conda run -n capstone --live-stream python ./server.py

FROM base AS notebook
CMD conda run -n capstone --live-stream python ./server.py