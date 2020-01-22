import types
import sys


def look_for_function(module, function, func_name):
    try:
        func = getattr(module, next(f for f in function if func_name in f))
    except StopIteration:
        f"{func_name} not found"
    return func


functions_c = []


def main(code, tests):
    functions = [
        a
        for a in dir(tests)
        if isinstance(getattr(tests, a), types.FunctionType)
    ]


    for i in functions:
        functions_c.append(look_for_function(tests, functions, i))

    try:
        ans = code.main()
        if ans is not None:
            return tests.test(ans), ans
    except Exception as err:
        return 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + "\n" + str(type(err).__name__) + "\n" + str(err), "None"

    return "Koden din må returnere noe!", "None"
















