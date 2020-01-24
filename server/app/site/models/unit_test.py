from typing import List

class UnitTestModel:
    TABLE = "questions"
    TYPE = "unittest"

    tags: List
    difficulty: int
    question_text: str
    question_answer: str
    unit_test: str
