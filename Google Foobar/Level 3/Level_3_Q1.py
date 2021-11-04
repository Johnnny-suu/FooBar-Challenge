import timeit
def solution2(n):
    count = 0
    n = int(n)
    while(n > 1):
        if n % 2 == 0:
            n = n >> 1
        elif n==3 or (((n&3)^3) >> 1) == 1:
            n = n-1
        else:
            n=n+1
        count = count + 1
    return (count)
def solution(n):
    count = 0
    n = int(n)
    while(n > 1):
        if n % 2 == 0:
            n = n >> 1
        elif n ==3 or n % 4 == 1:
            n = n-1
        else:
            n=n+1
        count = count + 1
    return (count)

starttime = timeit.default_timer()
print("The start time is :",starttime)

for i in range(1000000):
    solution(str(i))

print("The time difference is :", timeit.default_timer() - starttime)
starttime = timeit.default_timer()
print("The start time is :",starttime)

for i in range(1000000):
    solution2(str(i))

print("The time difference is :", timeit.default_timer() - starttime)
