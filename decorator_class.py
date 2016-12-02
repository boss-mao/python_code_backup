from functools import wraps


class logResult(object):
    def __init__(self, filename='results.txt'):
        self.filename = filename

    def __call__(self, fun):
        @wraps(fun)
        def new_fun(*args, **kwargs):
            result = fun(*args, **kwargs)
            with open(self.filename, 'wt') as f:
                f.write(str(result) + '\n')
            return result

        self.send_notification()
        return new_fun

    def send_notification(self):
        pass


@logResult('log.txt')
def add(a, b):
    return a + b

print add(1,2)