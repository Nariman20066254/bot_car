import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import g4f

# Установка политики Event Loop для Windows
asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

# Функция для обработки запроса и получения ответа от API
async def get_car_part_info(messages: list) -> str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4o_mini,
        messages=messages
    )
    return response

# Обработка команд "/start" и "/help"
async def start(update: Update, context):
    await update.message.reply_text("Привет! Напишите модель машины, и я постараюсь найти информацию.")

# Обработка текстовых сообщений
async def handle_message(update: Update, context):
    user_message = update.message.text
    question = f"""
{user_message}
Производитель	
Тип	
Назначение	
Марка	
Модель напиши все на которые подходит
Двигатель напиши все на которыеподходит
Обьем напиши объемы которые подходят 
Год	
Артикул оставт пустым
Номер OEM отсавь пустым 
напиши Вес 	
напиши Длину
напиши Высоту
напиши Ширину 
и в концу напиши на 150 слов мини описание
заполни эти данные
"""

    # Отправляем сообщение о сборе информации
    await update.message.reply_text("Идет сбор информации, пожалуйста, подождите...")
    
    # Обработка запроса и получение ответа от API
    messages = [{"role": "user", "content": question}]
    answer = await get_car_part_info(messages=messages)
    messages.append({"role": "assistant", "content": answer})

    # Отправляем результат пользователю
    await update.message.reply_text(answer)

def main():
    # Введите ваш токен бота здесь
    TOKEN = '7095244087:AAEiRoEGfDp6Nvu_66cVvoh0J_IuNfXWSQ8'
    
    # Создание приложения Telegram
    application = Application.builder().token(TOKEN).build()
    
    # Обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
