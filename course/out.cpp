#include <iostream>

int main()
{
	long long j;
	for (long long i = 0; (i < 10); i += 1)
	{
		std::cout << i << std::endl;
		j = i;
	}
	long long i;
	i = j;
	std::cout << i << std::endl;
	return 0;
}
