from time import time


def main():
    primeNumberCount: int
    number: int
    j: int

    primeNumberCount = 1000
    number = 0

    while (primeNumberCount > 0):
        number = (number + 1)
        j = 0

        for i in range(1, (number + 1), 1):

            if (number % i == 0):
                j = (j + 1)

        if (j == 2):
            primeNumberCount = (primeNumberCount - 1)
            print(number)


def primes():
    primeNumberCount = 1000
    number = 0
    while primeNumberCount > 0:
        number += 1
        j = 0
        for i in range(1, number + 1):
            if number % i == 0:
                j += 1

        if j == 2:
            primeNumberCount -= 1
            print(number)


if __name__ == '__main__':
    times = []
    n = 25
    for i in range(10):
        t0 = time()
        main()
        t1 = time()
        t = t1 - t0
        times.append(t)

    avg1 = sum(times) / len(times)

    times = []
    for i in range(10):
        t0 = time()
        primes()
        t1 = time()
        t = t1 - t0
        times.append(t)

    avg2 = sum(times) / len(times)
    print(f"Leo, 1000 чисел, среднее по {n} измерениям ", avg1)
    print(f"Python, 1000 чисел, среднее по {n} измерениям ", avg2)
    print("Leo / Python =", avg1 / avg2)
