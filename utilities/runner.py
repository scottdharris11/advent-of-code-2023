import time

"""Decorator for printing results and timing solutions"""
def Runner(day, part):
    def decorator(function):
        def wrapper(*args, **kwargs):
            start = time.time()
            ans = function(*args, **kwargs)
            end = time.time()
            print("%s, %s (%d ms): %s" % (day, part, end-start, ans))
            return ans
        return wrapper
    return decorator