import typing

from flasgger.utils import swag_from  # Specify swagger doc path
from app.decorators.api_decorators import json_serialize
from app.decorators.protected import protected
from app.site.exceptions import QuestionAlreadyExistsException
from app.site.models.feedback import Feedback as FeedbackModel
from app.site.models.question_feedback import (
    QuestionFeedback as QuestionFeedbackModel
)

from flask import request
from .ApiBase import ApiBase, ApiBaseDefault, validate_body

SWAGGERDOC_PATH = '../../swagger_documentation/feedback_endpoint'


class QuestionFeedback(ApiBase):
    @json_serialize
    @swag_from(f'{SWAGGERDOC_PATH}/delete_all_question_feedbacks.yml')
    def delete(self):
        allFeedback = self.get()
        for F in allFeedback:
            print(f'Question feedback object {F["_id"]} deleted.')
            try:
                QuestionFeedBackById.delete(self, id_=F['_id'])
            except TypeError:
                return {"message": "Nothing to delete."}, 204

        return {"message": f"{len(allFeedback)} feedback objects deleted."}, 200

    def validate_set(self, body):
        return True

    @json_serialize
    @swag_from(f'{SWAGGERDOC_PATH}/get_question_feedback.yaml')
    def get(self):
        self.manager.log.info(
            f"All {QuestionFeedbackModel.TABLE} entires were requested."
        )
        return list(
            self.database.find(
                QuestionFeedbackModel.TABLE,
                question_id={"$exists": True}
            )
        )

    # @protected
    @json_serialize
    def patch(self):
        body = request.get_json()
        types = typing.get_type_hints(QuestionFeedbackModel)
        error_or_None = validate_body(body["new"], types, post=False)

        if error_or_None is not None:
            return error_or_None

        valid_set = self.validate_set(body["new"])
        if valid_set is not True:
            return valid_set

        id_ = body.get("_id")
        new_record = body.get("new")

        if not id_:
            return {"message": "json body does not contain key `_id`"}, 400

        if not new_record:
            return {"message": "json body does not contain key `new`"}, 400

        if not self.database.exists(QuestionFeedbackModel.TABLE, _id=id_):
            return {"message": "Question does not exist"}, 400

        if new_record.get("feedbacks"):
            new_feedbacks = new_record["feedbacks"]
            old_record = self.database.find_one(
                QuestionFeedbackModel.TABLE, _id=id_
            )
            feedbacks = {**old_record["feedbacks"], **new_feedbacks}
            result = self.database.edit(
                QuestionFeedbackModel.TABLE,
                {"_id": id_},
                {"feedbacks": feedbacks},
            )
        else:
            result = self.database.edit(
                QuestionFeedbackModel.TABLE,
                {"_id": id_},
                new_record,
            )
        if result is None:
            return {"message": "Nothing changed, wrong endpoint?"}, 400
        return result, 200

    # @protected
    @json_serialize
    @swag_from(f'{SWAGGERDOC_PATH}/post_question_feedback.yaml')
    def post(self):
        body = request.get_json()

        types = typing.get_type_hints(QuestionFeedbackModel)
        error_or_None = validate_body(body, types)

        if error_or_None is not None:
            return error_or_None

        valid_set = self.validate_set(body)
        if valid_set is not True:
            return valid_set

        try:
            response = self.database.insert_one(
                QuestionFeedbackModel.TABLE, body
            )
        except QuestionAlreadyExistsException as e:
            self.manager.log.info(
                f"{QuestionFeedbackModel.TABLE} post returned 409 | {e}"
            )
            return {"message": str(e)}, 409
        except Exception as e:
            self.manager.log.info(
                f"{QuestionFeedbackModel.TABLE} post returned 500 | {e}"
            )
            return {"message": f"Internal server error: {e}"}, 500

        self.manager.log.info(
            f"{QuestionFeedbackModel.TABLE} question was posted."
        )

        if response:
            return body, 201
        else:
            return {"message": "something went wrong"}, 500


class QuestionFeedBackById(ApiBase):
    @json_serialize
    @swag_from(f"{SWAGGERDOC_PATH}/get_question_feedback_by_id.yml")
    def get(self, id_):
        getted = self.database.find_one(QuestionFeedbackModel.TABLE, _id=id_)
        if getted:
            return getted, 200
        return {"message": "No feedback for this id"}, 400

    @json_serialize
    @swag_from(f"{SWAGGERDOC_PATH}/delete_question_feedback_by_id.yml")
    def delete(self, id_):
        delete_result = self.database.delete(
            QuestionFeedbackModel.TABLE, _id=id_)
        if delete_result.deleted_count:
            return {"message": f"Question feedback object {id_} deleted."}, 200
        return {"message": "nothing deleted"}, 400


class FeedbackSet(ApiBase):
    @json_serialize
    def post(self):
        body = request.get_json()
        feedbacks = list(self.database.find("feedback", question_id=body))
        response = []
        for feedback in feedbacks:
            q_feeds = feedback["feedbacks"]
            ids = list(q_feeds.values())
            q_feedbacks = list(self.database.find("feedback", feedback_id=ids))

            resp = {"question_id": feedback["question_id"]}
            for key, value in q_feeds.items():
                for feed in q_feedbacks:
                    if feed["feedback_id"] == value:
                        resp[key] = feed["feedback"]
            response.append(resp)

        print("testing", response)
        return response


endpoints = {
    # "/api/v1/feedback": Feedback,
    # "/api/v1/feedback/<id_>": FeedbackById,
    "/api/v1/question_feedback": QuestionFeedback,
    "/api/v1/question_feedback/<id_>": QuestionFeedBackById,
    "/api/v1/question_feedback/set": FeedbackSet
}
