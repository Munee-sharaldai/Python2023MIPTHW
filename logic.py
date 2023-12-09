import telebot
# ... (other imports)

def create_telegram_bot(key, data):
    bot = telebot.TeleBot(key)

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.send_message(message.chat.id, "Привет! Введите название iPhone для получения информации в данном формате: iPhone 15 128GB Blue (Dual Sim), последний параметр может отсутсвовать.")

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        user_input = message.text

        for i in range(len(data[0])):
            if user_input.lower() in data[0][i].lower():
                response_message = (
                    f"Название: {data[0][i]}\n"
                    f"Цена: {data[1][i]}\n"
                    f"Ссылка: https://www.mvideo.ru{data[2][i]}\n"
                    f"Экран: {data[3][i]}\n" 
                    f"Технология экрана: {data[4][i]}\n"
                    f"Тип процессора: {data[5][i]}\n"
                    f"Основная камера: {data[6][i]}\n"
                )
                bot.send_message(message.chat.id, response_message)
                return

        bot.send_message(message.chat.id, "Извините, товар не найден.")

    bot.polling()
