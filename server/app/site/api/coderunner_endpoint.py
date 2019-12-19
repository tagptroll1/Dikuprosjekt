from app.site.api.ApiBase import ApiBase, ApiBaseDefault, validate_body
from app.site.models.session_data import DataModel, Testnes

from flask import request


class CoderunnerEndpoint(ApiBaseDefault):
    """api/v1/coderunner"""
    model = Testnes

    def post(self):
        data = request.get_json()




endpoints = {
    "/api/v1/coderunner": CoderunnerEndpoint
}

__slots__ = [endpoints]
