import json
from functools import wraps

from code.utils import clear_terminal


def terminal(func):
    """Decorator for cleaner terminal use
    Cleaning the terminal and prompting the user to press enter at the end
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        clear_terminal()
        res = func(*args, **kwargs)
        try:
            input("\nPress enter to continue.")
        except KeyboardInterrupt:
            return res
        return res
    return wrapper


def auto_save(file: str):
    """Decorator for auto saving result to json
    Append to a list in a json file, will create it if it doesn't exist.

    :file: str is the name of the file to save to
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                with open(file) as f:
                    json_content = json.load(f)
            except FileNotFoundError:
                with open(file, "w") as f:
                    f.write("[]")

                with open(file) as f:
                    json_content = json.load(f)

            assert isinstance(json_content, list)

            result = func(*args, **kwargs)

            # result may be None if aborted early
            if result is None:
                return result

            json_content.append(result)

            with open(file, "w") as f:
                json.dump(json_content, f, indent=4)

            return result
        return wrapper
    return decorator
