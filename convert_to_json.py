#!/usr/bin/env python3

import json
from collections import defaultdict

def parse_file(input_file):
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

    with open(input_file, 'r') as infile:
        current_instance = None
        current_operation = None
        current_b_value = None

        for line in infile:
            if line.startswith("Instance:"):
                current_instance = line.split(":")[1].strip()
            elif line.startswith("operation:"):
                current_operation = line.split(":")[1].strip()
            elif line.startswith("b:"):
                current_b_value = line.split(":")[1].strip()
            elif line.startswith("{"):
                values = [float(value.strip(',')) if '.' in value else int(value) for value in line[1:-2].split(", ")]
                data[current_operation][current_b_value][current_instance]['aff'] = values
            elif line.startswith("avg."):
                key, value = line.split(":")[0].strip(), line.split(":")[1].strip()
                data[current_operation][current_b_value][current_instance][key] = float(value)
            elif line.startswith("static"):
                data[current_operation][current_b_value][current_instance][line.split(":")[0].strip()] = float(line.split(":")[1].strip())

    return data

def write_json(data, output_file):
    with open(output_file, 'w') as outfile:
        json.dump(data, outfile, indent=2)

if __name__ == "__main__":
    input_file_path = "./res_less.txt"
    output_json_path = "./results.json"

    parsed_data = parse_file(input_file_path)
    write_json(parsed_data, output_json_path)
