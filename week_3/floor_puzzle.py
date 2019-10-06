import itertools

floors = [1,2,3,4,5]
for (L, M, N, E, J) in list(itertools.permutations(floors)):
    if (L != 5
        and M != 1
        and N != 1
        and E > M
        and (J-N >= 2 or J - N <= -2) 
        and (N - M >= 2 or N - M <= -2)):
        print(L, M, N, E, J)
