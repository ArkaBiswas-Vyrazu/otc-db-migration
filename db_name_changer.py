#!./venv/bin/python3
"""Script to modify all names in database to follow same naming convention.

This was done for the Money Tribe Project, as there was a lot of inconsistentency
in the naming of all tables and columns.
Also, UpperCase Naming convention was used a lot there, which can cause
unnecessary errors in query generation, so changing
the name was also important for this.

Please note that only the table names and the column names have been considered
here. This script should be able to provide the grounds for more extensions.
"""

from typing import Optional, Literal
import sys
import string as str_lib
import os
import json

import structlog
from dotenv import load_dotenv
from sqlalchemy import (
    URL,
    create_engine,
    MetaData,
    text,
)


def get_traceback(show_locals: bool = True, max_length: Optional[int] = 80) -> list[dict[str]]:
    """Returns relevant traceback information in JSON Format.

    This function can also be used to debug wherever necessary, 
    you only need to make sure that an exception gets called first.
    
    Reference: https://gitlab.com/-/snippets/2284049
    """

    exc_info = sys.exc_info()

    trace = structlog.tracebacks.extract(
            *exc_info,
            show_locals=show_locals,
            locals_max_string=max_length
        )

    for stack in trace.stacks:
        if len(stack.frames) <= 50:
            continue

        half = 50 // 2
        fake_frame = structlog.tracebacks.Frame(
            filename="",
            lineno=-1,
            name=f"Skipped frames: {len(stack.frames) - (2 * half)}",
        )
        stack.frames[:] = [*stack.frames[:half], fake_frame, *stack.frames[-half:]]

    stack_dicts = [
        {
            'exc_type': stack.exc_type,
            'exc_value': stack.exc_value,
            'syntax_error': stack.syntax_error,
            'is_cause': stack.is_cause,
            'frames': [
                {
                    'filename': frame.filename,
                    'lineno': frame.lineno,
                    'name': frame.name,
                    'locals': frame.locals,
                }

                for frame in stack.frames
            ],
        }

        for stack in trace.stacks
    ]

    return stack_dicts


class Caser:
    """Utility Class to convert string casing"""

    def __init__(self, string: Optional[str] = None) -> None:
        self.string = None
        if string is not None:
            self.string = string.strip()

    def identify(self, string: Optional[str] = None) -> str | None:
        """Identify the type of casing that was used in the provided string.
        
        If parameter is not passed to this function, class string will be identified.

        Reference:
        https://stackoverflow.com/questions/76115038/how-to-find-out-what-case-style-a-string-is-pascal-snake-kebab-camel
        """

        string = string or self.string

        if string.isupper() and string.isalpha():
            return "UPPER"

        if string.islower() and string.isalpha():
            return "LOWER"

        found = "PASCAL" if (string[0] in str_lib.ascii_uppercase) else None
        for i in range(1,len(string)):
            if string[i] == "-":
                if found == "KEBAB":
                    continue

                if found is None:
                    found = "KEBAB"
                    continue

                return None

            if string[i] == "_":
                if found == "SNAKE":
                    continue

                if found is None:
                    found = "SNAKE"
                    continue

                return None

            if string[i].isupper():
                if found in {"CAMEL", "PASCAL"}:
                    continue

                if found is None:
                    found = "CAMEL"
                    continue

                return None
        return found

    def split_joined_words(self, string: Optional[str] = None) -> list[str]:
        """Attempting to split words using the Viterbi Algorithm.

        If string is not passed to this function, split attempt will be made on class string.
        Reference: https://stackoverflow.com/questions/195010/how-can-i-split-multiple-joined-words
        """

        raise NotImplementedError("This has not been implemented yet")

    def split_words(self,
                    string: Optional[str] = None,
                    casing: Optional[
                        Literal["PASCAL"] |
                        Literal["SNAKE"]  |
                        Literal["KEBAB"]  |
                        Literal["CAMEL"]] = None,
                    exceptions: Optional[list[str]] = None) -> list[str]:
        """Split words in given string according to provided casing.
        
        If no string is provided, class default will be used.
        If no casing is provided, casing will be identified.
        """

        string = string or self.string
        if casing is None:
            casing = self.identify(string=string)
            if casing is None:
                raise ValueError("Provided string does not follow any known naming conventions")

        word = ""
        words = []

        exceptions_map = {}
        if exceptions is None:
            exceptions = []

        for exception in exceptions:
            while exception in string:
                # To account for multiple instances of the same exception
                next_index = len([... for exc in exceptions_map if exception in exc]) + 1
                exceptions_map[f"{exception}_{next_index}"] = string.find(exception)
                string = (
                    string
                    .replace(exception, "", 1)
                    .replace("-", "", 1)
                    .replace("_", "", 1)
                )

        match casing:
            case "PASCAL":
                for char in string:
                    if char.islower():
                        word += char
                        continue

                    if word == "":
                        word = char
                        continue

                    words.append(word)
                    word = char

            case "SNAKE":
                for char in string:
                    if char != "_":
                        word += char
                        continue

                    words.append(word)
                    word = ""

            case "KEBAB":
                for char in string:
                    if char != "-":
                        word += char
                        continue

                    words.append(word)
                    word = ""

            case "CAMEL":
                for char in string:
                    if char.isupper():
                        words.append(word)
                        word = ""

                    word += char

        words.append(word)
        for exception, exception_index in exceptions_map.items():
            words.insert(exception_index, exception.split("_")[0])

        return words

    def convert(self,
                string: Optional[str] = None,
                from_case: Optional[Literal["PASCAL"] |
                                    Literal["SNAKE"]  |
                                    Literal["KEBAB"]  |
                                    Literal["CAMEL"]  |
                                    Literal["UPPER"]  |
                                    Literal["LOWER"]] = None,
                to_case: Literal["PASCAL"] |
                         Literal["SNAKE"]  |
                         Literal["KEBAB"]  |
                         Literal["CAMEL"] = "SNAKE",
                exceptions: Optional[list[str]] = None):
        """Convert the case of a string to the specified case.

        If parameter is not passed to this function, class string will be converted.
        If from_case is not specified, case will be identified.
        If no discernable case is found, will raise error.
        If to_case is not specified, string will be converted to snake_casing.
        """

        string = string or self.string
        if from_case is None:
            from_case = self.identify(string=string)
            if from_case is None:
                raise ValueError("Provided string does not follow any known naming conventions")

        if from_case in {"UPPER", "LOWER"}:
            words = [string]
        else:
            words = self.split_words(string=string, casing=from_case, exceptions=exceptions)

        match to_case:
            case "SNAKE":
                result = "_".join([
                    word.lower()
                    for word in words
                ])
                return result

            case "CAMEL":
                result = "".join([
                    words[i].capitalize()
                    if i != 0 else words[i].lower()
                    for i in range(len(words))
                ])
                return result

            case "KEBAB":
                result = "-".join([
                    word.lower()
                    for word in words
                ])
                return result

            case "PASCAL":
                result = "".join([word.capitalize() for word in words])
                return result

            case "UPPER":
                result = "".join(words).upper()
                return result

            case "LOWER":
                result = "".join(words).lower()
                return result


