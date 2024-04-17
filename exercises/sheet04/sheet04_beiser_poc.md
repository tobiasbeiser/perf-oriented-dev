# Perfomance Oriented Computing - 04 - Beiser Tobias

## A) Memory profiling

### NPB_BT_S

This program does not seem to do many allocations. The only notable one is done by IO_file_doallocate with arround 8 KiB

Runtime without massif:  
0m0.362s

Runtime with massif:  
0m3.111s


### SSCA2

The largest sources of heap allocation seem to be computeGraph and genScaleData where both seem to allocate arround 4MiB each.

Runtime with massif:  
1m23.996s

Runtime without massif  
0m50.391s


## B) Measuring CPU counters

### NPB_BT_S

Runtime without perf:  
0m0.362s

Runtime with perf  
0m0.465s

| Performance Counter         | Relative Metric |
|-----------------------------|-----------------|
| L1-dcache-load-misses       | 10.70%          |
| L1-dcache-loads             | 14.50%          |
| L1-dcache-prefetch-misses   | 14.77%          |
| L1-dcache-prefetches        | 15.04%          |
| L1-dcache-store-misses      | 15.18%          |
| L1-dcache-stores            | 15.08%          |
| L1-icache-load-misses       | 14.81%          |
| L1-icache-loads             | 14.54%          |
| LLC-load-misses             | 14.27%          |
| LLC-loads                   | 14.08%          |
| LLC-prefetch-misses         | 7.04%           |
| LLC-prefetches              | 7.04%           |
| LLC-store-misses            | 7.04%           |
| LLC-stores                  | 7.04%           |
| branch-load-misses          | 10.56%          |
| branch-loads                | 14.08%          |
| dTLB-load-misses            | 14.08%          |
| dTLB-loads                  | 14.08%          |
| dTLB-store-misses           | 14.08%          |
| dTLB-stores                 | 14.08%          |
| iTLB-load-misses            | 14.08%          |
| iTLB-loads                  | 14.08%          |
| node-load-misses            | 14.08%          |
| node-loads                  | 14.08%          |
| node-prefetch-misses        | 7.04%           |
| node-prefetches             | 7.04%           |
| node-store-misses           | 7.04%           |
| node-stores                 | 7.04%           |


### SSCA2

Runtime without perf  
0m50.391s

Runtime with perf  
0m51.183s


| Performance Counter         | Relative Metric |
|-----------------------------|-----------------|
| L1-dcache-load-misses       | 10.71%          |
| L1-dcache-loads             | 14.28%          |
| L1-dcache-prefetch-misses   | 14.28%          |
| L1-dcache-prefetches        | 14.29%          |
| L1-dcache-store-misses      | 14.29%          |
| L1-dcache-stores            | 14.29%          |
| L1-icache-load-misses       | 14.29%          |
| L1-icache-loads             | 14.29%          |
| LLC-load-misses             | 14.29%          |
| LLC-loads                   | 14.29%          |
| LLC-prefetch-misses         | 7.14%           |
| LLC-prefetches              | 7.14%           |
| LLC-store-misses            | 7.14%           |
| LLC-stores                  | 7.14%           |
| branch-load-misses          | 10.72%          |
| branch-loads                | 14.29%          |
| dTLB-load-misses            | 14.29%          |
| dTLB-loads                  | 14.29%          |
| dTLB-store-misses           | 14.29%          |
| dTLB-stores                 | 14.29%          |
| iTLB-load-misses            | 14.29%          |
| iTLB-loads                  | 14.28%          |
| node-load-misses            | 14.28%          |
| node-loads                  | 14.28%          |
| node-prefetch-misses        | 7.14%           |
| node-prefetches             | 7.14%           |
| node-store-misses           | 7.14%           |
| node-stores                 | 7.14%           |


When looking at the full output we can see, that this program performs worse, compared the the first program, as the % for  L1-dcache-load-misses and LLC-load-misses are alot higher than the relativly well optimized first example