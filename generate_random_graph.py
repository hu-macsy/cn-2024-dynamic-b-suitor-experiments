#!/usr/bin/env python3

import networkit as nk
import os
import random

def generate(sc, fc, a, b, c, d, suf):
    input_dir = 'instances'
    os.makedirs(input_dir, exist_ok=True)
    file_name = f"rmat-{suf}.nkb"
    dest_path = os.path.join(input_dir, file_name)

    if os.path.isfile(dest_path):
        print(f"{file_name} already exists.")
        return
    
    G = nk.generators.RmatGenerator(sc, fc, a, b, c, d, True).generate()
    G.removeMultiEdges()
    G.removeSelfLoops()
    nk.graphtools.randomizeWeights(G)
    nk.graphio.NetworkitBinaryWriter().write(G, dest_path)

if __name__ == "__main__":
    sc = 20
    fc = 8
    a_probs = [0.55, 0.45, 0.25]
    b_probs = [0.15, 0.15, 0.25]
    c_probs = [0.15, 0.15, 0.25]
    d_probs = [0.15, 0.25, 0.25]
    suffix = ["b", "g", "er"]

    seed = 1
    nk.setSeed(seed, False)
    random.seed(seed)

    for a, b, c, d, suf in zip(a_probs, b_probs, c_probs, d_probs, suffix):
        generate(sc, fc, a, b, c, d, suf)