def main():
    """Function responsible for changing the casing conventions
    of the provided database tables and column names"""

    load_dotenv()

    database_url = URL.create(
        drivername=os.environ.get("DB_ENGINE", "postgresql+psycopg"),
        username=os.environ.get("PG_DB_USERNAME"),
        password=os.environ.get("PG_DB_PASSWORD"),
        host=os.environ.get("PG_DB_HOST"),
        database=os.environ.get("PG_DB_DATABASE"),
        port=os.environ.get("PG_DB_PORT")
    )
    engine = create_engine(url=database_url)

    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Define custom exceptions here
    # These are useful when we are trying to specify characters that should be kept together
    # Otherwise, this may yield unexpected results
    exceptions = [
        "UUID",
        "URL",
        "MT"
    ]

    for table_name in metadata.tables.keys():
        table_metadata = metadata.tables.get(table_name)

        for column in table_metadata.columns:
            name = column.name
            column_caser = Caser(name)

            try:
                new_name = column_caser.convert(to_case="SNAKE",exceptions=exceptions)
            except ValueError:
                # This is custom to the Money Tribe DB, but could also be used as a general case
                name_split = column.name.split("_")
                new_name = "_".join([
                    Caser(word).convert(to_case="SNAKE",
                                        exceptions=exceptions)
                    for word in name_split
                ])

            query = f'ALTER TABLE "public"."{table_name}" RENAME "{name}" TO "{new_name}"'

            with engine.begin() as conn:
                conn.execute(text(query))
                conn.commit()

            print(f"Changed column name of table {table_name} from {name} to {new_name}")


        table_caser = Caser(table_name)

        try:
            new_table_name = table_caser.convert(to_case="SNAKE", exceptions=exceptions)
        except ValueError:
            # This is custom to the Money Tribe DB, but could also be used as a general case
            name_split = table_name.split("_")
            new_table_name = "_".join([
                Caser(word).convert(to_case="SNAKE",
                                    exceptions=exceptions)
                for word in name_split
            ])

        query = f'ALTER TABLE "public"."{table_name}" RENAME TO "{new_table_name}"'
        with engine.begin() as conn:
            conn.execute(text(query))
            conn.commit()

        print(f"Changed table name {table_name} to {new_table_name}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps(get_traceback(), indent=4))
