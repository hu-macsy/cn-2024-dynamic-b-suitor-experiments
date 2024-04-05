#!/usr/bin/env python3

import argparse
import os

# transform weights to fit between 0 and 1
def transform(w, mn, mx):
    return (w - mn) / (mx - mn)

def process(graph_path):
    with open(graph_path, 'r') as file:
        ls = file.readlines()

    header_ls = []
    for l in ls:
        if l.startswith('%'):
            header_ls.append(l.strip())
        else:
            break

    # Skip the header and comment lines
    ls = ls[len(header_ls):]

    data_ls = [l.strip().split() for l in ls if l.strip()]

    # Skip the last size line
    size_l = data_ls.pop(0)

    weights = [float(l[2]) for l in data_ls]
    mn = min(weights) #if min(weights) < 0.0 else 0.0
    mx = max(weights) #if max(weights) > 1.0 else 1.0

    transformed_values = [transform(float(l[2]), mn, mx) for l in data_ls]

    base_name, extension = os.path.splitext(graph_path)
    output_filename = f"{base_name}-trans{extension}"

    with open(output_filename, 'w') as file:
        for l in header_ls:
            file.write(l + '\n')
        file.write(' '.join(size_l) + '\n')
        for i, l in enumerate(data_ls):
            l[2] = str(transformed_values[i])
            file.write(' '.join(l) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mtx_graph_path", help="Path to the graph file.")
    args = parser.parse_args()

    process(args.mtx_graph_path)
