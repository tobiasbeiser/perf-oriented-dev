#include "ArrayBenchmark.h"
#include <iostream>
#include <vector>
#include <memory>

template void ArrayBenchmark<Element8Bytes>::runBenchmark(int collectionSize, int readPercentage, int insertPercentage);
template void ArrayBenchmark<Element512Bytes>::runBenchmark(int collectionSize, int readPercentage, int insertPercentage);
template void ArrayBenchmark<Element8MB>::runBenchmark(int collectionSize, int readPercentage, int insertPercentage);

template<typename T>
void ArrayBenchmark<T>::runBenchmark(int collectionSize, int readPercentage, int insertPercentage)
{
	size_t operations = 0;
	size_t readOperations = 0;
	size_t insertOperations = 0;
	std::vector<T> collection(collectionSize);
	auto end = std::chrono::high_resolution_clock::now() + std::chrono::seconds(this->runtime);
	bool run = true;

	while (run)
	{
		for (int i = 0; i < collectionSize; i++)
		{
			if (std::chrono::high_resolution_clock::now() > end)
			{
				run = false;
				break;
			}
			if (operations % readPercentage == 0) {
				//read
				char data = collection[i].data[0];
				data++;
				//write
				collection[i].data[0] = 0;
				readOperations++;
			}
			if (insertPercentage != 0 && operations % insertPercentage == 0)
			{
				//insert
				T newElement = T();
				collection.push_back(newElement	);

				//delete
				collection.pop_back();
				insertOperations++;
			}

			operations++;
		}
	}
	std::cout << "Array Benchmark:" << std::endl;
	std::cout << "Operations: " << operations << std::endl;
	std::cout << "Read/Write Operations: " << readOperations << std::endl;
	std::cout << "Insert/Delete Operations: " << insertOperations << std::endl;

}