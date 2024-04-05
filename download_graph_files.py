#!/usr/bin/env python3

import os
import shutil
import tarfile
import urllib.request

def download(group, graph):
    url = f'https://suitesparse-collection-website.herokuapp.com/MM/{group}/{graph}.tar.gz'
    input_dir = 'instances'
    tmp_dir = os.path.join(input_dir, 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)

    tar_filename = os.path.join(tmp_dir, f"{graph}.tar.gz")
    graph_filename = f"{graph}.mtx"
    dest_path = os.path.join(input_dir, graph_filename)


    if os.path.exists(dest_path):
        print(f"{graph} already exists.")
        return

    urllib.request.urlretrieve(url, tar_filename)

    with tarfile.open(tar_filename, 'r:gz') as tar:
        try:
            tar.extractall(path=tmp_dir)
            shutil.move(os.path.join(tmp_dir, graph, graph_filename), dest_path)
            os.remove(tar_filename)
            shutil.rmtree(tmp_dir)

        except Exception as er:
            print(f"Error: {str(er)}")

        # try:
        #     member = tar.getmembers()[0]
        #     member.path = member.path.split('/', 1)[-1]
        #     tar.extractall(path=input_dir, members=[member])
        # except KeyError:
        #     print(f"File '{graph}.mtx' not found.")

    # os.remove(tar_filename)

if __name__ == "__main__":
    graph_file = 'graphs.txt'
    with open(graph_file, 'r') as file:
        instances = file.read().splitlines()

    for instance in instances:
        if not instance.startswith('#') and instance.strip():
            group, graph = instance.split('/')
            download(group, graph)
