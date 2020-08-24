# Seeds the test_databse with testing test_data.
import requests
import string
import random
import json

request_url = 'http://127.0.0.1:5000/api/v1/questions'


def fill_up_chapter_with_questions(amount=1, tags=['chapter1', 'test_question'], difficulty=1):
    """
    This function will perform x amounts of HTTP requests in order to seed the database with test questions.
    @amount - the number of questions for each chapter.
    @tags - specify which chapter to fill up with questions.
    @difficulty - specify which difficulty to fill up. (possible values are 1, 2 and 3).
    """

    for i in range(1, amount):
        test_data = [
            {
                "question_text": f"TEST QUESTION {tags[0]} + difficulty: {difficulty}",
                "question_code": ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(1, 101))),
                "question_answer": "Right answer",
                "alternatives": [
                    "Right answer",
                    "Wrong alternative",
                    "Also the wrong alternative"
                ],
                "difficulty": difficulty,
                "tags": tags,
                "type": "multichoice"
            }
        ]

        req = requests.post(request_url, json=test_data)


def generate_some_quick_test_data():
    '''Generates two questions for each chapter difficulty. (6 for each chapter)'''
    for i in range(2, 7):
        fill_up_chapter_with_questions(
            amount=3, tags=[f"chapter{i}"], difficulty=1)
        fill_up_chapter_with_questions(
            amount=3, tags=[f"chapter{i}"], difficulty=2)
        fill_up_chapter_with_questions(
            amount=3, tags=[f"chapter{i}"], difficulty=3)
        print(f"posted questions for chapter {i}")


def add_feedback_to_all_questions():
    # get all questions in DB
    req = requests.get('http://127.0.0.1:5000/api/v1/questions')
    data = req.json()  # parse json

    # get all question feedbacks
    req2 = requests.get('http://127.0.0.1:5000/api/v1/question_feedback')
    feedback_data = req2.json()

    questions_that_already_have_feedback = list(
        map(lambda x: x['question_id'], feedback_data))

    number_of_questions = len(data)
    questions_remaining = number_of_questions

    for item in data:
        if item['_id'] in questions_that_already_have_feedback:
            questions_remaining -= 1
            print(f'questions remaining: {questions_remaining}')
            continue

        question_id = item["_id"]
        question_alternatives = item["alternatives"]

        test_feedback = {
            "feedbacks": {},
            "question_id": question_id
        }

        print(question_id)
        print("-----------")
        for x in question_alternatives:
            print(f"Alternative: {x}")
            feedback = input("feedback for this alternative:")
            test_feedback["feedbacks"].update({x: feedback})

        print("-----------")
        print(test_feedback)

        questions_remaining -= 1
        if not questions_remaining == 0:
            print(f'questions remaining: {questions_remaining}')
        req = requests.post(
            'http://127.0.0.1:5000/api/v1/question_feedback', json=test_feedback)


def main():
    print("----------------------------")
    print("DIKUPROSJEKT DATABASE SEEDER")
    print("----------------------------")
    print("1. Generate test questions")
    print("2. Add feedback to questions that don't have any")
    print("3. Exit")
    print("----------------------------")

    choice = input("Select option >")
    if choice == "1":
        generate_some_quick_test_data()
    if choice == "2":
        add_feedback_to_all_questions()
    else:
        quit()


if __name__ == "__main__":
    main()
