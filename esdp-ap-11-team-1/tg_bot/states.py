from aiogram.fsm.state import StatesGroup, State


class RentState(StatesGroup):
    getting_confirm_code = State()
    getting_confirm_code_from_renter = State()
    
