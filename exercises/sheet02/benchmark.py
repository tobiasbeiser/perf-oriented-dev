import statistics
import subprocess
import sys
import json
import argparse
import socket
import math
import os


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
    
    
    if socket.gethostname() == "login.lcc3.uibk.ac.at" and False: # Currently not working when using subprocess
        lcc3_benchmark = ["sbatch", "--partition=lva", "--job-name={}".format(job_name), "--output=/dev/null" if quiet_mode else "--output=output.log", "--error=/dev/null" if quiet_mode else "--error=error.log", "--ntasks=1", "--ntasks-per-node=1", "--exclusive", "-W", "--wrap='{}'".format(" ".join(program_benchmark))]
        if DEBUG:
            print("Run {}: {}".format(job_name, " ".join(lcc3_benchmark)))
        process = subprocess.Popen(
            lcc3_benchmark, stdout=subprocess.PIPE)        
    else:
        if DEBUG:
            print("Run {}: {}".format(job_name, " ".join(program_benchmark)))
        process = subprocess.Popen(
            program_benchmark, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL if quiet_mode else subprocess.PIPE)

    _, stderr = process.communicate()
    time_res = stderr.decode('ascii')
    arr_result = time_res.split(';')
    benchmark_result = BenchmarkResult(float(arr_result[0]), float(
    arr_result[1]), float(arr_result[2]), float(arr_result[3]))
    return benchmark_result


def calculate_mean_variance(measurements):
    mean = statistics.mean(measurements)
    variance = statistics.variance(measurements)
    return mean, variance


def calculate_confidence_interval(mean, variance, n):
    standard_error = math.sqrt(variance/n)
    z_value = 1.96  # For 95% confidence level (standard normal distribution)
    margin_of_error = z_value * standard_error

    lower_bound = mean - margin_of_error
    upper_bound = mean + margin_of_error

    return lower_bound, upper_bound


def measurement_stable(measurements):
    mean, variance = calculate_mean_variance(measurements)
    confidence_interval = calculate_confidence_interval(mean, variance, len(measurements))
    if confidence_interval[0] <= measurements[-1]  <= confidence_interval[1]:
        return True
    else:
        return False


def check_if_mean_variance_stable(results):
    if len(results) < 2:
        return False

    real = []
    user = []
    sys = []
    max_mem = []
    for result in results:
        real.append(result.real)
        user.append(result.user)
        sys.append(result.sys)
        max_mem.append(result.max_mem)

    if measurement_stable(real) and measurement_stable(user) and measurement_stable(sys) and measurement_stable(max_mem):
        print("Mean and variance are stable.")
        return True
    else:
        mean_real, variance_real = calculate_mean_variance(real[:-1])
        mean_user, variance_user = calculate_mean_variance(user[:-1])
        mean_sys, variance_sys = calculate_mean_variance(sys[:-1])
        mean_max_mem, variance_max_mem = calculate_mean_variance(max_mem[:-1])
        ci_real = calculate_confidence_interval(mean_real, variance_real, len(real))
        ci_user = calculate_confidence_interval(mean_user, variance_user, len(user))
        ci_sys = calculate_confidence_interval(mean_sys, variance_sys, len(sys))
        ci_max_mem = calculate_confidence_interval(mean_max_mem, variance_max_mem, len(max_mem))
        print("real: {}({}-{}), user: {}({}-{}), sys: {}({}-{}), max_mem: {}({}-{})".format(results[-1].real, round(ci_real[0],2), round(ci_real[1],2), results[-1].user, round(ci_user[0],2), round(ci_user[1],2), results[-1].sys, round(ci_sys[0],2), round(ci_sys[1],2), results[-1].max_mem, round(ci_max_mem[0],2), round(ci_max_mem[1],2)))
        # print("Mean({}) and variance({}) are not stable. Increasing number of runs ({} total).".format(round(mean,2), round(variance,2) ,len(results)+1))
        return False


def experiment(number_runs, number_runs_max, program_name, program, quiet_mode):
    results = []
    json_output = {"command": program,
                   "number_of_runs_target": number_runs,"number_of_runs_actual":0, "runs": []}
    n = 1
    while True:
        job_name = program_name + "_run_{}".format(n)
        benchmark_result = measure_program(program, job_name,quiet_mode)
        results.append(benchmark_result)
        json_output["runs"].append(
            get_json_from_benchmark_result(benchmark_result))
        if n >= number_runs_max:
            print("Maximum number of runs reached.")
            json_output["number_of_runs_actual"] = n
            break
        if (number_runs) <= n and check_if_mean_variance_stable(results):
            json_output["number_of_runs_actual"] = n
            break
        n += 1

    return results, json_output


def main():
    # Default values
    number_runs = 5
    number_runs_max = 50
    confidence_level = 0.90
    output_file = "benchmark_result.json"
    lcc3 = False
    quiet_mode = False
    # Command line args
    parser = argparse.ArgumentParser(
        description="Script for benchmarking programs.")
    parser.add_argument("-runs", type=int, help="Number of runs")
    parser.add_argument("-runs-max", type=int, help="Maximum number of runs")
    parser.add_argument("-o", help="Output file path")
    parser.add_argument("-q", action="store_true", help="Quiet mode")
    parser.add_argument("program", nargs='+', help="Program to benchmark with arguments")
    args = parser.parse_args()

    if args.runs:
        number_runs = args.runs
    if args.o:
        output_file = args.o
    if args.q:
        quiet_mode = True
    if args.runs_max:
        number_runs_max = args.runs_max
    program = ' '.join(args.program)

    # Check if program is given
    if not program:
        print("Usage: {} [options] program [program_args...]".format(
            sys.argv[0]))
        sys.exit(1)

    print("Benchmarking command: '{}' with {} runs{}...".format(
        program, number_runs, " on LCC3" if lcc3 else ""))

    program_name = get_program_name(program)
    program_name_pretty = get_program_name(program, " ")

    results, json_output = experiment(number_runs, number_runs_max, program_name, program, quiet_mode)

    real = []
    user = []
    sys = []
    max_mem = []
    for result in results:
        real.append(result.real)
        user.append(result.user)
        sys.append(result.sys)
        max_mem.append(result.max_mem)

    real_mean, real_variance = calculate_mean_variance(real)
    user_mean, user_variance = calculate_mean_variance(user)
    sys_mean, sys_variance = calculate_mean_variance(sys)
    max_mem_mean, max_mem_variance = calculate_mean_variance(max_mem)
    
    json_output["mean"] = {"real": round(real_mean, 4), "user": round(
        user_mean, 4), "sys": round(sys_mean, 4), "max_mem": round(max_mem_mean, 4)}
    json_output["variance"] = {"real": round(real_variance, 4), "user": round(
        user_variance, 4), "sys": round(sys_variance, 4), "max_mem": round(max_mem_variance, 4)}

    print("Saving results to", output_file)

    # Save results to output file
    with open(output_file, 'w') as f:
        json.dump(json_output, f, indent=4)


if __name__ == "__main__":
    main()