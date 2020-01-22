from app.site.api.ApiBase import ApiBase, ApiBaseDefault, validate_body
from app.site.models.session_data import DataModel, Testnes
from app.site.api.unittest_runner import main
import types

from flask import request
from flask import jsonify


class CoderunnerEndpoint(ApiBaseDefault):
    """api/v1/coderunner"""
    model = Testnes

    def post(self):
        data = request.get_json()
        code = data["code"]
        tests = data["unit_tests"]

        code_module = types.ModuleType("code", code)
        test_module = types.ModuleType("tests", tests)

        exec(code, code_module.__dict__)
        exec(tests, test_module.__dict__)

        feedback, ans = main(code_module, test_module)

        return jsonify(fd=feedback, ans=ans)


endpoints = {
    "/api/v1/coderunner": CoderunnerEndpoint
}

__slots__ = [endpoints]