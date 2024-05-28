#pragma once
#include "Elements.h"
#include <chrono>
template<typename T>
class Benchmark
{
public:
	Benchmark(int runtime) : runtime(runtime) {}
	virtual void runBenchmark(int collectionSize, int readPercentage, int insertPercentage) = 0;
	virtual ~Benchmark() = default;

protected:
	int runtime;

};
