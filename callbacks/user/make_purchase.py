from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.types.input_file import FSInputFile

from aiogram.exceptions import TelegramBadRequest
from datetime import datetime
from os import remove

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, update, delete

from database.models.User import User
from database.models.Cart import Cart
from database.models.Product import Product
from database.models.Purchase import Purchase

from sqlalchemy.ext.asyncio.session import AsyncSession

from misc.misc import format_amount_to_text
from loader import logs_chat_id

async def check_total_cart(cart, db: AsyncSession, bot: Bot, id: int) -> dict:
    result = []
    unavailable_count = [] #количество товара слишком большое.
    for cart_product in cart:
        cart_product: Cart
        product_count_available = await db.execute(select(Product.count).where((Product.category == cart_product.category_id) & (Product.id == cart_product.product_id)))
        product_count_available = product_count_available.all()[0][0]
        if product_count_available == 0:
            await bot.send_message(
                chat_id=id,
                text=f'❗ <b>Внимание</b>\n\n'
                f'ℹ Товар <b>{cart_product.name} отсутствует</b> в наличии на данный момент.\n\n'
                f'❗ В покупке он учитываться <b>не</b> будет.'
            )
        if cart_product.count > product_count_available:
            unavailable_count.append({'id': cart_product.id, 'category_id': cart_product.category_id, 'product_id': cart_product.product_id, 'name': cart_product.name, 'cart_count': cart_product.count, 'available_count': product_count_available})
            cart_product.count = product_count_available
            result.append(cart_product)
        else:
            result.append(cart_product)
    amount = sum(p.price * p.count for p in result)
    return {'result': result, 'unavailable_count': unavailable_count, 'amount': amount}

async def make_purchase(callback: CallbackQuery, db: AsyncSession, bot: Bot) -> None:
    if not callback.message.chat.username:
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=f'❗️ <b>Перед покупкой вы должны установить себе имя пользователя, чтобы администратор смог выдать вам товар</b>'
        )
        return
    balance = await db.scalar(select(User.balance).where(User.telegram == callback.message.chat.id))
    cart = await db.scalars(select(Cart).where(Cart.telegram == callback.message.chat.id))

    cart = cart.all()

    if len(cart) > 0:
        cart_data = await check_total_cart(cart, db, bot, callback.message.chat.id)
        result, unavailable_count, amount = cart_data['result'], cart_data['unavailable_count'], cart_data['amount']

        if balance >= amount:
            await db.execute(update(User).where(
                User.telegram == callback.message.chat.id
            ).values(balance = User.balance - amount))
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text='🥳 <b>Благодарим за покупку!</b>\n\n'
                f'☝️ <b>{"Товары будут выданы" if len(cart) > 1 else "Товар будет выдан"} модератором в ближайшее время.</b>'
            )
            try:
                await bot.send_message(
                    chat_id=logs_chat_id,
                    text=f'<b>Пользователь <a href="t.me/{callback.message.chat.username}">{callback.from_user.first_name}</a> приобрел товары на сумму {format_amount_to_text(amount)} ₽.</b>\n'
                    'Список товаров:\n\n' +
                    '\n'.join(f'<b>{product.name}</b> <b>({product.count}</b> шт.)' for product in result)
                )
            except TelegramBadRequest:
                file = f'tmp_{callback.message.chat.id}.txt'
                with open(file, 'w', encoding='utf-8') as tmp:
                    tmp.write(
                        '\n'.join(f'{product.name} ({product.count} шт.)' for product in result)
                    )
                await bot.send_document(
                    chat_id=logs_chat_id,
                    document=FSInputFile(
                        path=file,
                        filename=f'user_{callback.message.chat.id}__{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.txt'
                    ),
                    caption=f'<b>Пользователь <a href="t.me/{callback.message.chat.username}">{callback.from_user.first_name}</a> приобрел товары на сумму {format_amount_to_text(amount)} ₽.</b>\n\n'
                    '❗️ <i>Список товаров приложен в текстовом файле, так как он слишком большой.</i>'
                )
                remove(file)
            for product in result:
                product: Cart
                uc_check = 0
                if await db.scalar(select(Purchase).where((Purchase.product_name == product.name) & (Purchase.product_price == product.price))):
                    await db.execute(
                        update(Purchase).where((Purchase.product_name == product.name) & (Purchase.product_price == product.price)).values(count = Purchase.product_count + product.count)
                    )
                else:
                    db.add(
                        Purchase(
                            telegram=product.telegram,
                            product_name = product.name,
                            product_price = product.price,
                            product_count = product.count
                        )
                    )
                for uc in unavailable_count:
                    if uc['id'] == product.id:
                        await bot.send_message(
                            chat_id=callback.message.chat.id,
                            text=f'❗ <b>Внимание</b>\n\n'
                            f'🔢 Количество <b>{uc["name"]}</b> - <b>{uc["available_count"]}</b> шт.\n'
                            f'🔢 В корзине - <b>{uc["cart_count"]}</b> шт.\n\n'
                            f'❗ В покупке будет указано <b>{uc["available_count"]}</b> шт.'
                        )
                        await db.execute(
                            update(Cart).where(Cart.id == uc['id']).values(count = uc['cart_count'] - uc['available_count'])
                        )
                        await db.execute(
                            update(Product).where((Product.category == uc['category_id']) & (Product.id == uc['product_id'])).values(count = uc['cart_count'] - uc['available_count'])
                        )
                        uc_check = 1
                if not uc_check:
                    await db.execute(delete(Cart).where(Cart.id == product.id))
                    await db.execute(
                        update(Product).where((Product.category == product.category_id) & (Product.id == product.product_id)).values(count = Product.count - product.count)
                    )
        else:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text='<b>😔 Не достаточно денег на балансе!</b>\n\n'
                f'💰 Сумма на балансе - <b>{format_amount_to_text(balance)}</b>₽\n'
                f'💸 Сумма покупки - <b>{format_amount_to_text(amount)}</b>₽\n\n'
                f'💁 <i>Подсказка: Пополнить баланс можно при помощи</i> <b>/start -> 🧍 Профиль -> 💸 Пополнить баланс</b>'
            )
    else:
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=f'❗️ <b>Корзина пуста.</b>\n'
        )