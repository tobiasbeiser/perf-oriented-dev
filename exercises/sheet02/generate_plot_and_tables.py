import json
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

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

    return "target/total runs: {}/{} | {}".format(json_data["number_of_runs_target"], json_data["number_of_runs_actual"],title)

def save_plot(real,user,sys, title, output_file):
    
    fig, ax = plt.subplots(1,3, figsize=(12,5))
    fig.suptitle(title)
    ax[0].boxplot(real, 0, 'gD')
    ax[1].boxplot(user, 0, 'gD')
    ax[2].boxplot(sys, 0, 'gD')
    ax[0].set_title('Real')
    ax[1].set_title('User')
    ax[2].set_title('Sys')
    ax[0].set_ylabel('Time in seconds')
    
    # Round y ticks to 2 decimal places
    for axis in ax:
        axis.set_yticklabels([f'{tick:.2f}' for tick in axis.get_yticks()])
    
    plt.savefig(output_file)

def generate_markdown_row(data):
    command_params = data["command"].split()[1:]
    mean = data["mean"]
    variance = data["variance"]
    
    row = "|"
    for param in command_params:
        row += f"{param}|"
    for key in ["real", "user", "sys", "max_mem"]:
        row += f"{mean[key]:.3f} &plusmn; {variance[key]:.3f}|"
    
    return row

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
    markdown_rows = []

    for filename in sorted(os.listdir()):
        if filename.startswith(pattern) and filename.endswith('.json'):
            try:
                print(f"Processing file '{filename}'")
                with open(filename, "r") as file:
                    json_data = json.load(file)
                    markdown_row = generate_markdown_row(json_data)
                    real, user, sys = exctract_results(json_data);
                    title = get_plot_title(json_data, delimiter=" ")
                    # filename = get_plot_title(json_data, delimiter="_")                  
                    save_plot(real, user, sys, title, filename.replace(".json", ".png"))
                    markdown_rows.append(markdown_row)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error processing file '{filename}': {e}")
                continue

    return markdown_rows


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <pattern>")
        sys.exit(1)

    pattern = sys.argv[1]
    print(f"Pattern: {pattern}")
    markdown_rows = process_files(pattern)
    for row in markdown_rows:
        print(row)
        

if __name__ == "__main__":
    main()