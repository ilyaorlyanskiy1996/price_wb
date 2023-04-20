import TG_api.core
from telebot import types

bot = TG_api.core.bot


def func_start(message):
    return (message.text == '/start') or (message.text == '/in_home')


@bot.message_handler(func=func_start)
def start(message):
    print(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Добавить товар')
    btn2 = types.KeyboardButton('Показать список моих товаров')
    markup.add(btn1, btn2)
    mess = f'Привет, {message.from_user.first_name}, введите команду'
    bot.send_message(message.chat.id, mess, reply_markup=markup)

@bot.message_handler()
def incorrecte_mess(message):
    printed_info = f'Некорректный ввод'
    bot.send_message(message.chat.id, printed_info)

if __name__=="__main__":
    print(f'Запущено {__name__}')
else:
    print(f'Импортируется {__name__}')