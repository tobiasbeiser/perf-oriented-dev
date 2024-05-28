#pragma once
#include "Benchmark.h"
template<typename T>
class ListBenchmark : public Benchmark<T>
{
public:
	ListBenchmark(int runtime) : Benchmark<T>(runtime) {}
	void runBenchmark(int collectionSize, int readPercentage, int insertPercentage) override;
};