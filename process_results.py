#!/usr/bin/env python3

import os
import re

def remove_warn_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            affected_nodes_values = []
            runtimes_values = []
            if line.startswith("(Dynamic) affected nodes per run:"):
                for _ in range(50):
                    next_line = next(infile).strip()
                    if next_line:
                        value = int(next_line)
                        affected_nodes_values.append(value)
                avg_affected_nodes = sum(affected_nodes_values) / len(affected_nodes_values)
                # outfile.write(f"avg. aff.: {avg_affected_nodes}\n")
                outfile.write(f"aff: {{{', '.join(map(str, affected_nodes_values))}}}\n")
            elif line.startswith("(Dynamic) runtimes [s] per run:"):
                for _ in range(50):
                    next_line = next(infile).strip()
                    if next_line:
                        value = float(next_line)
                        runtimes_values.append(value)
                avg_runtime = sum(runtimes_values) / len(runtimes_values)
                # outfile.write(f"avg. runtime: {avg_runtime}\n")
                outfile.write(f"runtimes: {{{', '.join(map(str, runtimes_values))}}}\n")
            elif line.startswith("Start comparison"):
                match = re.match(r"Start comparison for the dynamic ([\w]+)-matching: ([\w]+) ([\d]+) edge(?:s)? (?:into|from) the graph located at (?:[^\s]+)/([^\s]+)\.(?:[^\s]+) with ([\d]+) nodes and ([\d]+) edges.", line)
                if match:
                    b_value = match.group(1)
                    operation = match.group(2)
                    batch_size = match.group(3)
                    graph = match.group(4)
                    nodes = match.group(5)
                    edges = match.group(6)
                    outfile.write(f"graph: {graph}\n")
                    outfile.write(f"operation: {operation}\n")
                    outfile.write(f"b: {b_value}\n")
                    outfile.write(f"batch size: {batch_size}\n")
                    # outfile.write(f"nodes: {nodes}\n")
                    # outfile.write(f"edges: {edges}\n")
                else:
                    None
                    # outfile.write(line)
            elif line.startswith("Average degree:"):
                line = next(infile).strip()
                # outfile.write(f"avg. deg: {next(infile).strip()}\n")
            elif line.startswith("(Static) runtimes [s] per run:"):
                None
                outfile.write(f"static runtime: {next(infile).strip()}\n\n")
            elif line.startswith("Experiment: dynamic-b-suitor"):
                outfile.write(f"\n")
            elif not (line.startswith("[WARN") or line.startswith("Experiment: dynamic-b-suitor") or line.startswith("Output:") or line.startswith("Error Output:") or line.isspace()):
                outfile.write(line)

if __name__ == "__main__":
    input_file_path = "./results.txt"
    output_file_path = "./res_less.txt"

    if os.path.exists(input_file_path):
        remove_warn_lines(input_file_path, output_file_path)
