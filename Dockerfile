# Use the jupyter base-notebook
FROM jupyter/base-notebook

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install graphviz

#RUN pip install numpy pandas networkx matplotlib seaborn itertools
# Removed itertools, since it seems to crash
RUN pip install numpy
RUN pip install pandas
RUN pip install networkx
RUN pip install matplotlib
RUN pip install seaborn
RUN pip install plotly
RUN pip install pm4py
