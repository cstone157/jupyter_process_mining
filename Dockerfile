# Use the jupyter base-notebook
FROM jupyter/base-notebook

#RUN pip install numpy pandas networkx matplotlib seaborn itertools
# Removed itertools, since it seems to crash
RUN pip install numpy pandas networkx matplotlib seaborn 
RUN pip install pm4py
