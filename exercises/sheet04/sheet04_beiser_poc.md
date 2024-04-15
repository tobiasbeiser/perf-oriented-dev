# Perfomance Oriented Computing - 04 - Beiser Tobias

## A) Memory profiling

### NPB_BT

This program does not seem to do many allocations. The only notable one is done by IO_file_doallocate with arround 8 KiB

Runtime with massif:  
0m3.111s

Runtime without massif:  
0m0.362s

### SSCA2

The largest sources of heap allocation seem to be computeGraph and genScaleData where both seem to allocate arround 4MiB each.

Runtime with massif:  
1m23.996s

Runtime without massif
0m50.391s