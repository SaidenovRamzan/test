
import websockets
import json
import aiohttp
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.simple_row import make_row_keyboard


class ChatState(StatesGroup):
    getting_message = State()
    
router = Router()


@router.message(Command('all_chats'))
async def get_all_my_chats(message: types.Message) -> None:
    async with aiohttp.ClientSession() as session:
            async with session.get(f'http://localhost:8000/api/telegram-chat/{message.chat.id}') as response:
                if response.status == 200:
                    response_text = await response.text()
                    
                    response_data = json.loads(response_text)
                    orders = response_data.get('orders')
                    if not orders:
                        await message.answer("Нет активных чатов")
                    else:
                        for order in orders:
                            builder = InlineKeyboardBuilder()
                            builder.add(types.InlineKeyboardButton(
                                text="Перейти в чат",
                                callback_data=f"connect_chat_{order.get('self_id')}_{order.get('user_id')}_{order.get('user_shelf_id')}")
                            )
                            text = f"Пользователь: {order.get('user_name')}\n"
                            text += f"Книга: {order.get('user_shelf_name')}\n"
                            text += f"Номер объявления: {order.get('user_shelf_id')}\n"
                            await message.answer(text, reply_markup=builder.as_markup()) 
                else:
                    await message.answer(f"Ошибка при отправке запроса: {response.status}")
                    
                    
@router.callback_query(F.data.startswith('connect_chat_'))
async def send_code(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    sender_id = int(data[2])
    recipient_id = int(data[3])
    user_shelf_id = int(data[4])
    url = f"ws://localhost:8000/ws/chat/{sender_id}/{recipient_id}/{user_shelf_id}/"
    await state.set_state(ChatState.getting_message)
    await state.update_data(url=url)
    await callback.message.answer('Введите ваше сообщение')


@router.message(ChatState.getting_message)
async def food_size_chosen_incorrectly(message: types.Message, state: FSMContext):
    if message.text == 'stop':
        await message.reply('stop')
        await state.clear()
    else: 
        data = await state.get_data()
        url = data['url']
        async with websockets.connect(url) as websocket:
            await websocket.send(json.dumps({'message': message.text}))


# async def send_message_to_websocket(message, bot: types.Message):
#     url = "ws://localhost:8000/ws/chat/1/2/1/"
#     async with websockets.connect(url) as websocket:
#         await websocket.send(json.dumps({'message': message}))
        

# @router.message(Command('send_via_websocket'))
# async def send_via_websocket(message: types.Message):
#     await send_message_to_websocket(message="Hello from the bot via WebSocket!", bot=message)
