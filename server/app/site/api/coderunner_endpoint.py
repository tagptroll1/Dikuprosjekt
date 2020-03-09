from app.site.api.ApiBase import ApiBase, ApiBaseDefault, validate_body
from app.site.models.session_data import DataModel
from app.site.api.unittest_runner import main
import types

from flask import request
from flask import jsonify


class CoderunnerEndpoint(ApiBaseDefault):
    """api/v1/coderunner"""
    model = DataModel

    def post(self):
        data = request.get_json()
        code_ans = data["answer_code"]
        code = data["code"]
        tests = data["tests"]
        function_name = data["function_name"]

        obj = main(code, tests, code_ans, function_name)

        return jsonify(data=obj)


endpoints = {
    "/api/v1/coderunner": CoderunnerEndpoint
}

__slots__ = [endpoints]