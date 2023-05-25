#!/usr/bin/env python

import math

SIZE = 80
WIDTH = SIZE * 2
HEIGHT = SIZE
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

BG_COLOR_PREFIX = str(b"\x1b[48;2;", encoding="utf-8")
BG_DEFAULT_COLOR = str(b"\x1b[49m", encoding="utf-8")

FG_COLOR_PREFIX = str(b"\x1b[38;2;", encoding="utf-8")
FG_DEFAULT_COLOR = str(b"\x1b[39m", encoding="utf-8")


def f_to_i(rf, gf, bf):
    r, g, b = int(rf * 255), int(gf * 255), int(bf * 255)
    if r < 0 or g < 0 or b < 0:
        r, g, b = 255, 255, 255
    elif r > 255 or g > 255 or b > 255:
        r, g, b = 0, 0, 0
    return r, g, b


def fg(rf, gf, bf):
    r, g, b = f_to_i(rf, gf, bf)
    return FG_COLOR_PREFIX + f"{r};{g};{b}m"


def bg(rf, gf, bf):
    r, g, b = f_to_i(rf, gf, bf)
    return BG_COLOR_PREFIX + f"{r};{g};{b}m"


def bias(rf, gf, bf, biasf):
    return rf + biasf, gf + biasf, bf + biasf


def main():
    max_dist_from_mid = math.dist((0.5, 0.5), (0, 0))
    for y in range(HEIGHT + 1):
        for x in range(WIDTH + 1):
            dist_from_mid = math.dist((0.5, 0.5), (x / WIDTH, y / HEIGHT))
            rf = ((WIDTH - x) * y) / (WIDTH * HEIGHT)
            gf = (x * y) / (WIDTH * HEIGHT)
            bf = (x * (HEIGHT - y)) / (WIDTH * HEIGHT)
            rf, gf, bf = bias(rf, gf, bf, max_dist_from_mid - dist_from_mid)

            cell_color = fg(rf, gf, bf) + bg(1 - rf, 1 - gf, 1 - bf)
            print(cell_color, end=" ")
        print(BG_DEFAULT_COLOR + FG_DEFAULT_COLOR)
    print()


if __name__ == "__main__":
    main()
