from typing import List


class QuestionLineModel:
    TABLE = "questions"
    TYPE = "questionline"

    tags: List
    difficulty: int
    question_text: str
    question_code: List
    question_answer: int
