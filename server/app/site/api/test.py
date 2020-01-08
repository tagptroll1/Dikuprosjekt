import types


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

    ans = code.main()

    return tests.test(ans)
















