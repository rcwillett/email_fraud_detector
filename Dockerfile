
FROM --platform=linux/amd64 ubuntu:latest AS base
RUN  apt-get update \
    && apt-get install -y wget \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir ./models && curl -o ./models/bert_model_20_relu_sig.h5 https://rosswillett.blob.core.windows.net/models/bert_model_20_relu_sig.h5

RUN wget https://repo.anaconda.com/archive/Anaconda3-2023.03-Linux-x86_64.sh
RUN bash Anaconda3-2023.03-Linux-x86_64.sh -b -p $HOME/anaconda3 &&\
    echo 'export PATH=$PATH:$HOME/anaconda3/bin' >>~/.bash_profile

# USER root
COPY . .
SHELL ["bash", "-lc"]
RUN conda config --add channels conda-forge &&\
    conda env create -f requirements.yml

RUN chmod +rwx ./start.sh
ENTRYPOINT ["bash", "-lv", "./start.sh"]

FROM base AS server
CMD conda run -n capstone --live-stream python ./server.py

FROM base AS notebook
CMD jupyter notebook --allow-root --ip 0.0.0.0 --no-browser --port=8080