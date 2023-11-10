#include <iostream>

int main()
{
	int primeNumberCount, number, i, j;
	std::cin >> primeNumberCount;
	number = 0;
	while ((primeNumberCount > 0))
	{
		number = (number + 1);
		j = 0;
		i = 1;
		for (; (i <= (number + 1)); i = i + 1)
		{
			if ((((number / i) * i) == number))
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
