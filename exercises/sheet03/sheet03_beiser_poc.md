# Perfomance Oriented Computing - 03 - Beiser Tobias
## A) Traditional profiling
Compile the programs with the -pg flag

~~~bash
mkdir build && cd $_
cmake .. -G Ninja -DCMAKE_CXX_FLAGS=-pg -DCMAKE_EXE_LINKER_FLAGS=-pg -DCMAKE_BUILD_TYPE=Releaes && ninja
~~~

run any program as usual to generate the ```gmon.out``` file and create the gprof report by running ```gprof <program_path> > <output.txt>```

### variant a:

This variant spends significant time in **binvcrhs**, **compute_rhs**, **z_solve**, **y_solve**, and **x_solve** functions, with **binvcrhs** consuming the most time.


Local:
| % | cumulative seconds | self seconds | name |
|---|---|---|---|
| 19.24 | 23.83 | 23.83 | binvcrhs |
| 17.56 | 45.57 | 21.74 | compute_rhs |
| 16.50 | 66.01 | 20.43 | z_solve |
| 16.17 | 86.04 | 20.03 | y_solve |
| 15.40 | 105.11 | 19.07 | x_solve |
| 10.00 | 117.49 | 12.38 | matmul_sub |
| 3.28 | 121.55 | 4.06 | matvec_sub |
 
 LCC3:
 | % | cumulative seconds | self seconds | name |
|---|---|---|---|
| 26.28 | 67.47 | 67.47 | binvcrhs |
| 15.62 | 107.58 | 40.11 | compute_rhs |
| 14.79 | 145.55 | 37.97 | z_solve |
| 14.32 | 182.33 | 36.77 | y_solve |
| 13.16 | 216.11 | 33.78 | x_solve |
| 11.52 | 245.69 | 29.58 | matmul_sub |
| 2.65 | 252.49 | 6.80 | matvec_sub |

### variant b:

Similar to variant a, the distribution of time among functions is similar, with **binvcrhs** consuming the most time.


Local:
| % | cumulative seconds | self seconds | name |
|---|---|---|---|
| 19.26 | 98.69 | 98.69 | binvcrhs |
| 17.47 | 188.19 | 89.50 | compute_rhs |
| 16.75 | 274.02 | 85.83 | z_solve |
| 16.11 | 356.57 | 82.55 | y_solve |
| 15.76 | 437.34 | 80.78 | x_solve |
| 10.00 | 488.56 | 51.21 | matmul_sub |
| 2.99 | 503.87 | 15.31 | matvec_sub |


LCC3:
| % | cumulative seconds | self seconds | name |
|---|---|---|---|
| 25.63 | 270.00 | 270.00 | binvcrhs |
| 15.07 | 428.70 | 158.71 | z_solve |
| 14.98 | 586.49 | 157.78 | compute_rhs |
| 14.28 | 736.86 | 150.37 | y_solve |
| 14.17 | 886.11 | 149.25 | x_solve |
| 11.51 | 1007.36 | 121.25 | matmul_sub |
| 2.90 | 1037.94 | 30.58 | matvec_sub |

### variant s:

This variant spends a considerable amount of time in **x_solve**, followed by **matmul_sub**, **y_solve**, and **z_solve**.

PC:
| % | cumulative seconds | self seconds | name |
|---|---|---|---|
| 29.41 | 0.05 | 0.05 | x_solve |
| 17.65 | 0.08 | 0.03 | matmul_sub |
| 17.65 | 0.11 | 0.03 | y_solve |
| 17.65 | 0.14 | 0.03 | z_solve |
| 11.77 | 0.16 | 0.02 | binvcrhs |
| 5.88 | 0.17 | 0.01 | binvrhs |

LCC3:
| % | cumulative seconds | self seconds | name |
|---|---|---|---|
| 26.47 | 0.09 | 0.09 | binvcrhs |
| 20.59 | 0.16 | 0.07 | compute_rhs |
| 17.65 | 0.22 | 0.06 | y_solve |
| 11.77 | 0.26 | 0.04 | matmul_sub |
| 11.77 | 0.30 | 0.04 | x_solve |
| 8.82 | 0.33 | 0.03 | z_solve |
| 2.94 | 0.34 | 0.01 | lhsinit |

### Interpretation:

The function **binvcrhs** seems to be a critical component across all variants, consuming a significant amount of execution time. Optimizing this function might lead to overall performance improvements. 


