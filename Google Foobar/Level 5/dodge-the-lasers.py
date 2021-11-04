#from math import floor,isqrt
def solution(n):
    decimal_digits = len(n)
    n = long(n)
    def newtons_method(n):
        if n == 0:
            return 0
        x0 = 1 << (n.bit_length()//2 + 1)
        x1 = (x0 + n//x0) >> 1
        while( x1 < x0):
            x0 = x1
            x1 = (x0 + n//x0) >> 1
        return x0

    def triangle_number(n):
        return n*(n+1)//2

    def find_B_comp(B_max,decimal_digits):
        precision = 10**(decimal_digits-1)
        beta = newtons_method(2* ( (precision**2 ) )) + 2*precision #Get a good upper bound approx for p
        p_upper = (B_max*precision)//beta+1
        p_lower = (B_max*precision)//(beta+1)
        if p_upper- p_lower > 2 :
            print p_upper,p_lower, p_upper-p_lower
        def bin_search(p_upper,p_lower,B_max):
                #As beatty is mononitcally increasing sequence, we can perform binary search between the bounds
                p = p_lower
                B_2 = newtons_method(2*p**2) +2*p
                while(p_upper-p_lower > 1):
                        p_2 = (p_upper + p_lower)//2
                        B_2 = newtons_method(2*p_2**2) + 2*p_2
                        if B_2 > B_max: #if we overshoot
                            p_upper = p_2
                        else:
                            p_lower = p_2
                return p_lower
        return bin_search(p_upper,p_lower,B_max)
        # B_p = newtons_method(2*p**2) +2*p
        # #print('B max',B_max)
        # while B_p < B_max:
        #     p+= 1
        #     B_p = newtons_method(2*p**2) +2*p #Need to compute (sqrt2 + 2)
        #     print(p)
        # return p-1

    if n <= 0 :
        return

    B_max = newtons_method(2*n**2)
    p = find_B_comp(B_max,decimal_digits)
    S = triangle_number(B_max) -2*triangle_number(p) - long( solution(str(p)) )

    return str(S)
def solution2(n):

    def newtons_method(n):

        return isqrt(n)

    def triangle_number(n):
        return n*(n+1)//2

    def find_B_comp(B_max):
        p = B_max//3 # 3 < 2+ sqrt(2) so is valid inequality
        B_p = newtons_method(2*p**2) +2*p
        #print('B max',B_max)
        while B_p < B_max:
            p+= 1
            B_p = newtons_method(2*p**2) +2*p #Need to compute (sqrt2 + 2)
        return p-1

    if n <= 0 :
        return 0
    #n_sqrt2 = newtons_method(2*n**2)
    B_max = newtons_method(2*n**2)

    p = find_B_comp(B_max)
    #print(p)

    S = triangle_number(B_max) -2*triangle_number(p) - solution(p)

    return S #uses isqrt() for newtons_method

def main():

    # for i in range(60,71):
    #     print(i,solution(i))
    # x = 0
    print(solution('9'*111))
    #for i in range(26):
        #print(i,solution(i)) #Problems after n =26,24 not a problem with newtons_method --> summing or finding B_comp
    # print( isqrt(1000**2*2) )
main()
