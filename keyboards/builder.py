from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

class Mode(Enum):
    REPLY = 0, # Под input
    INLINE = 1 # В сообщении

"""
Examples:
    1. Reply keyboard
        reply_keyboard = [
            [
                ['button_0'],
                ['button_1']
            ],
            [
                ['button_2']
            ]
        ]
        simple_keyboard_builder(
            keyboard=reply_keyboard,
            mode=Mode.REPLY,
            input_field_placeholder='Simple placeholder'
        )
    2. Inline keyboard
        inline_keyboard = [
            [
                ['button_0', 'callback_data_0'],
                ['button_1', 'callback_data_1']
            ],
            [
                ['button_2', 'callback_data_2']
            ]
        ]
        simple_keyboard_builder(
            keyboard=inline_keyboard,
            mode=Mode.INLINE
        )
"""
def simple_keyboard_builder(keyboard: list, mode: Mode, input_field_placeholder = 'By @IsHeCoder') -> None | ReplyKeyboardMarkup | InlineKeyboardMarkup:
    """
    By @IsHeCoder.
    Simple keyboard builder. Can build KeyboardButton and InlineKeyboardButton only with text or callback_data. You can view examples in builder.py .
    :param list:
    :param mode:
    :param input_field_placeholder:
    :return ReplyKeyboardMarkup | InlineKeyboardMarkup:
    """
    match mode:
        case Mode.REPLY:
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=item[0]) for item in row] for row in keyboard],
                resize_keyboard=True,
                input_field_placeholder=input_field_placeholder
            )
        case Mode.INLINE:
            return InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=item[0], callback_data=item[1]) if not item[1].startswith('__url__') else InlineKeyboardButton(text=item[0], url=item[1].split('__url__')[1]) for item in row] for row in keyboard],
            )
        case _:
            print('[SIMPLE KEYBOARD BUILDER]: Unknown mode!')
            print('Excepted at')
            print(keyboard)
            print(f'Selected mode - {mode}')

"""
Examples:
    1. Reply keyboard
        reply_keyboard = [
            [
                KeyboardButton(text='button_0'),
                KeyboardButton(text='button_1')
            ],
            [
                KeyboardButton(text='button_2')
            ]
        ]
        keyboard_builder(
            keyboard=reply_keyboard,
            mode=Mode.REPLY,
            input_field_placeholder='Simple placeholder'
        )
    2. Inline keyboard
        inline_keyboard = [
            [
                InlineKeyboardButton(text='button_0', callback_data='callback_data_0'),
                InlineKeyboardButton(text='button_1', callback_data='callback_data_1')
            ],
            [
                InlineKeyboardButton(text='button_2', callback_data='callback_data_2')
            ]
        ]
        keyboard_builder(
            keyboard=inline_keyboard,
            mode=Mode.INLINE
        )
"""
def keyboard_builder(keyboard: list, mode: Mode, input_field_placeholder = 'By @IsHeCoder') -> None | ReplyKeyboardMarkup | InlineKeyboardMarkup:
    """
    By @IsHeCoder.
    Keyboard builder. Can build KeyboardButton and InlineKeyboardButton. You can view examples in builder.py .
    :param list:
    :param mode:
    :param input_field_placeholder:
    :return ReplyKeyboardMarkup | InlineKeyboardMarkup: 
    """
    match mode:
        case Mode.REPLY:
            return ReplyKeyboardMarkup(
                keyboard=keyboard,
                resize_keyboard=True,
                input_field_placeholder=input_field_placeholder
            )
        case Mode.INLINE:
            return InlineKeyboardMarkup(
                inline_keyboard=keyboard,
            )
        case _:
            print('[KEYBOARD BUILDER]: Unknown mode!')
            print('Excepted at')
            print(keyboard)
            print(f'Selected mode - {mode}')