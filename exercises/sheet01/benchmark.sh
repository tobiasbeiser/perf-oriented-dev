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

echo "-----"
#cleanup
rm -f $time_output

# calculate mean
sum_real=0
sum_user=0
sum_sys=0
sum_max_mem=0

json_output="{\"command\": \"$program\", \"number_of_runs\": $number_runs, \"runs\": ["
for result in "${results[@]}"; do
    arr_result=(${result//;/ })
    sum_real=$(echo "$sum_real ${arr_result[0]}" | awk '{printf "%.3f", $1 + $2}')
    sum_user=$(echo "$sum_user ${arr_result[1]}" | awk '{printf "%.3f", $1 + $2}')
    sum_sys=$(echo "$sum_sys ${arr_result[2]}" | awk '{printf "%.3f", $1 + $2}')
    sum_max_mem=$(echo "$sum_max_mem ${arr_result[3]}" | awk '{printf "%.3f", $1 + $2}')
    json_output="$json_output{\"real\": ${arr_result[0]}, \"user\": ${arr_result[1]}, \"sys\": ${arr_result[2]}, \"max_mem\": ${arr_result[3]}},"
done
json_output="${json_output::-1}]"
echo "Sum: $sum_real s (real), $sum_user s (user), $sum_sys s (sys), $sum_max_mem kb (max mem)"

mean_real=$(echo "$sum_real $number_runs" |awk '{printf "%.3f", $1 / $2}')
mean_user=$(echo "$sum_user $number_runs" |awk '{printf "%.3f", $1 / $2}')
mean_sys=$(echo "$sum_sys $number_runs" |awk '{printf "%.3f", $1 / $2}')
mean_max_mem=$(echo "$sum_max_mem $number_runs" |awk '{printf "%.3f", $1 / $2}')

json_output="$json_output, \"mean\": {\"real\": $mean_real, \"user\": $mean_user, \"sys\": $mean_sys, \"max_mem\": $mean_max_mem}"

echo "Mean: $mean_real s (real), $mean_user s (user), $mean_sys s (sys), $mean_max_mem kb (max mem)"

variance_sum_real=0
variance_sum_user=0
variance_sum_sys=0
variance_sum_max_mem=0

for result in "${results[@]}"; do
    arr_result=(${result//;/ })
    variance_sum_real=$(echo "$variance_sum_real ${arr_result[0]} $mean_real" | awk '{printf "%.3f", $1 + ($2 - $3)^2}')
    variance_sum_user=$(echo "$variance_sum_user ${arr_result[1]} $mean_user" | awk '{printf "%.3f", $1 + ($2 - $3)^2}')
    variance_sum_sys=$(echo "$variance_sum_sys ${arr_result[2]} $mean_sys" | awk '{printf "%.3f", $1 + ($2 - $3)^2}')
    variance_sum_max_mem=$(echo "$variance_sum_max_mem ${arr_result[3]} $mean_max_mem" | awk '{printf "%.3f", $1 + ($2 - $3)^2}')
done

variance_real=$(echo "$variance_sum_real $number_runs" |awk '{printf "%.3f", $1 / $2}')
variance_user=$(echo "$variance_sum_user $number_runs" |awk '{printf "%.3f", $1 / $2}')
variance_sys=$(echo "$variance_sum_sys $number_runs" |awk '{printf "%.3f", $1 / $2}')
variance_max_mem=$(echo "$variance_sum_max_mem $number_runs" |awk '{printf "%.3f", $1 / $2}')

json_output="$json_output, \"variance\": {\"real\": $variance_real, \"user\": $variance_user, \"sys\": $variance_sys, \"max_mem\": $variance_max_mem}"

echo "Variance: $variance_real s (real), $variance_user s (user), $variance_sys s (sys), $variance_max_mem kb (max mem)"

echo "Saving results to $output_file"

rm -f $output_file
json_output="$json_output}"
echo $json_output >> $output_file

