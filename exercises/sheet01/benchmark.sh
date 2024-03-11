#!/bin/bash

# Default values
number_runs="5"
output_file="benchmark_result.json"

# Command line args

while [[ $# -gt 0 ]]; do
    key="$1"
    
    case $key in
        -runs)
            number_runs="$2"
            shift
            shift
        ;;
        -o)
            output_file="$2"
            shift
            shift
        ;;
        -h|--help)
            echo "Usage: $0 [-runs <number_of_runs>] [-o <path_to_output_file>] \"program_to_benchmark_with_args\""
            echo "Example: $0 -runs 10 -o benchmark_result.json \"./delannoy 14\""
            exit 0
        ;;
        -*)
            echo "Unknown option: $1"
            exit 1
        ;;
        *)
            program="$1"
            break
        ;;
    esac
done


# Check if program is given
if [[ -z $1 ]]; then
    echo "Usage: $0 [options] program [program_args...]"
    exit 1
fi





echo "Benchmarking command: \"$program\" with $number_runs runs..."
time_output="/tmp/time_output.tmp"
results=()
for n in $(seq 1 $number_runs); do
    echo "Run $n"
    /usr/bin/time -f "%e;%U;%S;%M" -o $time_output $program
    read time_res < "$time_output"
    results+=("$time_res")
    # echo $time_res
done

collumn_names=("real" "user" "sys" "max_mem")
collumn_units=("s" "s" "s" "kb")

echo "-----"
#cleanup
rm -f $time_output

# calculate mean
sum_real=0
sum_user=0
sum_sys=0
sum_max_mem=0


for result in "${results[@]}"; do
    echo $result
done


echo "Saving results to $output_file"