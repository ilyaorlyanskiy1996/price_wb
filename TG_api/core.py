import telebot
import os
from telebot import types
import site_api.utils.site_api_handler
import databases.utils.CRUD
from dotenv import load_dotenv
load_dotenv()
token_telebot = os.getenv('token_telebot')

bot = telebot.TeleBot(token_telebot)
my_reg_exp = str()

@bot.message_handler(commands=['start', 'in_home'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Добавить товар')
    btn2 = types.KeyboardButton('Показать список моих товаров')
    markup.add(btn1, btn2)
    mess = f'Привет, {message.from_user.first_name}, введите команду'
    bot.send_message(message.chat.id, mess, reply_markup=markup)

def func_plus(message):
    return message.text == 'Добавить товар'

def func_all(message):
    return message.text == 'Показать список моих товаров'

def func_delete(message):
    return message.text == 'Удалить товар'

def func_delete_all(message):
    return message.text == 'Удалить все'


@bot.message_handler(func=func_plus)
def plus(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup_1 = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('/in_home')
    btn2 = types.InlineKeyboardButton(text='Перейти', url='https://www.wildberries.ru/')
    markup.add(btn1)
    markup_1.add(btn2)
    bot.send_message(message.chat.id, 'Выберите товар', reply_markup=markup_1)
    send = bot.send_message(message.chat.id, 'Введите URL товара', reply_markup=markup)
    bot.register_next_step_handler(send, add_url)


@bot.message_handler(func=func_all)
def all(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    sent = databases.utils.CRUD.all_orders(message.from_user.id)
    if len(sent) > 0:
        btn1 = types.KeyboardButton('/in_home')
        btn2 = types.KeyboardButton('Удалить товар')
        btn3 = types.KeyboardButton('Удалить все')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Cписок добавленных товаров', reply_markup=markup)
        for i_key, i_value in sent.items():
            printed_info = f'{i_key}: {sent[i_key][1]}, {sent[i_key][3]} руб.'
            bot.send_message(message.chat.id, printed_info)
    else:
        btn1 = types.KeyboardButton('/in_home')
        markup.add(btn1)
        bot.send_message(message.chat.id, 'Cписок пуст', reply_markup=markup)


@bot.message_handler(func=func_delete)
def delete(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('/in_home')
    markup.add(btn1)
    sent = bot.send_message(message.chat.id, 'Введите номер удаляемого товара', reply_markup=markup)
    bot.register_next_step_handler(sent, delete_order)

@bot.message_handler(func=func_delete_all)
def delete_all(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('/in_home')
    markup.add(btn1)
    if databases.utils.CRUD.delete_all_data(message.from_user.id):
        bot.send_message(message.chat.id, 'Список очищен', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Товаров в списке нет', reply_markup=markup)


def add_url(message):
    if message.text == '/in_home':
        start(message)
    else:
        try:
            url = site_api.utils.site_api_handler.take_url(message.text)
            site_api.utils.site_api_handler.search_json(url)
            data = site_api.utils.site_api_handler.take_data(url)
            original_url = message.text.split('\n')[-1]
            if databases.utils.CRUD.store_data(message.from_user.id, data[0], data[1], data[2], data[3], data[4], original_url):
                send = bot.send_message(message.chat.id, 'Товар добавлен')
                bot.register_next_step_handler(send, add_url)
            else:
                send = bot.send_message(message.chat.id, 'Товар уже есть')
                bot.register_next_step_handler(send, add_url)
        except:
            printed_info = f'Некорректный ввод'
            bot.send_message(message.chat.id, printed_info)


def delete_order(message):
    if message.text == '/in_home':
        start(message)
    else:
        try:
            databases.utils.CRUD.delete_data(int(message.text), message.from_user.id)
        except:
            printed_info = f'Некорректный ввод'
            sent = bot.send_message(message.chat.id, printed_info)
            bot.register_next_step_handler(sent, delete_order)
        else:
            printed_info = f'Товар удален'
            bot.send_message(message.chat.id, printed_info)
            printed_info = f'Оставшиеся товары:'
            send = bot.send_message(message.chat.id, printed_info)
            sent = databases.utils.CRUD.all_orders(message.from_user.id)
            if len(sent) > 0:
                for i_key, i_value in sent.items():
                    printed_info = f'{i_key}: {sent[i_key][1]}, {sent[i_key][3]} руб.'
                    bot.send_message(message.chat.id, printed_info)
                printed_info = f'Введите номер удаляемого товара'
                bot.send_message(message.chat.id, printed_info)
                bot.register_next_step_handler(send, delete_order)
            else:
                printed_info = f'Список пуст'
                bot.send_message(message.chat.id, printed_info)



@bot.message_handler()
def incorrecte_mess(message):
    printed_info = f'Некорректный ввод'
    bot.send_message(message.chat.id, printed_info)

def create_message(users_id, order_brand, order_name, order_id, old_price, new_price, url_order, url_order_original):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Перейти', url=url_order_original)
    markup.add(btn1)
    printed_info = f'Изменение цены:\n {order_brand} {order_name} {order_id}. {old_price} руб. -> {new_price} руб.'
    bot.send_message(users_id, printed_info, reply_markup=markup)

def create_message_error():
    printed_info = f'Ошибка в боте, выключаюсь!'
    bot.send_message('1604211187', printed_info)

if __name__=="__main__":
    start()
    func_plus()
    func_all()
    func_delete()
    func_delete_all()
    plus()
    all()
    delete()
    delete_all()
    add_url()
    delete_order()
    incorrecte_mess()
    create_message()
    create_message_error()
else:
    print(f'Импортируется {__name__}')