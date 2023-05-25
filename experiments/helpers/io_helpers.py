#!/usr/bin/env python
"""
Auto-comment-and-document
"""
from experiments.helpers.terminal_color_helper import fg, BG_DEFAULT_COLOR, FG_DEFAULT_COLOR


def multiline_input(user_prompt: str = "> ", input_fn=input) -> str:
    """
    Obtain multiline input from the user.
    Upon encountering "<<<EOF" at the end of a line, the function will continue accepting input until
    the user types "EOF" on a new line.

    :param user_prompt: The prompt to display to the user.
    :return: The user's input as a single string with newline characters.
    """
    # Set the terminal foreground color.
    print(fg(0, 1, 0))

    # Get the user input, if EOFError occurs, set input as "exit".
    try:
        user_input = input_fn(user_prompt)
    except EOFError:
        user_input = "exit"

    # If the user input ends with "<<EOF", process multiline input.
    if user_input.endswith("<<EOF"):
        # Remove the "<<EOF" from the user input.
        user_input = user_input[:-5]
        input_lines = []

        # Keep accepting input until "EOF" is entered.
        while user_input != "EOF":
            input_lines.append(user_input)
            try:
                user_input = input_fn("")
            except EOFError:
                user_input = "EOF"

        # Join the input_lines into a single string with newline characters.
        user_input = "\n".join(input_lines)

    # Reset the terminal background and foreground colors.
    print(BG_DEFAULT_COLOR + FG_DEFAULT_COLOR)

    return user_input
