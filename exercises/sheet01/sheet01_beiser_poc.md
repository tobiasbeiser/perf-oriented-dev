# Perfomance Oriented Computing - 01 - Beiser Tobias
## A) Preparation
### delannoy
Calculates the Delannoy number (Number of paths in a grid from 0,0 to N,N) in a recursive way  
**Parameters:** N  
**How to scale workload:** Increase N  
**Selected Parameters:** 14 as the execution time seems to scale exponentially and this is the last value with an execution time <= 1min

### filegen
Generates N directory with M files in them, with a file size between FS_min and FS_max  
**Parameters:** N, M, FS_min, FS_max  
**How to scale workload:** Increase any of the parameters  
**Selected Parameters:** 1000 100 9000 10000, as this also creates enough directories and folders for filesearch

### filesearch
searches the largest file in a directory, including all subdirectoryies  
**Parameters:** None  
**How to scale workload:** Run Script in a directory with many subdirs/files  
**Selected Parameters:** -

### mmul
Matrix multiplications  
**Parameters:** None  
**How to scale workload:** There is no way to scale the workload without changing the source code  
**Selected Parameters:** -

### nbody
simulation of the n-body problem  
**Parameters:** None  
**How to scale workload:** There is no way to scale the workload without changing the source code  
**Selected Parameters:** -

### qap
solves the Quadratic Assignment Problem for a specified input.  
**Parameters:** Problem file  
**How to scale workload:** larger problems require more computation time  
**Selected Parameters:** chr15a.dat, as the larger problems take more than a minute to solve 

## B) Experiments

