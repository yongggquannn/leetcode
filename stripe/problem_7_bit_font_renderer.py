"""
Bit Font Renderer (Stripe)
Source (paywalled): https://darkinterview.com/collections/t4y7u1i8/questions/b8820dd8-fb20-437c-8aee-e17ac3078bff
Reference: prachub.com "Render Bitmap Font to ASCII Grid" (paywalled),
           1point3acres thread 1132535 (Stripe Bitmap Interview Questions)

Public detail is THIN. Below is the canonical version of this problem family
based on community write-ups; confirm exact wording with your source.

================================================================================
SHARED FONT (used by examples below) - 5 rows x 3 cols, classic 7-seg style
================================================================================

FONT = {
    "0": [[1,1,1], [1,0,1], [1,0,1], [1,0,1], [1,1,1]],
    "1": [[0,1,0], [1,1,0], [0,1,0], [0,1,0], [1,1,1]],
    "2": [[1,1,1], [0,0,1], [1,1,1], [1,0,0], [1,1,1]],
    "3": [[1,1,1], [0,0,1], [1,1,1], [0,0,1], [1,1,1]],
    # ... fill 4-9 similarly
}

================================================================================
PART 1: Render a single digit
================================================================================

Each digit '0'..'9' is described as a 2D grid of bits (1 = pixel on,
0 = pixel off), all the same dimensions H x W. Render it to an ASCII grid
using '#' for 1 and ' ' (space) for 0. Return as a list of strings.

Example:
    render_digit(FONT, "1") == [
        " # ",
        "## ",
        " # ",
        " # ",
        "###",
    ]

    render_digit(FONT, "0") == [
        "###",
        "# #",
        "# #",
        "# #",
        "###",
    ]

================================================================================
PART 2: Render a multi-digit string
================================================================================

Given a string of digits, render side-by-side with a 1-column space gap
between digits. Return list of row strings.

Example:
    render_string(FONT, "12") == [
        " #     # ",   # cols: digit "1" (3) + gap (1) + ... wait, see below
        "##  # # ",
        ...
    ]

    Concretely with our 3-wide font and 1 space between digits, "12" is 7
    columns wide (3 + 1 + 3):
    render_string(FONT, "12") == [
        " #  ###",
        "##    #",
        " #  ###",
        " #  #  ",
        "### ###",
    ]

================================================================================
PART 3 (typical follow-ups - confirm with source)
================================================================================

Likely scaling extension. Each pixel becomes a kxk block of '#' or ' '.

Example with scale=2 on digit "1":
    render_string_scaled(FONT, "1", 2) == [
        "  ##  ",
        "  ##  ",
        "####  ",
        "####  ",
        "  ##  ",
        "  ##  ",
        "  ##  ",
        "  ##  ",
        "######",
        "######",
    ]
    # 5 source rows * 2 = 10 rows, 3 source cols * 2 = 6 cols

NOTE: Open the actual problem to fix the input format (the font may arrive as
a hex/binary string, a list of ints, or a multi-line string of '#'/'.' rather
than a 2D bit array).
"""


def render_digit(font: dict, digit: str) -> list[str]:
    pass


def render_string(font: dict, text: str) -> list[str]:
    pass


def render_string_scaled(font: dict, text: str, scale: int) -> list[str]:
    pass


if __name__ == "__main__":
    pass
