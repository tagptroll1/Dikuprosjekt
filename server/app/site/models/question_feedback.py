from typing import Dict


class QuestionFeedback:
    TABLE = "question_feedback"

    question_id: str
    feedbacks: Dict
