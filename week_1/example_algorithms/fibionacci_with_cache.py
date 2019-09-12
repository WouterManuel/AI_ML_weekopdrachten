fibo_cache = {} 

def fibonacci(n): 
    # if we have the value in cache, return it
    if n in fibo_cache: 
        return fibo_cache[n]
    
    # else compute value
    if n in (0, 1):
        return n
    value = fibonacci(n-1) + fibonacci(n-2)

    # store value in cache and return value
    fibo_cache[n] = value
    return value

for n in range(1, 10): 
    print(n, ':', fibonacci(n))


"""
nu met decorator functie
"""

def memorize(f):
    memo = {}
    # definining function wrapper
    def helper(x):
        print('a')
        if x not in memo:
            memo[x] = f(x)
            print(f(x), " added")
        return memo[x]
    return helper

@memorize
def fibonacci_1(n):
    if n in (0, 1):
            return n
    return fibonacci_1(n-1) + fibonacci_1(n-2)

for n in range(1, 10): 
    print(n, ':', fibonacci_1(n))
