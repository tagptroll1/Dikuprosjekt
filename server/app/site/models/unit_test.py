from typing import List

class UnitTestModel:
    TABLE = "questions"
    TYPE = "coderunner"

    tags: List
    difficulty: int
    question_text: str
    question_answer: str
    unit_tests: List
