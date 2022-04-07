import os
from textwrap import dedent

import requests

from code.decorators import terminal
from code.utils import clear_terminal, get_int_input, get_multi_line_input


class Feedback:
    def __init__(self):
        self.url = os.environ.get("API_URL") or "http://localhost:5000/api"
        self.token = os.environ.get("API_URL") or "bananas"

    @terminal
    def info(self):
        print(dedent(
            """
            Feedback builder.

            Terminology:

            feedback:
                A specific message that is to be displayed to a user.
                This is not directly linked to a question, but a tag.
                The tag is given in a set to fetch the message.

                Structure:
                    {
                        "feedback_id": "some-tag-here",
                        "feedback": "This is the message given to a user"
                    }

            question set or just set:
                This is a set which belongs to a question alone.
                It acts as a bridge between 1 question
                and multiple feedback messages,
                this is done by referencing the questions tag.
                The feedbacks attribute directly connects a
                questions alternative to a tag,
                which again references the feedback
                for choosing that alternative.

                Structure:
                    {
                        "question_id": "<id of a question">,
                        "feedbacks": {
                            "alternative": "some-tag-here",
                            "True": "tag-about-True",
                            "False": "tag-about-False",
                            "List": "list-as-a-stack"
                        }
                    }
            """
        ))

    def print_menu(self):
        print(dedent(
            """
            Welcome to the feedback builder!
            You can ctrl + c at any time to go back a step in the process.
            This app does not temporarily save your progress,
            but instead sends it as you work.

            1. Info
            2. See all feedback alternatives
            3. Lookup feedback by tag
            4. Create a new feedback alternative
            5. Get all question feedback sets
            6. Get fully formed set (with feedback messages)
            7. Create/edit question feedback set
            8. Exit

            """
        ))

    @terminal
    def see_all_feedbacks(self):
        url = f"{self.url}/v1/feedback"

        response = requests.get(url)
        json_resp = response.json()

        # Bug in api atm returns sets as well
        feedbacks = [
            (
                f"feedback_id: {feedback['feedback_id']}\n"
                f"feedback: {feedback['feedback']}\n"
            )
            for feedback in json_resp
            if feedback.get("feedback_id")
        ]
        print("\n".join(feedbacks))

    @terminal
    def lookup_feedback(self):
        tag = input("Input tag name: ").replace(" ", "-")
        url = f"{self.url}/v1/feedback/{tag}"

        response = requests.get(url)
        json_resp = response.json()
        print(
            f"feedback_id: {json_resp['feedback_id']}",
            f"feedback: {json_resp['feedback']}",
            sep="\n"
        )

    @terminal
    def create_feedback(self):
        try:
            print("Input new tag name, space are converted to '-'")
            tag = input("> ").replace(" ", "-")

            print("\nWrite the feedback message to go with this tag")
            feedback = "\n".join(get_multi_line_input())

            if not tag:
                return print("No tag given, aborting")

            if not feedback:
                return print("No message given, aborting")

            clear_terminal()
            print(
                f"You are about to post the tag \"{tag}\" "
                "with the message:",
                f'"""\n{feedback}\n"""\n',
                "are you sure? [y/n]",
                sep="\n"
            )
            try:
                if input("> ").lower()[0] != "y":
                    return print("Aborting...")
            except IndexError:
                return print("Aborting")

        except KeyboardInterrupt:
            return print("\naborting...")

    @terminal
    def get_all_sets(self):
        try:
            url = f"{self.url}/v1/question_feedback"

            response = requests.get(url)
            json_resp = response.json()

            for q_set in json_resp:
                print(f'question_id: {q_set["question_id"]}')

                for answer, tag in q_set["feedbacks"].items():
                    answer = answer.replace("\n", "\\n").replace("\t", "\\t")
                    print(f"\t{answer}: {tag}")
        except KeyboardInterrupt:
            return print("Aborting")

    def get_full_set_internal(self, id_):
        url = f"{self.url}/v1/question_feedback/set"
        if not id_:
            id_ = input("Paste the id of the questions:\n>")

        response = requests.post(url, json=id_)
        json_resp = response.json()

        for q_set in json_resp:
            print("id: ", q_set.pop("question_id"), "\n")
            for key, value in q_set.items():
                key = key.replace("\n", "\\n").replace("\t", "\\t")
                print(f"  {key:<10}: {value}")

    @terminal
    def get_full_set(self):
        try:
            id_ = input("Paste the id of the questions:\n>")
            self.get_full_set_internal(id_)
        except KeyboardInterrupt:
            return print("Aborting")

    @terminal
    def edit_set(self):
        id_ = input("Paste the id of the questions:\n>")
        url = f"{self.url}/v1/question_feedback"

        response = requests.get(url)
        json_resp = response.json()

        try:
            question_set = next(
                s for s in json_resp if s["question_id"] == id_
            )
        except StopIteration:
            print("This question does not exist!")
            return

        feedbacks = question_set["feedbacks"].items()

        print()
        for i, (answer, tag) in enumerate(feedbacks):
            answer = answer.replace("\n", "\\n").replace("\t", "\\t")
            print(f"{i}. {answer}: {tag}")

        print("\nSelect the answer you would like to edit.")
        selection = get_int_input("> ")

        clear_terminal()

        print(f"{id_}\n")

        for i, (answer, tag) in enumerate(feedbacks):
            tmp_answer = answer.replace("\n", "\\n").replace("\t", "\\t")
            if i == selection:
                new_tag = input(f"{i}. {tmp_answer}: ")
                question_set["feedbacks"][answer] = new_tag
                tmp = tmp_answer
            else:
                print(f"{i}. {tmp_answer}: {tag}")

        print(
            f"You are about to edit the tag for answer {tmp}, "
            "are you sure? [y/n]"
        )
        try:
            if input("> ").lower()[0] != "y":
                return print("Aborting...")
        except IndexError:
            return print("Aborting")

        # post here
        resp = requests.post(
            self.url + "/v1/question_feedback",
            json=question_set,
            headers={
                "Authorization": f"token {self.token}"
            }
        )

        if resp.status_code == requests.codes.ok:
            print("Success!")
            self.get_full_set_internal(id_)
        else:
            print("Failed...", resp.text)


feedback = Feedback()
functions = [
    feedback.info,
    feedback.see_all_feedbacks,
    feedback.lookup_feedback,
    feedback.create_feedback,
    feedback.get_all_sets,
    feedback.get_full_set,
    feedback.edit_set,
]


def main():
    while True:
        clear_terminal()
        feedback.print_menu()

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
