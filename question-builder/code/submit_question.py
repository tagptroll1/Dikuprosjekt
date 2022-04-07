import json
import os
import requests
from datetime import datetime
from pprint import pprint
from textwrap import dedent

from code.decorators import terminal, auto_save
from code.utils import (
    clear_terminal, get_int_input, get_multi_line_input
)


date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
save_file = f"save-{date}.json"


class QuestionBuilder:
    def __init__(self):
        self.questions = []

    @staticmethod
    def build_base_question(type_):
        """Helper function to abstract out code duplication"""

        question = {}

        print("\nEnter question text")
        question["question_text"] = "\n".join(get_multi_line_input())

        clear_terminal()

        if type_ == "dropdown":
            question_code = (
                "Place a '@@' anywhere in the code "
                "for the dropdown box (max 1)"
            )
        else:
            question_code = ""

        question["question_code"] = "\n".join(
            get_multi_line_input("Question code. ", end=question_code)
        )

        clear_terminal()
        print("Enter the answer for the question")
        question_answer = "\n".join(get_multi_line_input())
        question["question_answer"] = question_answer

        clear_terminal()
        alternatives = [question_answer]
        print(
            "You may now enter n amount of alternatives\n"
            "(Do NOT enter the answer from before, it's already stored)\n"
            "Write 'DONE', 'EXIT' or blank line when finished."
        )
        while True:
            answer = input("> ")
            if answer.upper() == "DONE" or answer.upper() == "EXIT":
                break

            if not answer:
                break

            alternatives.append(answer)
        question["alternatives"] = alternatives

        clear_terminal()
        print("What difficulty is this question? (1-5)")
        question["difficulty"] = get_int_input("> ")

        clear_terminal()
        tags = []
        print(
            "Add tags to identify and filter the question"
            "\nWrite 'DONE', 'EXIT' or blank line when finished"
        )
        while True:
            tag = input("> ")
            if tag.upper() == "DONE" or tag.upper() == "EXIT":
                break
            if not tag:
                break
            tags.append(tag)
        question["tags"] = tags
        return question

    @terminal
    @auto_save(save_file)
    def create_dropdown(self):
        """Create a dropdown question and appends to list of questions"""

        try:
            type_ = "dropdown"
            question = QuestionBuilder.build_base_question(type_)
            question["type"] = type_
            self.questions.append(question)

            print(
                "\nQuestion added, there are now "
                f"{len(self.questions)} questions"
            )
            pprint(question)

            return question
        except KeyboardInterrupt:
            return

    @terminal
    @auto_save(save_file)
    def create_multichoice(self):
        """Create a multi choice question and appends to list of questions"""

        try:
            type_ = "multichoice"
            question = QuestionBuilder.build_base_question(type_)
            question["type"] = type_
            self.questions.append(question)

            print(
                "\nQuestion added, there are now "
                f"{len(self.questions)} questions"
            )
            pprint(question)

            return question
        except KeyboardInterrupt:
            return

    @terminal
    def print_questions_simple(self):
        """Prints all questions in an easy to read format of
        text: amount of alternatives"""

        for i, question in enumerate(self.questions):
            print(
                f"{i}.",
                question["question_text"],
                "amount of answers:",
                len(question["alternatives"])
            )

    @terminal
    def print_questions(self):
        """Pretty prints the entire questions list"""

        pprint(self.questions)

    @terminal
    def create_new_tag_set(self):
        try:
            tags_prompt = (
                "Input one or more tags to add to "
                "a set of questions(on new lines)\n"
            )
            ids_prompt = (
                "Input one or more ids you wish to "
                "add these tags to(on new lines)\n"
            )

            tags = get_multi_line_input(tags_prompt)
            if tags[0] == "" and len(tags) == 1:
                return print("No tags were given, aborting")
            print()

            ids = get_multi_line_input(ids_prompt)
            if ids[0] == "" and len(ids) == 1:
                return print("No ids were given, aborting.")
            print()

            to_send = {"tag": tags, "ids": ids}

            print(
                f"You are about to post {len(tags)} tags "
                f"to {len(ids)} questions, are you sure? [y/n]",
                f"tags: {tags}",
                f"ids: {ids}",
                sep="\n"
            )
            try:
                if input("> ").lower()[0] != "y":
                    return print("Aborting...")
            except IndexError:
                return print("Aborting")

            url = os.environ.get("API_URL") or "http://localhost:5000/api"
            token = os.environ.get("API_KEY") or "bananas"

            resp = requests.post(
                url + "/v1/searchset",
                json=to_send,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"token {token}"
                }
            )

            if resp.status_code == requests.codes.ok:
                print("success!")
            else:
                print("Failed...", resp.text)
        except KeyboardInterrupt:
            return
        except Exception as e:
            raise e

    @terminal
    def send(self):
        """Sends to api
        Requires API_KEY and API_URL to either be in environment variables
        or in a .env file in the same directory, else it sends to localhost
        with bananas as token.
        """
        try:
            with open(save_file) as f:
                json_content = json.load(f)
        except FileNotFoundError:
            return print("You haven't created any questions yet!")

        to_send = self.questions
        if json_content != self.questions:
            print(
                save_file,
                "is different from cached questions",
                "\n1. Send cached list",
                "\n2. Send saved list",
                "\n3. Go back"
            )
            selection = get_int_input("> ")
            if selection == 3:
                return

            if selection == 2:
                to_send = json_content

        print(
            f"You are about to post {len(to_send)} "
            "questions, are you sure? [y/n]"
        )
        try:
            if input("> ").lower()[0] != "y":
                return print("Aborting...")
        except IndexError:
            return print("Aborting")

        url = os.environ.get("API_URL") or "http://localhost:5000/api"
        token = os.environ.get("API_KEY") or "bananas"

        resp = requests.post(
            url + "/v1/questions",
            json=to_send,
            headers={
                "Authorization": f"token {token}"
            }
        )

        if resp.status_code == requests.codes.ok:
            print("Success!")
            json_resp = resp.json()
            responses = json_resp["responses"]
            questions = [(response["_id"], response["question_text"])
                         for response in responses]

            for id_, question in questions:
                print(f"{id_}: {question}")

        else:
            print("Failed...", resp.text)

    def print_menu(self):
        """Prints the menu with options"""

        print(dedent(f"""
            Welcome to question json builder & sender!
            You can ctrl+c at any time during question creation to go back.
            You currently have {len(self.questions)} questions ready.

            What would you like to do?
            - 1. Add a dropdown question
            - 2. Add a multichoice question
            - 3. View current list of questions simplified
            - 4. View current list of questions expanded
            - 5. Create a new set of questions with a common tag
            - 6. Send questions
            - 7. Exit

        """))


question_builder = QuestionBuilder()
functions = [
    question_builder.create_dropdown,
    question_builder.create_multichoice,
    question_builder.print_questions_simple,
    question_builder.print_questions,
    question_builder.create_new_tag_set,
    question_builder.send,
]


def main():
    while True:
        clear_terminal()
        question_builder.print_menu()

        while True:
            try:
                selection = get_int_input("> ") - 1
                if len(functions) < selection <= 0:
                    raise UserWarning
            except UserWarning:
                print(f"Not a valid selection, use 1-{len(functions)}")
            except KeyboardInterrupt:
                return print("Good bye!")
            else:
                break

        if selection == len(functions):
            break

        functions[selection]()


if __name__ == "__main__":
    main()
