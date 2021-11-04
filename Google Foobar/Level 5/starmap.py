from math import factorial
from numpy import lcm

def solution2(w,h,s):
    def partition(n):
        a = [0 for i in range(n + 1)]
        k = 1
        a[1] = n
        while k != 0:
            x = a[k - 1] + 1
            y = a[k] - 1
            k -= 1
            while x <= y:
                a[k] = x
                y -= x
                k += 1
            a[k] = x + y
            yield a[:k + 1]
    def get_Cycle_index(n):
        n_p = []
        coeff = {}
        for i in partition(n):

            count = [ (cycle, i.count(cycle)) for cycle in set(i)]
            coeff = factorial(n)//prod([ (k**jk)*factorial(jk) for k,jk in count])
            n_p.append((i,coeff))
        return n_p

    w_p= get_Cycle_index(w)
    h_p= get_Cycle_index(h)
    a_list = []

    #Calculate the number of each term


    #Form a list of dicts where each dict contains a cycle index of S_w X S_h
    #Key is the cycle length, value is the power/# of occurances of the cycle
    for per_w, num_w in w_p:
        for per_h, num_h in h_p:
            a={lcm(i,j) : 0 for i in set(per_w) for j in set(per_h)}
            for i in per_w:
                for j in per_h:
                    a[lcm(i,j)] += (i*j)//lcm(i,j)


            a_list.append((a,num_w*num_h))

    G = factorial(w)*factorial(h)
    N = 0
    for cycles,coeff in a_list:
        power =  sum([jk for jk in cycles.values()])
        N += coeff*s**power

    return N//G

def solution(w,h,s):
    from math import factorial
    from fractions import gcd
    from functools import reduce

    #Generate Cycle index polynomial for n objects. Uses integer partition to generate the cycles
    #Returns a list of tuples (partition(i),permutation count(partition(i)))
    def Cycle_index(n):
        #Generate the all integer partition of n in ascending order
        #Gives us the equivalence classes of permutations
        def partition(n):
            if n == 1:
                yield [1]
                return
            for p in partition(n-1):
                yield [1] + p
                if p and ( len(p) < 2 or p[1] > p[0]) :
                    p[0] += 1
                    yield p

        #Count how many permutations belong to an equivalence class/partition p
        def count_permutations(p):
        #returns n!/Product(k^jk * jk!) counts the number of times the equivalence class for a partition/permutation i occurs with len(i)
            count = [ (cycle, p.count(cycle)) for cycle in set(p)]
            return factorial(n)//reduce(lambda x,y: x*y,[ (k**jk)*factorial(jk) for k,jk in count])

        #Store the partition and then the number of permutations that are equivalent to that partition
        return [(p,count_permutations(p)) for p in partition(n)]
    # Get the Cycle Index polynomial of S_h x S_w
    def MatrixMonomial(per_w, per_h):
        def lcm(a,b):
            return a*b//gcd(a,b)
        #Generate all the unique monomial sequences for this pair of permutations
        #Store as a dict where key = cycle length, value = # of occurances of cycle length
        monomial={lcm(i,j) : 0 for i in set(per_w) for j in set(per_h)}
        for i in per_w:
            for j in per_h:
                # gcd(i,j) = i*j/lcm(i,j) cycle lcm(i.j) forms a subgroup of orbits on the i*j elements
                # so there must be gcd(i,j) # of lcm(i,j) cycles
                monomial[lcm(i,j)] += gcd(i,j)
        return monomial

    #Loop through each unique partitions of w and h and get the MatrixMonomial and count
    a_list = [
    ( MatrixMonomial(per_w,per_h) ,num_w*num_h )
    for per_w, num_w in Cycle_index(w)
    for per_h, num_h in Cycle_index(h)
    ]

    G = factorial(w)*factorial(h)
    #To count the states, we first sum up the number of cycle lengths in a permutation
    N = sum( [num_cycles*pow(s, sum(cycles.values()) )  for cycles,num_cycles in a_list] )//G
    return str(N)



def main():
    print(solution(2,3,4))
    #print(len([i for i in partition(30)]))




main()
