#include <iostream>

int main()
{
	long long primeNumberCount, number, j;
	primeNumberCount = 1000;
	number = 0;
	while ((primeNumberCount > 0))
	{
		number = (number + 1);
		j = 0;
		for (long long i = 1; (i <= (number + 1)); i = i + 1)
		{
			if (((number % i) == 0))
			{
				j = (j + 1);
			}
		}
		if ((j == 2))
		{
			primeNumberCount = (primeNumberCount - 1);
			std::cout << number << std::endl;
		}
	}
	return 0;
}
