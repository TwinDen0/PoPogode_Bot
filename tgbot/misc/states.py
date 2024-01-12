from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
	pref_coord = State()
	location = State()
	weather = State()
	set_reminder = State()



class AdminStates(StatesGroup):
	start = State()