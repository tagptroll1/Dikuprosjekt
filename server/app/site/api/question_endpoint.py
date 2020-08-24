import random  # Used for shuffling lists of objects
import typing  # Used for type checking data in HTTP requests.

from flasgger.utils import swag_from  # Specify swagger doc path
from app.decorators.api_decorators import json_serialize
from app.decorators.protected import protected
from app.site.api.ApiBase import ApiBase, validate_body
from app.site.exceptions import QuestionAlreadyExistsException
from app.site.models.dropdown import DropdownModel
from app.site.models.fill_in import FillInModel
from app.site.models.multi_choice import MultiChoiceModel
from app.site.models.question_line import QuestionLineModel
from flask import request

'''
Endpoint for questions used in the quiz.
@orotected methods require authorization and cannot be done without the API-KEY.
All other methods are exposed for public external use and will be exposed.

WARNING:
Private methods are currently NOT decorated with @protected,
deleting and adding data will not require authorization.

'''

# These models determine the allowed structure of questions.
QUESTION_TYPES = ["dropdown", "multichoice", "fillin", "questionline"]
MODELS = {
    "dropdown": DropdownModel,
    "multichoice": MultiChoiceModel,
    "fillin": FillInModel,
    "questionline": QuestionLineModel,
}

SWAGGERDOC_PATH = '../../swagger_documentation/question_endpoint'


class QuestionSet(ApiBase):
    @json_serialize
    @swag_from(f'{SWAGGERDOC_PATH}/get_questions.yml')
    def get(self):
        self.manager.log.info(
            f"A set of random questions were requested."
        )

        args = dict(request.args)

        questions = []
        table_args = {}
        additional_args = {}

        for key, value in args.items():
            if key in QUESTION_TYPES:
                table_args[key] = value
                continue

            if key == "tags":
                value = value.split(",")
            elif value.isnumeric():
                value = int(value)

            additional_args[key] = value

        limit = additional_args.pop("limit", None)

        if not table_args:
            tmp = list(self.database.find("questions", **additional_args))
            random.shuffle(tmp)

            if limit:
                return tmp[:limit], 200
            return tmp, 200

        for table, amount in table_args.items():
            amount = int(amount)
            count = self.database.count("questions", type=table)
            if amount > count:
                message = f"{table} amount too high, max is: {count}"
                return {"message": message}, 400

            tmp = list(
                self.database.find(
                    "questions",
                    type=table,
                    **additional_args
                )
            )

            # TODO: seeded shuffle
            # Shuffle and extend so we can random results
            random.shuffle(tmp)
            questions.extend(tmp[:amount])

        random.shuffle(questions)
        return questions, 200

    @json_serialize
    @swag_from(f'{SWAGGERDOC_PATH}/delete_all.yml')
    def delete(self):
        '''Deletes the entire question database.'''
        allQuestions = self.get()  # Do a regular GET request to get all questions.
        for Q in allQuestions[0]:
            # Loop through their ID's and perform a delete on each one.
            QuestionSetById.delete(self, id_=Q['_id'])

        if len(allQuestions[0]) == 0:
            return {"message": "No questions to delete, the database is empty."}, 400
        else:
            return {"message": f"{len(allQuestions[0])} questions deleted"}, 200

    @json_serialize
    @ swag_from(f'{SWAGGERDOC_PATH}/post_questions.yml')
    def post(self):
        body = request.get_json()  # Recieves HTTP request
        if not isinstance(body, list):
            if not body.get("type"):  # Check for required field "type" in the request's body
                return {
                    "message": (
                        "type is a required field when using this endpoint"
                    )
                }, 400
            # Check if the type conforms to predefined models.
            if body.get("type") not in QUESTION_TYPES:
                return {"message": "Unrecognized question type"}, 400

            model = MODELS[body["type"]]
            types = typing.get_type_hints(model)
            error_or_None = validate_body(body, types)

            if error_or_None is not None:
                return error_or_None, 400

            try:
                return self.database.insert_one(model.TABLE, body)
            except QuestionAlreadyExistsException as e:
                return {"message": str(e)}, 400

        assert isinstance(body, list)

        errors = []
        responses = []

        for question in body:
            if not question.get("type"):
                errors.append({
                    "message": (
                        "type is a required field - question with text "
                        f"{question['question_text']} failed to store"
                    )
                })
                continue

            if question.get("type") not in QUESTION_TYPES:
                errors.append({
                    "message": (
                        "Unrecognized question type - question with id "
                        f"{question['question_text']} failed to store"
                    )
                })
                continue

            model = MODELS[question["type"]]

            types = typing.get_type_hints(model)
            types["type"] = str
            error_or_None = validate_body(question, types)

            if error_or_None is not None:
                errors.append(error_or_None[0])
                continue

            try:
                # Have to convert id as some conversion went bad here
                result = self.database.insert_one(model.TABLE, question)
                result["_id"] = str(result["_id"])
                responses.append(result)
            except QuestionAlreadyExistsException as e:
                errors.append({"message": str(e)})

        if errors and responses:
            return {"errors": errors, "responses": responses}, 200
        elif errors and not responses:
            return {"errors": errors}, 400
        else:
            return {"responses": responses}, 200


class QuestionSetById(ApiBase):
    @json_serialize
    @swag_from(f'{SWAGGERDOC_PATH}/get_question_by_id.yml')
    def get(self, id_):
        getted = self.database.find_one("questions", _id=id_)
        if getted:
            return getted, 200
        return {"message": "No feedback for this id"}, 400

    # @protected
    @json_serialize
    @swag_from(f'{SWAGGERDOC_PATH}/del_question_by_id.yml')
    def delete(self, id_):
        delete_result = self.database.delete("questions", _id=id_)

        if delete_result.deleted_count:
            return {"message": f"question {id_} deleted."}
        return {"message": "nothing deleted"}, 400


endpoints = {
    "/api/v1/questions": QuestionSet,
    "/api/v1/questions/<id_>": QuestionSetById,
}


__slots__ = [endpoints]
