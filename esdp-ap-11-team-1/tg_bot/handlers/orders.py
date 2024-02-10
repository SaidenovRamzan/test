import json
import aiohttp
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


from keyboards.simple_row import make_row_keyboard


class RentState(StatesGroup):
    getting_confirm_code = State()
    getting_confirm_code_from_renter = State()
    
    
router = Router()


@router.message(Command('my_orders'))
async def get_all_my_orders(message: types.Message) -> None:
    async with aiohttp.ClientSession() as session:
            data = {"id": f"{message.chat.id}"}
            async with session.post('http://localhost:8000/api/telegram-get-my-orders', json=data) as response:
                if response.status == 200:
                    response_text = await response.text()
                    
                    response_data = json.loads(response_text)
                    orders = response_data.get('orders')
                    if not orders:
                        await message.answer("Нет заказов")
                    else:
                        for order in orders:
                            builder = InlineKeyboardBuilder()
                            
                            if order.get('is_ended'):
                                pass
                            
                            elif order.get('is_approved') and order.get('is_started'):
                                builder.add(types.InlineKeyboardButton(
                                    text="Я получил книгу назад",
                                    callback_data=f"send_code_{order.get('id')}")
                                )
                            elif not order.get('is_approved'):
                                builder.add(types.InlineKeyboardButton(
                                    text="Поддтвердить",
                                    callback_data="cancel_order")
                                )
                                builder.add(types.InlineKeyboardButton(
                                    text="Отменить",
                                    callback_data="confirm_order")
                                )
                                
                            text = f"\n\nНомер заказа: {order.get('id')}\nНазвание книги: {order.get('name')}\n"
                            text += f"Дата начала: {order.get('start')} Дата конца: {order.get('end')}\n"
                            text += f"Отправьте этот код получателю, при его получении: {order.get('code')}\n"
                            await message.answer(text.strip(), reply_markup=builder.as_markup()) 
                else:
                    await message.answer(f"Ошибка при отправке запроса: {response.status}")



@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: types.CallbackQuery):
    order_id = callback.message.text.split(":")[1].split('\n')[0].strip()
    await callback.bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id, reply_markup=None)
    async with aiohttp.ClientSession() as session:
            async with session.post(f'http://localhost:8000/api/order/{order_id}/approve') as response:
                if response.status == 200:
                    await callback.message.answer(f"Заказ {order_id} отменен")
                else:
                    await callback.message.answer(f"Заказ {hbold('НЕ')} {order_id} отменен!!!")


@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: types.CallbackQuery):
    order_id = callback.message.text.split(":")[1].split('\n')[0].strip()
    
    await callback.bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id, reply_markup=None)
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://localhost:8000/api/order/{order_id}/approve') as response:
            if response.status == 200:
                await callback.message.answer(f"Заказ {order_id} принят")
            else:
                await callback.message.answer(f"Заказ {hbold('НЕ')} {order_id} принят!!!")
                
            
@router.callback_query(F.data.startswith('send_code'))
async def send_code(callback: types.CallbackQuery):
    order_id = int(callback.data.split('_')[2])
    async with aiohttp.ClientSession() as session:
            async with session.post(f'http://localhost:8000/api/telegram-order/{order_id}/finish-rent') as response:
                if response.status == 200:
                    await callback.message.answer('Заказ завершен')
                else:
                    await callback.message.answer('Код не верный', reply_markup=make_row_keyboard(['stop']))




@router.message(Command('orders'))
async def command_end_handler(message: types.Message) -> None:
    async with aiohttp.ClientSession() as session:
            data = {"id": f"{message.chat.id}"}
            async with session.post('http://localhost:8000/api/telegram-get-orders', json=data) as response:
                if response.status == 200:
                    response_text = await response.text()
                    
                    response_data = json.loads(response_text)
                    orders = response_data.get('orders')
                    
                    if not orders:
                        await message.answer("Нет заказов")
                    else:
                        for order in orders:
                            builder = InlineKeyboardBuilder()
                            
                            if order.get('is_approved') and not(order.get('is_started')):
                                builder.add(types.InlineKeyboardButton(
                                    text="Я получил книгу",
                                    callback_data=f"renter_send_code_{order.get('id')}")
                                )
                            text = f"\n\nНомер заказа: {order.get('id')}\nНазвание книги: {order.get('name')}\n"
                            text += f"Отправьте этот код владельцу кеини, при получении книги: {order.get('code')}\n"
                            text += f"Статус: {'Подтвержден' if order.get('is_approved') else 'В ожидании'}"
                            await message.answer(text.strip(), reply_markup=builder.as_markup()) 
                else:
                    await message.answer(f"Ошибка при отправке запроса: {response.status}")
                    

@router.callback_query(F.data.startswith('renter_send_code_'))
async def send_code(callback: types.CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split('_')[3])
    async with aiohttp.ClientSession() as session:
            async with session.post(f'http://localhost:8000/api/telegram-order/{order_id}/start-rent') as response:
                if response.status == 200:
                    await callback.message.answer('Успешно поддтвердили получение')
                    await state.clear()

                else:
                    await callback.message.answer('Код не верный', reply_markup=make_row_keyboard(['stop']))
