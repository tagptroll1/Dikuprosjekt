import logging

from flask import Flask
from flask_restful import Resource, Api
from .database import MongoDb
from flasgger import Swagger


class Manager(Flask):
    def __init__(self):
        super().__init__(__name__)
        # Route the flask server through swagger in order to generate documentation.
        self.swagger = Swagger(self)
        self.swagger.config["openapi"] = "3.0.0"
        self.swagger.config["title"] = "Feedback UiB API"
        self.swagger.config["description"] = "This API enables the posting and retrieval of  data stored in UiB Feedback's database."

        self.swagger.config
        self.api = Api(self)
        self.db = MongoDb()
        self.log = logging.getLogger(__name__)
        self.log.debug("Manager initialized")

    def add_from_dict(self, dic):
        for endpoint, class_ in dic.items():
            class_.add(self, endpoint)

    def load_api_resources(self, endpoints):
        for endpoint in endpoints:
            self.add_from_dict(endpoint)
