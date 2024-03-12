# Perfomance Oriented Computing - 01 - Beiser Tobias
## A) Preparation
### delannoy
Calculates the Delannoy number (Number of paths in a grid from 0,0 to N,N) in a recursive way  
**Parameters:** N  
**How to scale workload:** Workload scales exponentially based on N

### filegen
Generates N directory with M files in them, with a file size between FS_min and FS_max  
**Parameters:** N, M, FS_min, FS_max  
**How to scale workload:** Workload scales with all input parameters, likley in linear fashion $O(N*M*\frac{FS_{min}+FS_{max}}{2})$. Since we want to benchmark this program it's best to set FS_min and FS_max to the same values to reduce randomness during our experiments.

### filesearch
searches the largest file in a directory, including all subdirectories  
**Parameters:** None  
**How to scale workload:** The workload scales depending on the number of files/directories. File size should not matter as the file size is determined by POSIX stat.

### mmul
Matrix multiplications  
**Parameters:** None  
**How to scale workload:** There is no way to scale the workload without changing the source code  

### nbody
simulation of the n-body problem  
**Parameters:** None  
**How to scale workload:** There is no way to scale the workload without changing the source code  

### qap
solves the Quadratic Assignment Problem for a specified input.  
**Parameters:** Problem file  
**How to scale workload:** larger problems require more computation time

## B) Experiments
For the LCC3 experiments, the samples were all built on LCC3 with the recommended gcc, cmake and ninja modules loaded from [modules.sh](../../lcc3_helpers/modules.sh)

As for my personal computer:  
**OS:** Ubuntu 20.04.6(WSL2 on Windows 11)  
**CPU:** Intel i7-9700K (8) @ 3.600GHz  
**Memory:** 32GB DDR4 3200MHz  
**Storage:** 1TB M.2 NVME SSD

All experiments were run 5 times to calculate the mean and variance.  



### delannoy
LCC3
|N|real(s)|user(s)|sys(s)|mem(kb)|
|---|---|---|---|---|
|10|0.022 &plusmn; 0.000|0.020 &plusmn; 0.000|0.000 &plusmn; 0.000|1382.400 &plusmn; 279.040|
|11|0.112 &plusmn; 0.000|0.110 &plusmn; 0.000|0.000 &plusmn; 0.000|1343.200 &plusmn; 328.960|
|12|0.630 &plusmn; 0.000|0.620 &plusmn; 0.000|0.000 &plusmn; 0.000|1365.600 &plusmn; 1053.440|
|13|3.378 &plusmn; 0.000|3.372 &plusmn; 0.000|0.000 &plusmn; 0.000|1360.800 &plusmn; 1058.560|
|14|12.324 &plusmn; 0.002|12.300 &plusmn; 0.001|0.000 &plusmn; 0.000|1378.400 &plusmn; 989.440|

PC
|N|real(s)|user(s)|sys(s)|mem(kb)|
|---|---|---|---|---|
|10|0.010 &plusmn; 0.000|0.008 &plusmn; 0.000|0.000 &plusmn; 0.000|1328.800 &plusmn; 2984.960|
|11|0.066 &plusmn; 0.000|0.066 &plusmn; 0.000|0.000 &plusmn; 0.000|1332.000 &plusmn; 2220.800|
|12|0.388 &plusmn; 0.000|0.388 &plusmn; 0.000|0.000 &plusmn; 0.000|1340.000 &plusmn; 1152.000|
|13|2.180 &plusmn; 0.000|2.180 &plusmn; 0.000|0.000 &plusmn; 0.000|1344.000 &plusmn; 12.800|
|14|12.348 &plusmn; 0.024|12.324 &plusmn; 0.019|0.018 &plusmn; 0.000|1322.400 &plusmn; 2282.240|

### filegen
LCC3  
for this benchmark i changed the working dir on lcc3 to the scratch disk with the flag:
~~~bash
#SBATCH --chdir=/scratch/cb761223 
~~~

