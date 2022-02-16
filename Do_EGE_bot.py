from bs4 import BeautifulSoup
import requests
from aiogram import Bot, Dispatcher, executor, types


def get_days(): # возвращет количество дней оставшихся до ЕГЭ по русскому
				# формат: int
				# парсит с сайта https://countdownz.ru/EGE/countdown/c2hbl9z3Xng1icEM


	url = 'https://countdownz.ru/EGE/countdown/c2hbl9z3Xng1icEM'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}

	page = requests.get(url,headers = headers).text
	soup = BeautifulSoup(page, 'html.parser')
	phrase = soup.find('h1').text.split() 
	days_Rus = int(phrase[2])-21 # сайт считает дни до 20 июня, мне надо до 30 мая

	return days_Rus

def sklonenie(number): # возвращает строку "n дней" или "n дня" или "n день"
	n = number %100
	if 5 <= n <= 20:
		return str(number)+ 'дней'
	last_digit = str(number)[-1]
	dney = ['0','5','6','7','8','9']
	den = ['1']
	dnya = ['2','3','4']
	if last_digit in dney:
		return str(number)+' дней'
	elif last_digit in den:
		return str(number)+' день'
	else:
		return str(number)+' дня'

TOKEN = open('TOKEN.txt').readline()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands = ['start', 'help'])  # команды start и help
async def send_helper(message: types.Message):

	await message.answer('Привет! Я бот, который позволит тебе '+\
						 'контролировать время, оставшееся до ЕГЭ 2022 '+\
						 'по русскому языку. Отправь любое '+\
						 'сообщение, чтобы узнать.')

@dp.message_handler()								# обработка всех сообщений
async def echo(message: types.Message):

	await message.answer(f'До ЕГЭ осталось {sklonenie(get_days())}')





if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)

	
