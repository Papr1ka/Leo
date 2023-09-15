from timeit import timeit
import collections

a = """\
import collections
s = collections.deque()
for i in range(1, 10000000):
    s.append(128)
    if (i % 150 == 0):
        for j in range(100):
            s.pop()
"""

b = """\
s = []
for i in range(1, 10000000):
    s.append(128)
    if (i % 150 == 0):
        for j in range(100):
            s.pop()
"""

t1 = timeit(stmt=a, number=1)
t2 = timeit(stmt=b, number=1)

print(t1, t2)