also, as the scratch disk on lcc3 seems really slow i skipped the 100k experiment for files as to not lock out other students.
|dirs|files|filesize|real(s)|user(s)|sys(s)|mem(kb)|
|---|---|---|---|---|---|---|
|1000|1|1|0.222 &plusmn; 0.065|0.002 &plusmn; 0.000|0.070 &plusmn; 0.002|1480.000 &plusmn; 889.600|
|10000|1|1|4.468 &plusmn; 35.523|0.068 &plusmn; 0.000|0.712 &plusmn; 0.157|1462.400 &plusmn; 3171.840|
|20000|1|1|57.530 &plusmn; 928.999|0.273 &plusmn; 0.000|3.517 &plusmn; 0.023|1469.333 &plusmn; 1518.222|
|100000|1|1|318.757 &plusmn; 32973.192|1.300 &plusmn; 0.037|16.403 &plusmn; 7.991|1494.667 &plusmn; 2232.889|
|1|1000|1|0.167 &plusmn; 0.010|0.003 &plusmn; 0.000|0.053 &plusmn; 0.000|1464.000 &plusmn; 138.667|
|1|10000|1|2.010 &plusmn; 0.639|0.050 &plusmn; 0.000|0.643 &plusmn; 0.031|1440.000 &plusmn; 3530.667|
|1|20000|1|8.350 &plusmn; 4.109|0.143 &plusmn; 0.000|1.453 &plusmn; 0.012|1480.000 &plusmn; 32.000|
|1|1|1000|0.003 &plusmn; 0.000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|1500.000 &plusmn; 714.667|
|1|1|10000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|1476.000 &plusmn; 330.667|
|1|1|20000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|1496.000 &plusmn; 138.667|
|1|1|100000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|1529.333 &plusmn; 3256.889|




PC
|dirs|files|filesize|real(s)|user(s)|sys(s)|mem(kb)|
|---|---|---|---|---|---|---|
|1000|1|1|0.030 &plusmn; 0.000|0.000 &plusmn; 0.000|0.030 &plusmn; 0.000|1529.600 &plusmn; 144.640|
|10000|1|1|0.368 &plusmn; 0.046|0.020 &plusmn; 0.000|0.340 &plusmn; 0.047|1510.400 &plusmn; 1245.440|
|20000|1|1|0.632 &plusmn; 0.044|0.068 &plusmn; 0.001|0.558 &plusmn; 0.047|1555.200 &plusmn; 60.160|
|100000|1|1|3.674 &plusmn; 3.615|0.294 &plusmn; 0.001|3.360 &plusmn; 3.503|1552.800 &plusmn; 2338.560|
|1|1000|1|0.020 &plusmn; 0.000|0.002 &plusmn; 0.000|0.016 &plusmn; 0.000|1531.200 &plusmn; 168.960|
|1|10000|1|0.220 &plusmn; 0.001|0.020 &plusmn; 0.001|0.198 &plusmn; 0.000|1504.000 &plusmn; 480.000|
|1|20000|1|0.456 &plusmn; 0.000|0.036 &plusmn; 0.001|0.410 &plusmn; 0.001|1500.800 &plusmn; 968.960|
|1|100000|1|2.230 &plusmn; 0.027|0.192 &plusmn; 0.001|2.022 &plusmn; 0.021|1507.200 &plusmn; 1096.960|
|1|1|1000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|1531.200 &plusmn; 732.160|
|1|1|10000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|1549.600 &plusmn; 10.240|
|1|1|20000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|1563.200 &plusmn; 591.360|
|1|1|100000|0.002 &plusmn; 0.000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|1645.600 &plusmn; 304.640|










### filesearch
LCC3  
|real(s)|user(s)|sys(s)|mem(kb)|
|---|---|---|---|
|0.008 &plusmn; 0.000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|1408.800 &plusmn; 3522.560|

