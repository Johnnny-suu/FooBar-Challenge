from itertools import combinations
def solution(num_buns, num_required):
    copies = num_buns - num_required + 1
    keys_dist = [[] for _ in range(num_buns)]
    #We don't want any num_required tuple to contain all the copies of 2 or more keys.
    #At most we only want a tuple to have only have all the copies of at most one key
    for key,bs in enumerate(combinations(range(num_buns),copies)):
        for b in bs:
            keys_dist[b].append(key)
def main():
    solution(10,4)

main()
