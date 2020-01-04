from app.site.models.unit_test import UnitTestModel

from app.site.api.ApiBase import ApiBaseDefault

class UnitTest(ApiBaseDefault):
    """api/v1/unittest"""

    model = UnitTestModel



endpoints = {
    "/api/v1/unittest": UnitTest
}

__slots__ = [endpoints]
