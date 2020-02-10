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
    function_name: str # snitt(x, y)
    question_answer_code: str # def snitt(x,y): return (x+y) / 2
    question_textcases: List # [snitt(2,4), snitt(3,4), snitt(4,5)]
    question_answer: List # [question_answer_code(2,4), question_answer_code(3,4), question_answer_code(4,5)]
    hints: List #


