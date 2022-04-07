import argparse

import code.feedback as feedback
import code.submit_question as submit_question

parser = argparse.ArgumentParser()
parser.add_argument('--mode', action='store', type=int, required=True)

args = parser.parse_args()


if args.mode == 1:
    submit_question.main()
elif args.mode == 2:
    feedback.main()
