from time import time

def timing(func, inputs=False):
    def func_decorated(*args, **kwargs):
        t0 = time()
        func(*args, **kwargs)
        t1 = time()
        print(f"{func.__name__} - {t1-t0:.3f} s")
        if inputs:
            print(f"args: {args}")
            print(f"kwargs: {kwargs}")
        return func(*args, **kwargs)
    return func_decorated

if __name__== "__main__":
    def fib(n):
        if n <= 2: return 1
        return fib(n-1) + fib(n-2)
    
    @timing
    def fib_calc(n):
        return fib(n)
        
    print(fib_calc(35))
    