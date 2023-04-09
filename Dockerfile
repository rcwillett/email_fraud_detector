FROM continuumio/conda-ci-linux-64-python3.8
COPY . .
RUN conda create --name server --file requirements.txt
RUN conda activate capstone
RUN python './server.py'