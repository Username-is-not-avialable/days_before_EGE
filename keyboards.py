from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

subjects_keyboard = ReplyKeyboardMarkup(keyboard = (
													["профиль","русский","база"],\
													["физика","химия","информатика"],\
													["биология","история","география"],\
													["английский","обществознание"]
												   ),
										resize_keyboard = True
										)