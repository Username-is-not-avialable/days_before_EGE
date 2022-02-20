from bs4 import BeautifulSoup
import requests
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from keyboards import *

def get_days(): # возвращет количество дней оставшихся до ЕГЭ по русскому
				# формат: int
				# парсит с сайта https://countdownz.ru/EGE/countdown/c2hbl9z3Xng1icEM


	url = 'https://countdownz.ru/EGE/countdown/c2hbl9z3Xng1icEM'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}

	page = requests.get(url,headers = headers).text
	soup = BeautifulSoup(page, 'html.parser')
	phrase = soup.find('h1').text.split() 
	days_Rus = int(phrase[2])-21 # на сайте отсчет до 20 июня, мне надо до 30 мая

	return days_Rus



def Rus_to_other(days_Rus, subject):
	

	difference_with_rus = {'math_prof':3,'math_base':4,'physics':7,\
						   'chemistry':-4, 'inform':21,'biology':15,'history':7,\
						   'geography': -4, 'english':15, 'soc_studies':10 }
	return days_Rus + difference_with_rus[subject]




def sklonenie(number): # возвращает строку "n дней" или "n дня" или "n день"

	if 5 <= number%100 <= 20:
		return str(number)+ ' дней'

	n = number%10

	if n == 1:
		return str(number)+' день'
	if n > 4:
		return str(number)+' дней' 
	else:
		return str(number)+ ' дня'


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands = ['start', 'help'])  # команды start и help
async def send_helper(message: types.Message):

	await message.answer('Привет! Я бот, который позволит '+\
						 'контролировать время, оставшееся до ЕГЭ 2022. '+\
						 'Какой предмет вас интересует?', reply_markup = subjects_keyboard)
						 

@dp.message_handler()								# обработка всех сообщений
async def answerer(message: types.Message):

	text = message.text.lower()
	if 'рус' in text:
		await message.answer(f'До ЕГЭ по русскому языку осталось {sklonenie(get_days())}')
	elif 'проф' in text:
		await message.answer(f'До профильного ЕГЭ по математике осталось {sklonenie(Rus_to_other(get_days(),"math_prof"))}')
	elif 'база' in text:
		await message.answer(f'До базового ЕГЭ по математике осталось {sklonenie(Rus_to_other(get_days(),"math_base"))}')
	elif 'физ' in text:
		await message.answer(f'До ЕГЭ по физике осталось {sklonenie(Rus_to_other(get_days(),"physics"))}')
	elif 'хим' in text:
		await message.answer(f'До ЕГЭ по химии осталось {sklonenie(Rus_to_other(get_days(),"chemistry"))}')
	elif 'инф' in text:
		await message.answer(f'До ЕГЭ по информатике осталось {sklonenie(Rus_to_other(get_days(),"inform"))}')
	elif 'био' in text:
		await message.answer(f'До ЕГЭ по биологии осталось {sklonenie(Rus_to_other(get_days(),"biology"))}')
	elif 'ист' in text:
		await message.answer(f'До ЕГЭ по истории осталось {sklonenie(Rus_to_other(get_days(),"history"))}')
	elif 'гео' in text:
		await message.answer(f'До ЕГЭ по географии осталось {sklonenie(Rus_to_other(get_days(),"geography"))}')
	elif 'анг' in text:
		await message.answer(f'До ЕГЭ по английскому языку(письменная часть) осталось {sklonenie(Rus_to_other(get_days(),"english"))}')
	elif 'общ' in text:
		await message.answer(f'До ЕГЭ по обществознанию осталось {sklonenie(Rus_to_other(get_days(),"soc_studies"))}')


	else:
		await message.answer('*Неизвестная команда.*\n\nВведите одно из ключевых слов:\n\n\u2713 проф (профильная математика)'+\
																						   "\n\u2713 рус"+\
																					 	   "\n\u2713 база (базовая математика)"+\
																					  	   "\n\u2713 физ"+\
																					  	   "\n\u2713 хим"+\
																					  	   "\n\u2713 инф"+\
																					  	   "\n\u2713 био"+\
																					  	   "\n\u2713 ист"+\
																					  	   "\n\u2713 гео"+\
																					  	   "\n\u2713 анг"+\
																					  	   "\n\u2713 общ",
																					  	   parse_mode = 'markdown')

		#мат-проф, матБ, физ, хим, инф, био, ист, гео, анг, общ





if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)

	
