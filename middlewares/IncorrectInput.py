from typing import Any, Awaitable, Callable, Dict, Optional, Set
from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, Update, Message, CallbackQuery

from states.UserStates import UserState
from states.AdminStates import AdminState

from misc.misc import format_text_to_amount

class IncorrectInput(BaseMiddleware):
    def setup(
        self: BaseMiddleware, router: Dispatcher, exclude: Optional[Set[str]] = None
    ) -> BaseMiddleware:
        """
        Register middleware for all events in the Router

        :param router:
        :param exclude:
        :return:
        """
        if exclude is None:
            exclude = set()
        exclude_events = {"update", *exclude}
        for event_name, observer in router.observers.items():
            if event_name in exclude_events:
                continue
            observer.outer_middleware(self)
        return self

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        state = await data['state'].get_state()
        if state:
            if state in (UserState.input_amount, UserState.input_products_count, AdminState.givemoney, AdminState.add_category, AdminState.change_price, AdminState.change_count, AdminState.alert_user):
                if isinstance(event, CallbackQuery) and not event.data.startswith('cancel'):
                    await event.answer('Вам не доступна эта функции, пока вы вводите данные.')
                    return
            if isinstance(event, Message):
                if state in (UserState.input_amount, UserState.input_products_count, AdminState.givemoney, AdminState.change_price, AdminState.change_count):
                    if not format_text_to_amount(event.text):
                        await event.answer('Вы ввели не правильное значение. Посмотрите подсказку и попробуйте ещё раз.')
                        return
                elif state in (AdminState.add_category,):
                    if len(event.text) > 50:
                        await event.answer(
                            text='❗️ <b>Вы ввели недопустимое значение.</b>\n\n'
                            '💁 <i>Подсказка: текст не должен содержать больше 50 символов.</i>')
                        return
        return await handler(event, data)