PC  
|real(s)|user(s)|sys(s)|mem(kb)|
|---|---|---|---|
|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|1545.600 &plusmn; 1424.640|

### mmul
LCC3  
|real(s)|user(s)|sys(s)|mem(kb)|
|---|---|---|---|
|2.036 &plusmn; 0.004|2.024 &plusmn; 0.004|0.000 &plusmn; 0.000|24564.800 &plusmn; 3772.160|

PC
|real(s)|user(s)|sys(s)|mem(kb)|
|---|---|---|---|
|1.400 &plusmn; 0.002|1.396 &plusmn; 0.002|0.002 &plusmn; 0.000|24457.600 &plusmn; 1162.240|

### nbody
LCC3  
|real(s)|user(s)|sys(s)|mem(kb)|
|---|---|---|---|
|2.554 &plusmn; 0.000|2.548 &plusmn; 0.000|0.000 &plusmn; 0.000|1869.600 &plusmn; 477.440|

PC  
|real(s)|user(s)|sys(s)|mem(kb)|
|---|---|---|---|
|0.450 &plusmn; 0.000|0.448 &plusmn; 0.000|0.000 &plusmn; 0.000|1831.200 &plusmn; 2172.160|

### qap
LCC3  
|problem|real(s)|user(s)|sys(s)|mem(kb)|
|---|---|---|---|---|
|chr10a.dat|0.004 &plusmn; 0.000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|1477.600 &plusmn; 669.440|
|chr12a.dat|0.040 &plusmn; 0.000|0.032 &plusmn; 0.000|0.000 &plusmn; 0.000|1509.600 &plusmn; 720.640|
|chr12b.dat|0.036 &plusmn; 0.000|0.030 &plusmn; 0.000|0.000 &plusmn; 0.000|1529.600 &plusmn; 266.240|
|chr12c.dat|0.050 &plusmn; 0.000|0.050 &plusmn; 0.000|0.000 &plusmn; 0.000|1501.600 &plusmn; 29.440|
|chr15b.dat|0.944 &plusmn; 0.000|0.934 &plusmn; 0.000|0.000 &plusmn; 0.000|1477.600 &plusmn; 643.840|
|chr15a.dat|3.494 &plusmn; 0.000|3.482 &plusmn; 0.000|0.000 &plusmn; 0.000|1511.200 &plusmn; 469.760|
|chr15c.dat|3.174 &plusmn; 0.000|3.166 &plusmn; 0.000|0.000 &plusmn; 0.000|1500.000 &plusmn; 1683.200|

PC
|problem|real(s)|user(s)|sys(s)|mem(kb)|
|---|---|---|---|---|
|chr10a.dat|0.002 &plusmn; 0.000|0.000 &plusmn; 0.000|0.000 &plusmn; 0.000|1595.200 &plusmn; 2037.760|
|chr12a.dat|0.022 &plusmn; 0.000|0.022 &plusmn; 0.000|0.000 &plusmn; 0.000|1592.800 &plusmn; 1666.560|
|chr12b.dat|0.010 &plusmn; 0.000|0.010 &plusmn; 0.000|0.000 &plusmn; 0.000|1606.400 &plusmn; 471.040|
|chr12c.dat|0.020 &plusmn; 0.000|0.020 &plusmn; 0.000|0.000 &plusmn; 0.000|1583.200 &plusmn; 770.560|
|chr15a.dat|1.842 &plusmn; 0.001|1.840 &plusmn; 0.001|0.000 &plusmn; 0.000|1585.600 &plusmn; 490.240|
|chr15b.dat|0.480 &plusmn; 0.000|0.478 &plusmn; 0.000|0.000 &plusmn; 0.000|1600.000 &plusmn; 1100.800|
|chr15c.dat|1.684 &plusmn; 0.000|1.682 &plusmn; 0.000|0.000 &plusmn; 0.000|1579.200 &plusmn; 1276.160|