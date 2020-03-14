from typing import List


class DataModel:
    TABLE = "data"

    user: str
    start_time: str
    end_time: str
    questions: List


class QuestionDataModel:
    question_id: str
    selected_answer: str
    correct: bool
    #time_spent: int  # seconds
    tries: int  # num of tries

class UnitTestingQuestionDataModel:
    question_id: str
    selected_answer: str
    all_correct: bool
    num_tests: int
    correct: int
    tries: int
    show_solution: bool