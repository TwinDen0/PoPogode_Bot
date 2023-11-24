from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
	location = State()



class AdminStates(StatesGroup):
	start = State()