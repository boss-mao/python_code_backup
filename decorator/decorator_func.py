from functools import wraps
def decorator_fun(fun):
    @wraps(fun)
    def new_fun(*args, **kwargs):
        result = fun(*args, **kwargs)
        print(result)
        return result

    return new_fun


@decorator_fun
def add(a, b):
    return a + b


print(add.__name__)