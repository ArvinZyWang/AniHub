import time

def timer(func):
    
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'Function <{func.__name__}> takes {end - start} seconds to finish.')
        return result
    
    return inner