from experiments.helpers.terminal_color_helper import fg, BG_DEFAULT_COLOR, FG_DEFAULT_COLOR


def multiline_input(user_prompt="> ") -> str:
    print(fg(0, 1, 0))
    try:
        user_input = input(user_prompt)
    except EOFError:
        user_input = "exit"
    if user_input.endswith("<<EOF"):
        user_input = user_input[:-5]
        input_lines = []
        while user_input != "EOF":
            input_lines.append(user_input)
            try:
                user_input = input("")
            except EOFError:
                user_input = "EOF"
        user_input = "\n".join(input_lines)
    print(BG_DEFAULT_COLOR + FG_DEFAULT_COLOR)
    return user_input
