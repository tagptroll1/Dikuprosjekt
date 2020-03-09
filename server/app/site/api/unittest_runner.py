import types
import sys


def look_for_function(module, function, func_name):
    try:
        func = getattr(module, next(f for f in function if func_name in f))
    except StopIteration:
        f"{func_name} not found"
    return func


functions_c = []


def main(code, tests, code_ans, func_name):

    # Student
    code_module = types.ModuleType("code", code)
    exec(code, code_module.__dict__)

    # Answer
    code_module_ans = types.ModuleType("code_ans", code_ans)
    exec(code_ans, code_module_ans.__dict__)

    try:
        method_to_call = getattr(code_module, func_name)
    except:
        f"{func_name} not found"

    student_ans = [method_to_call(i[0], i[1]) for i in tests]
    ans = [getattr(code_module_ans, func_name)(i[0], i[1]) for i in tests]


    obj = {
        "student_ans": student_ans,
        "ans": ans,
        "all_same": sorted(ans) == sorted(student_ans)
    }

    return obj













