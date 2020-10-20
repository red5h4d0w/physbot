from enum import Enum


class _StringEnum:
    def __str__(self):
        return self.value


Alphabet = Enum(
    'Alphabet',
    {
        chr(char): chr(emoji) for char, emoji in zip(
            range(ord('A'), ord('Z') + 1),
            range(0x1F1E6, 0x1F200)  # :regional_indicator_#:
        )
    },
    type=_StringEnum,
)


class Hangman(_StringEnum, Enum):
    BLACK = '\U00002B1B'  # :black_large_square:
    DIZZY_FACE = '\U0001F635'  # :dizzy_face:
    SHIRT = '\U0001F455'  # :shirt:
    POINT_LEFT = '\U0001F448'  # :point_left:
    POINT_RIGHT = '\U0001F449'  # :point_right:
    JEANS = '\U0001F456'  # :jeans:
    SHOE = '\U0001F45E'  # :mans_shoe:
    BLANK = '\U000023F9'  # :stop_button:
