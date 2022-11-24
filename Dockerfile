# Dockerfile with the PIA package installed and PIAWeb
# author: Micha Birklbauer
# version: 1.0.4

FROM ubuntu:20.04

LABEL maintainer="micha.birklbauer@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    git \
    libopenbabel-dev \
    libopenbabel6 \
    openbabel \
    python3-openbabel \
    pymol \
    python3-pymol \
    python3-distutils \
    python3-lxml \
    python3-rdkit \
    python3-pip

RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install scikit-learn
RUN pip3 install plip==2.2.2 --no-deps
RUN pip3 install biopandas
RUN pip3 install matplotlib
RUN pip3 install "protobuf<=3.20.0"
RUN pip3 install streamlit==1.1.0
RUN pip3 install jupyterlab

RUN git clone https://github.com/michabirklbauer/pia.git
WORKDIR pia
RUN python3 setup.py install
WORKDIR /

RUN git clone https://github.com/michabirklbauer/piaweb.git
WORKDIR piaweb

CMD  ["streamlit", "run", "streamlit_app.py"]
