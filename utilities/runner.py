import time

"""Decorator for printing results and timing solutions"""
def Runner(day, part):
    def decorator(function):
        def wrapper(*args, **kwargs):
            start = time.time() * 1000
            ans = function(*args, **kwargs)
            end = time.time() * 1000
            print("%s, %s (%d ms): %s" % (day, part, end-start, ans))
            return ans
        return wrapper
    return decorator