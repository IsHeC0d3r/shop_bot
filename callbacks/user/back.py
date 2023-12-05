from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.filters import CommandObject

from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio.session import AsyncSession

from callbacks.admin.apurchases import apurchases

from callbacks.user.categories import categories
from callbacks.user.products import products
from callbacks.user.product import product
from callbacks.user.cart import cart

from handlers.user.profile import profile
from handlers.admin.afind import afind

async def back(callback: CallbackQuery, db: AsyncSession, bot: Bot) -> None:
    async def call_delete_prev_message():
        await bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
    
    if len(callback.data.split('back_')) > 1:
        args = callback.data.split('_')

        match(args[1]):
            case 'apurchases':
                await apurchases(
                    callback=CallbackQuery(
                        id=callback.id,
                        from_user=callback.from_user,
                        chat_instance=callback.chat_instance,
                        message=callback.message,
                        data='_'.join(args[1:])
                    ),
                    bot=bot,
                    db=db
                )
            case 'categories':
                await categories(
                    callback=CallbackQuery(
                        id=callback.id,
                        from_user=callback.from_user,
                        chat_instance=callback.chat_instance,
                        message=callback.message,
                        data='_'.join(args[1:])
                    ),
                    bot=bot,
                    db=db
                )
            case 'category':
                await products(
                    callback=CallbackQuery(
                        id=callback.id,
                        from_user=callback.from_user,
                        chat_instance=callback.chat_instance,
                        message=callback.message,
                        data='_'.join(args[1:])
                    ),
                    bot=bot,
                    db=db
                )
            case 'product':
                await product(
                    callback=CallbackQuery(
                        id=callback.id,
                        from_user=callback.from_user,
                        chat_instance=callback.chat_instance,
                        message=callback.message,
                        data='_'.join(args[1:])
                    ),
                    bot=bot,
                    db=db
                )
            case 'cart':
                await cart(
                    callback=CallbackQuery(
                        id=callback.id,
                        from_user=callback.from_user,
                        chat_instance=callback.chat_instance,
                        message=callback.message,
                        data='_'.join(args[1:])
                    ),
                    bot=bot,
                    db=db
                )
            case 'profile':
                await call_delete_prev_message()
                await profile(callback.message, db)
            case 'aprofile':
                await call_delete_prev_message()
                await afind(callback.message, CommandObject(args=args[2]), db)
            case _:
                pass
    else:
        await call_delete_prev_message()

async def cancel(callback: CallbackQuery, db: AsyncSession, bot: Bot, state: FSMContext) -> None:
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text='<b>Действие было отменено. Для дальнейшего взаимодействия с ботом введите /start, либо воспользуйтесь клавиатурой.</b>'
    )
    await state.clear()

async def skip(callback: CallbackQuery, db: AsyncSession, bot: Bot, state: FSMContext) -> None:
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text='<b>Действие было успешно выполнено. Для дальнейшего взаимодействия с ботом введите /start, либо воспользуйтесь клавиатурой.</b>'
    )
    await state.clear()