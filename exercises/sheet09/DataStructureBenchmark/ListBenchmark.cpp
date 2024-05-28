#include "ListBenchmark.h"
#include <iostream>
#include <forward_list>

template void ListBenchmark<Element8Bytes>::runBenchmark(int collectionSize, int readPercentage, int insertPercentage);
template void ListBenchmark<Element512Bytes>::runBenchmark(int collectionSize, int readPercentage, int insertPercentage);
template void ListBenchmark<Element8MB>::runBenchmark(int collectionSize, int readPercentage, int insertPercentage);

template<typename T>
void ListBenchmark<T>::runBenchmark(int collectionSize, int readPercentage, int insertPercentage)
{
	size_t operations = 0;
	size_t readOperations = 0;
	size_t insertOperations = 0;
	std::forward_list<T> collection(collectionSize);
	auto end = std::chrono::high_resolution_clock::now() + std::chrono::seconds(this->runtime);
	bool run = true;

	while (run)
	{
		for (typename std::forward_list<T>::iterator it = collection.begin(); it != collection.end(); ++it) 
		{
			if (std::chrono::high_resolution_clock::now() > end)
			{
				run = false;
				break;
			}
			if (operations % readPercentage == 0)
			{
				//read
				char data = (*it).data[0];
				data++;
				//write
				(*it).data[0] = 0;
				readOperations++;
			}
			if (insertPercentage != 0 && operations % insertPercentage == 0)
			{
				//insert
				T newElement = T();
				collection.push_front(newElement);
				//delete
				collection.pop_front();
				insertOperations++;
			}
			operations++;
		}

	}
	std::cout << "List Benchmark: " << std::endl;
	std::cout << "Operations: " << operations << std::endl;
	std::cout << "Read/Write Operations: " << readOperations << std::endl;
	std::cout << "Insert/Delete Operations: " << insertOperations << std::endl;
}
