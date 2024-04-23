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


def save_plot(O0, O1, O2, O3, Os, Ofast, title, output_file):

    fig, ax = plt.subplots(figsize=(12, 5))
    fig.suptitle(title)

    data = [O0, O1, O2, O3, Os, Ofast]
    ax.boxplot(data, positions=[1, 2, 3, 4, 5, 6],
               widths=0.6, patch_artist=True)

    ax.set_title('Real')
    ax.set_ylabel('Time in seconds')

    # Round y ticks to 2 decimal places
    ax.set_yticklabels([f'{tick:.2f}' for tick in ax.get_yticks()])
    ax.set_xticklabels(["-O0", "-O1", "-O2", "-O3", "-Os", "-Ofast"])
    plt.savefig(output_file)


def exctract_results(json_data):
    results_real = []
    results_user = []
    results_sys = []
    for run in json_data["runs"]:
        results_real.append(run["real"])
        results_user.append(run["user"])
        results_sys.append(run["sys"])
    return results_real, results_user, results_sys


def process_files(pattern):
    O0, O1, O2, O3, Os, Ofast = [], [], [], [], [], []
    title = ""
    filename_plot = ""
    for filename in sorted(os.listdir()):
        if filename.startswith(pattern) and filename.endswith('.json'):
            try:
                print(f"Processing file '{filename}'")
                with open(filename, "r") as file:
                    json_data = json.load(file)
                    real, user, sys = exctract_results(json_data)
                    optim = json_data["optimization"]
                    if optim == "-O0":
                        O0 = real
                    elif optim == "-O1":
                        O1 = real
                    elif optim == "-O2":
                        O2 = real
                    elif optim == "-O3":
                        O3 = real
                    elif optim == "-Os":
                        Os = real
                    elif optim == "-Ofast":
                        Ofast = real

                    title = get_plot_title(json_data, delimiter=" ")
                    filename_plot = filename.replace(".json", ".png")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error processing file '{filename}': {e}")
                continue
    print("Saving plot to file '{}'".format(filename_plot))
    save_plot(O0, O1, O2, O3, Os, Ofast, title, filename_plot)
    print(title,"\t", round(mean(O0),2),"\t", round(mean(O1),2),"\t", round(mean(O2),2),"\t", round(mean(O3),2),"\t", round(mean(Os),2),"\t", round(mean(Ofast),2))


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <pattern>")
        sys.exit(1)

    pattern = sys.argv[1]
    print(f"Pattern: {pattern}")
    process_files(pattern)


if __name__ == "__main__":
    main()
