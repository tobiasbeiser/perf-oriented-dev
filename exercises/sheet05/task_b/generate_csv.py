import json
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean


def get_plot_title(json_data, delimiter="_"):
    command_array = json_data["command"].split(" ")
    title = os.path.basename(command_array[0])
    del command_array[0]
    for i in range(len(command_array)):
        if os.path.exists(command_array[i]):
            command_array[i] = os.path.basename(command_array[i])
    args_string = delimiter.join(command_array)
    if args_string != "":
        title = title + delimiter + args_string

    return title


def exctract_results(json_data):
    return str(json_data["mean"]["real"])


def process_files(pattern):
    
    fgcse_after_reload="0"
    fipa_cp_clone="0"
    floop_interchange="0"
    floop_unroll_and_jam="0"
    fpeel_loops="0"
    fpredictive_commoning="0"
    fsplit_loops="0"
    fsplit_paths="0"
    ftree_loop_distribution="0"
    ftree_partial_pre="0"
    funroll_completely_grow_size="0"
    funswitch_loops="0"
    fvect_cost_model=dynamic="0"
    fversion_loops_for_strides="0"
    
    title = ""
    filename_plot = ""
    for filename in sorted(os.listdir()):
        if filename.startswith(pattern) and filename.endswith('.json'):
            try:
                print(f"Processing file '{filename}'")
                with open(filename, "r") as file:
                    json_data = json.load(file)
                    real = exctract_results(json_data)
                    optim = json_data["optimization"]
                    
                    if optim == "-fgcse-after-reload":
                        fgcse_after_reload = real
                    elif optim == "-fipa-cp-clone":
                        fipa_cp_clone = real
                    elif optim == "-floop-interchange":
                        floop_interchange = real
                    elif optim == "-floop-unroll-and-jam":
                        floop_unroll_and_jam = real
                    elif optim == "-fpeel-loops":
                        fpeel_loops = real
                    elif optim == "-fpredictive-commoning":
                        fpredictive_commoning = real
                    elif optim == "-fsplit-loops":
                        fsplit_loops = real
                    elif optim == "-fsplit-paths":
                        fsplit_paths = real
                    elif optim == "-ftree-loop-distribution":
                        ftree_loop_distribution = real
                    elif optim == "-ftree-partial-pre":
                        ftree_partial_pre = real
                    elif optim == "-funroll-completely-grow-size":
                        funroll_completely_grow_size = real
                    elif optim == "-funswitch-loops":
                        funswitch_loops = real
                    elif optim == "-fvect-cost-model=dynamic":
                        fvect_cost_model_dynamic = real
                    elif optim == "-fversion-loops-for-strides":
                        fversion_loops_for_strides = real

                    title = get_plot_title(json_data, delimiter=" ")
                    filename_plot = filename.replace(".json", ".png")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error processing file '{filename}': {e}")
                continue
    csv_string = ';'.join([title,fgcse_after_reload, fipa_cp_clone, floop_interchange, floop_unroll_and_jam, fpeel_loops, fpredictive_commoning, fsplit_loops, fsplit_paths, ftree_loop_distribution, ftree_partial_pre, funroll_completely_grow_size, funswitch_loops, fvect_cost_model_dynamic, fversion_loops_for_strides])
    print(csv_string.replace(".",","))


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <pattern>")
        sys.exit(1)

    pattern = sys.argv[1]
    print(f"Pattern: {pattern}")
    process_files(pattern)


if __name__ == "__main__":
    main()
