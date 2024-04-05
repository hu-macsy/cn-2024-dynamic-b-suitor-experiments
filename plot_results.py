#!/usr/bin/env python3

from pylab import rcParams
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
import os
import re
import copy
import matplotlib.ticker as plticker

groups = {}
operations = {}
batch_vals = {}
b_vals = {}

b_vals["1"] = {"affected": [], "runtimes": []}
b_vals["2"] = {"affected": [], "runtimes": []}
b_vals["3"] = {"affected": [], "runtimes": []}
b_vals["random"] = {"affected": [], "runtimes": []}

batch_vals["1"] = copy.deepcopy(b_vals)
batch_vals["10"] = copy.deepcopy(b_vals)
batch_vals["100"] = copy.deepcopy(b_vals)
batch_vals["1000"] = copy.deepcopy(b_vals)

operations["insert"] = copy.deepcopy(batch_vals)
operations["remove"] = copy.deepcopy(batch_vals)

groups["sparse"] = copy.deepcopy(operations)
groups["infrastructure"] = copy.deepcopy(operations)
groups["social"] = copy.deepcopy(operations)
groups["random"] = copy.deepcopy(operations)

graph_groups = {
    "sparse": [
        "human_gene2",
        "mouse_gene",
        "cage14",
        "bone010",
        "cage15"
    ],
    "infrastructure": [
        "belgium",
        "austria",
        "poland",
        "france",
        "africa"
    ],
    "social": [
        "com-youtube",
        "petster-catdog-friend",
        "flickr-growth",
        "soc-LiveJournal1",
        "orkut-links"
    ],
    "random": [
        "rmat-e",
        "rmat-b",
        "rmat-g"
    ]
}


def process(input_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        graph_group = ""
        for line in infile:
            if line.startswith("graph:"):
                graph = re.match(r"graph: (.+)", line).group(1)
                for graph_group_key, graph_group_val in graph_groups.items():
                    if graph in graph_group_val:
                        graph_group = graph_group_key
                # if line.startswith("operation:"):
                line = next(infile).strip()
                operation = re.match(r"operation: ([\w]+)", line).group(1)
                #if line.startswith("b:"):
                line = next(infile).strip()
                b = re.match(r"b: ([\w]+)", line).group(1)
                # if line.startswith("batch size:"):
                line = next(infile).strip()
                batch_size = re.match(r"batch size: ([\w]+)", line).group(1)
                # if line.startswith("aff:"):
                line = next(infile).strip()
                aff = re.match(r"aff: {([^}]+)}", line).group(1)
                affected = [int(i) for i in aff.split(',')]
                # if line.startswith("runtimes:"):
                line = next(infile).strip()
                run = re.match(r"runtimes: {([^}]+)}", line).group(1)
                runtimes = [float(i) for i in run.split(',')]
                line = next(infile).strip()
                static_run = re.match(r"static runtime: (\w+[.?]\w+)", line).group(1)

                groups[graph_group][operation][batch_size][b]["static runtime"] = static_run
                groups[graph_group][operation][batch_size][b]["affected"].extend(affected)
                groups[graph_group][operation][batch_size][b]["runtimes"].extend(runtimes)

def plot():
    for group_key, group_val in groups.items():
        for op_key, op_val in group_val.items():
            for batch_key, batch_val in op_val.items():
                com_affected = []
                com_runtime = []
                com_b = []

                for b in list(batch_val.keys()):
                    affected2 = batch_val[b]["affected"]
                    runtimes2 = batch_val[b]["runtimes"]
                    b2 = [b]*len(affected2)
                    com_affected.extend(affected2)
                    
                    stat = batch_val[b]["static runtime"]
                    for i,r in enumerate(runtimes2):
                        runtimes2[i] = float(stat) / r

                    com_runtime.extend(runtimes2)
                    com_b.extend(b2)  

                # print(com_runtime)
                # for i,r in enumerate(com_runtime):
                #     com_runtime[i] = com_stat / r
                # print(com_runtime)

                sns.set_theme(style="whitegrid")
                sns.violinplot(x=com_b, y=pd.to_numeric(com_affected), bw=1.2, inner=None, linewidth=2, cut=0, density_norm="count") # , log_scale=(False, True)
                # plt.title(f"{group_key} + {op_key} + {batch_key}")
                plt.xlabel('b', fontsize=25)
                plt.ylabel('aff. vertices', fontsize=25)
                plt.xticks(fontsize=20)
                plt.yticks(plt.yticks()[0][::2], fontsize=20)
                plt.ylim(bottom=0)
                # plt.yscale("log")
                plt.tight_layout()
                loc = plticker.MultipleLocator(base=1.0)
                # plt.axes.set_major_locator(loc)
                # plt.rcParams["set_major_locator"]
                # ax.set_xticks(ax.get_xticks()[::2])

                img_name = f"figures/affected/{group_key}_{op_key}_{batch_key}.png"
                plt.savefig(img_name, bbox_inches='tight')
                # plt.show()
                plt.close()


                sns.set_theme(style="whitegrid")
                sns.violinplot(x=com_b, y=pd.to_numeric(com_runtime), bw=1.2, inner=None, linewidth=2, cut=0, density_norm="count") # , log_scale=(False, True)
                # plt.title(f"{group_key} + {op_key} + {batch_key}")
                plt.xlabel('b', fontsize=25)
                plt.ylabel('speedup', fontsize=25)
                plt.xticks(fontsize=20)
                # plt.yticks(fontsize=20)
                plt.yscale("log")
                plt.tight_layout()
                plt.ylim((10e-4,10e6))
                plt.yticks(ticks=[10e-2,10e0,10e2,10e4,10e6], fontsize=20)
                # plt.ylim([10e2,10e44,10e6,10e8]) #bottom=10e2, top=10e8) # (10e2,10e7)
                # plt.yticks(plt.yticks()[0][::2], fontsize=20)

                img_name = f"figures/speedup/{group_key}_{op_key}_{batch_key}.png"
                # plt.savefig(img_name, bbox_inches='tight')
                # plt.show()
                plt.close()

if __name__ == "__main__":
    input_file_path = "./res_less.txt"

    if os.path.exists(input_file_path):
        process(input_file_path)
        plot()