import statistics
import subprocess
import sys
import json
import argparse
import socket
import math
import os
import shutil
import time


DEBUG = False

class BenchmarkResult:
    def __init__(self, real, user, sys, max_mem):
        self.real = real
        self.user = user
        self.sys = sys
        self.max_mem = max_mem


def get_program_name(program, delimiter="_"):
    job_name_arr = program.split(" ")
    program_name = os.path.basename(job_name_arr[0])
    del job_name_arr[0]
    for i in range(len(job_name_arr)):
        if os.path.exists(job_name_arr[i]):
            job_name_arr[i] = os.path.basename(job_name_arr[i])
    args_string = "_".join(job_name_arr)
    if args_string != "":
        program_name = program_name + delimiter + args_string

    return program_name



def get_json_from_benchmark_result(benchmark_result):
    return {"real": float(benchmark_result.real), "user": float(benchmark_result.user), "sys": float(benchmark_result.sys), "max_mem": float(benchmark_result.max_mem)}


def measure_program(program, job_name,quiet_mode):
    temp_output_path = os.path.abspath("./{}.tmp".format(job_name))
    program_parts = program.split(" ")
    executable = program_parts[0]
    arguments = program_parts[1:]
    # program_benchmark = ["/usr/bin/time", "-f", "%e;%U;%S;%M", "-o", temp_output_path, executable] + arguments
    program_benchmark = ["/usr/bin/time", "-f", "%e;%U;%S;%M", executable] + arguments
    output_file = "{}.log".format(job_name)
    job_script="""#!/bin/bash
# Execute job in the partition "lva" unless you have special requirements.
#SBATCH --partition=lva
# Name your job to be able to identify it later
#SBATCH --job-name {job_name}
# Redirect output stream to this file
#SBATCH --output={output_file}
# Maximum number of tasks (=processes) to start in total
#SBATCH --ntasks=1
# Maximum number of tasks (=processes) to start per node
#SBATCH --ntasks-per-node=1
# Enforce exclusive node allocation, do not share with other jobs
#SBATCH --exclusive

/usr/bin/time -f '%e;%U;%S;%M' {program}""".format(job_name=job_name, output_file=output_file,program=program, arguments=" ".join(arguments))
        
        
    job_file="{}.sh".format(job_name)
    f = open(job_file, "w")
    f.write(job_script)
    f.close()
    
    lcc3_benchmark = "sbatch -W {}".format(os.path.abspath(job_file))
    process = subprocess.run(lcc3_benchmark, shell=True, stdout=subprocess.DEVNULL)        

    
    while not os.path.exists(output_file):
        time.sleep(1)    
        
    time_res = open(output_file, "r").readlines()[-1]
    arr_result = time_res.split(';')
    os.remove(output_file)
    os.remove(job_file)
    benchmark_result = BenchmarkResult(float(arr_result[0]), float(
    arr_result[1]), float(arr_result[2]), float(arr_result[3]))
    return benchmark_result



def experiment(program_name, program, quiet_mode):
    results = []
    json_output = {"command": program}

    benchmark_result = measure_program(program, program_name,quiet_mode)
    json_output["results"]=get_json_from_benchmark_result(benchmark_result)
    
    return json_output


def main():
    # Default values
    output_file = "benchmark_result.json"
    lcc3 = False
    quiet_mode = False
    # Command line args
    parser = argparse.ArgumentParser(
        description="Script for benchmarking programs.")
    parser.add_argument("-o", help="Output file path")
    parser.add_argument("-q", action="store_true", help="Quiet mode")
    parser.add_argument("program", nargs='+', help="Program to benchmark with arguments")
    args = parser.parse_args()

    program = ' '.join(args.program)
    # Check if program is given
    if not program:
        print("Usage: {} [options] program [program_args...]".format(
            sys.argv[0]))
        sys.exit(1)

    print("Benchmarking command: '{}' {}...".format(
        program, " on LCC3" if lcc3 else ""))

    program_name = get_program_name(program)
    program_name_pretty = get_program_name(program, " ")

    if args.o:
        output_file = args.o
    else:
        output_file="benchmark_results_{}.json".format(program_name)
    if args.q:
        quiet_mode = True
    



    values = ["1", "8", "32", "64", "256", "1024", "4096"]
    
    for height in values:
        for width in values:
            print("Benchmarking with HEIGHT/WIDTH:", height, width)
            program_w_h = program + " " + str(height) + " " + str(width)
            
            json_output = experiment(program_name, program_w_h, quiet_mode)
            
            json_output["width"]=width
            json_output["height"]=height
            output_file_tile=output_file.replace('.json', "_H{}_W{}".format(height, width))+'.json'
            
            print("Saving results to", output_file_tile)

            # Save results to output file
            with open(output_file_tile, 'w') as f:
                json.dump(json_output, f, indent=4)


if __name__ == "__main__":
    main()