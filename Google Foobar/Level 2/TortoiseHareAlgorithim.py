def solution(n, b):
    from numpy import base_repr
    x0 = n
    k = len(n)
    def f(z0,k,b):
        x = "".join(sorted(z0, reverse=True))
        y = "".join(sorted(z0))
        z1 = base_repr( (int(x,b)-int(y,b)), base=b)

        return z1.zfill(k)

    tortoise = f(x0,k,b)
    hare  = f(tortoise,k,b)

    while tortoise != hare:
        tortoise = f(tortoise,k,b)
        hare = f(f(hare,k,b),k,b)

    tortoise = x0
    while tortoise != hare:
        tortoise = f(tortoise,k,b)
        hare = f(hare,k,b)

    lam = 1
    hare = f(tortoise,k,b)
    while tortoise != hare:
        hare = f(hare,k,b)
        lam += 1
    return lam
print(solution(n='210022',b=3))
