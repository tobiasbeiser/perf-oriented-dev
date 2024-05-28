#pragma once
#include "Benchmark.h"
template<typename T>
class ArrayBenchmark : public Benchmark<T>
{
public:
	ArrayBenchmark(int runtime) : Benchmark<T>(runtime) {}
	void runBenchmark(int collectionSize, int readPercentage, int insertPercentage) override;

};