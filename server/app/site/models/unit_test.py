from typing import List

class UnitTestModel1:
    TABLE = "questions"
    TYPE = "unittest"

    tags: List
    difficulty: int
    question_text: str
    question_answer: str
    unit_test: str


class UnitTestModel:
    TABLE = "questions"
    TYPE = "unittest"

    tags: List # ['functions']
    difficulty: int # 1
    question_text: str # Skriv en funksjon snitt(x,y) som beregner gjennomsnittet av 2 tall
    function_name: str # snitt
    question_answer_code: str # def snitt(x,y): return (x+y) / 2
    question_testcases: List #
    hints: List #


