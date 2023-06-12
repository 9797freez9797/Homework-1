import os
import logging
import random

from aiogram import Bot, Dispatcher, executor, types
from decouple import config

API_TOKEN = config('TELEGRAM_BOT_TOKEN')

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Определение функции для генерации клавиатуры
def generate_keyboard(examples):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for example in examples:
        keyboard.add(example)
    return keyboard

# Глобальные переменные
examples = []
expected_result = None

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    global expected_result, examples
    examples = []
    text = 'Привет!\n'
    operations = ['+', '-', '*', '/']

    # Генерация 4 случайных примеров
    for i in range(4):  
        mathematical_operation1 = random.choice(operations)
        mathematical_operation2 = random.choice(operations)
        number1 = random.randint(0, 99)
        number2 = random.randint(0, 99)
        number3 = random.randint(0, 99)
        example = f"{number1} {mathematical_operation1} {number2} {mathematical_operation2} {number3}"
        examples.append(example)
    
    random_example = random.choice(examples)  # Выбор случайного примера

    expected_result = eval(random_example)  # Определение ожидаемого результата примера
    text = f"Выбери пример, в котором результат равен {expected_result}"

    keyboard = generate_keyboard(examples)
    await message.reply(text, reply_markup=keyboard)

# Обработчик ответов пользователя
@dp.message_handler(lambda message: message.text in examples)
async def check_answer(message: types.Message):
    global expected_result
    user_answer = message.text
    if eval(user_answer) == expected_result:
        response = 'Верно! Правильный ответ.'
    else:
        response = 'Неверно! Попробуй еще раз.'
    await message.reply(response)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)