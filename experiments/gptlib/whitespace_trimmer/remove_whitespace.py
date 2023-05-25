#!/usr/bin/env python
"""
has a function that takes a markdown document in as a string, and removes any whitespace from any lines that are not inside a code block tag "```" or "```python" etc. If the whitespace is in a code block tag, it leave it alone. It should only remove leading whitespace from the start of the line.
"""


def remove_leading_whitespace(markdown: str) -> str:
    """
    Remove leading whitespace from any line not inside a code block.

    :param markdown: The input markdown document as a string.
    :return: The processed markdown document as a string.
    """
    in_code_block = False
    processed_lines = []

    # Iterate through each line of the markdown document
    for line in markdown.split("\n"):
        # Check for the code block tag
        if line.lstrip().startswith("```"):
            # Toggle the in_code_block flag
            in_code_block = not in_code_block
            line = line.lstrip()

        # Remove leading whitespace if not in a code block
        if not in_code_block:
            line = line.lstrip()

        # Append the processed line to the list
        processed_lines.append(line)

    # Combine the processed lines to form the output markdown string
    return "\n".join(processed_lines)


def main():
    """
    The main function for the remove_whitespace script.
    This is called when the script is run directly.
    """
    # Provide a sample markdown document as input
    sample_markdown = """\
## Example Markdown

This is a sample markdown document.

    This line has leading whitespace.
    
    ```python
    
    if True:
        print("This line is inside a code block and should not be processed.")
    ```
"""

    # Process the sample markdown and remove leading whitespace
    print(remove_leading_whitespace(sample_markdown))


if __name__ == "__main__":
    main()
