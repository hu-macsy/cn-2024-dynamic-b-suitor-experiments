#!/usr/bin/env python3

import os

def convert(graph_path):
    with open(graph_path, 'r') as file:
        ls = file.readlines()

if __name__ == "__main__":
    dir = "instances/konect"
    for graph in os.listdir(dir):
       graph_path = os.path.join(dir, graph)
       if os.path.isfile(graph_path):
           convert(graph_path)