from .builder import Mode, simple_keyboard_builder

kb_start = simple_keyboard_builder(
    [
        [
            ['🧍 Профиль'],
            ['🛍 Товары']
        ],
        [
            ['🔗 Обратная связь']
        ]
    ],
    Mode.REPLY
)