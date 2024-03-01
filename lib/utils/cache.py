import functools
import time

def cache(enable = True, timeout = 300):
    """
    自定义缓存装饰器，支持设置缓存超时时间（默认为300秒）
    """
    def decorator(func):
        cache_dict = {}  # 用字典来存储缓存的结果和时间戳

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))  # 构建缓存的键
            current_time = time.time()
            
            # 若启用，则在缓存字典中查找args
            if enable and (key in cache_dict):
                result, timestamp = cache_dict[key]
                if current_time - timestamp <= timeout:
                    # 缓存未过期，直接返回结果
                    return result

            # 如果未启用或传入的args不存在，则返回结果并更新缓存字典
            if not enable or (not key in cache_dict):
                result = func(*args, **kwargs)
                cache_dict[key] = (result, current_time)
                return result

        return wrapper

    return decorator

if __name__ == "__main__":
    from timer import timer
    
    @timer
    def fib(n:int) -> int:
        if type(n) != int:
            raise TypeError()
        @cache(enable = True, timeout = 300)
        def inner(i:int) -> int:
            if i >= 2:
                return inner(i-1) + inner(i-2)
            elif i == 1 or i == 0:
                return 1
            else:
                return 0
        return inner(n)
        
    n = 200
    start = time.time()
    print(f"Attempt 1: fib({n}) = {fib(n)} \n  Time consumed:{time.time() - start}s")
    deltaT1 = time.time() - start
    print()
    start = time.time()
    print(f"Attempt 2: fib({n+450}) = {fib(n+100)} \n  Time consumed:{time.time() - start}s")
    deltaT2 = time.time() - start
