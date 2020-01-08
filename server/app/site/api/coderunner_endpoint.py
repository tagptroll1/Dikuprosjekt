from app.site.api.ApiBase import ApiBase, ApiBaseDefault, validate_body
from app.site.models.session_data import DataModel, Testnes
from app.site.api.test import main
import types

from flask import request
from flask import jsonify


class CoderunnerEndpoint(ApiBaseDefault):
    """api/v1/coderunner"""
    model = Testnes

    def post(self):
        data = request.get_json()
        code = data["code"]
        # code = 'def main(): return sum(range(1,100))'
        # print(data["unit_tests"])
        # tests = data["unit_tests"]
        # tests = ["def test(): self.assertEquals(1,1)"]
        tests = """def test(case): 
                       if case < 4000: 
                           return 'For lavt' 
                       elif case > 5000: 
                           return 'For høyt'
                       elif case == 4950:
                           return 'Riktig!'"""

        code_module = types.ModuleType("code", code)
        test_module = types.ModuleType("tests", tests)
        exec(code, code_module.__dict__)
        exec(tests, test_module.__dict__)

        feedback = main(code_module, test_module)
        print(feedback)
        return jsonify(fd=feedback)


endpoints = {
    "/api/v1/coderunner": CoderunnerEndpoint
}

__slots__ = [endpoints]