import TG_api.core
import databases.utils.CRUD
import TG_api
from telebot import types
from TG_api.Client_part.client_func.client_func import add_url, delete_order, delete_all_orders

bot = TG_api.core.bot


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
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn4 = types.InlineKeyboardButton(text='Перейти', url=sent[i_key][4])
            markup.add(btn4)
            printed_info = f'{i_key}: {sent[i_key][1]}, {sent[i_key][3]} руб.'
            bot.send_message(message.chat.id, printed_info, reply_markup=markup)
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
    btn1 = types.KeyboardButton('Да')
    btn2 = types.KeyboardButton('Нет')
    markup.add(btn1, btn2)
    sent = bot.send_message(message.chat.id, 'Вы уверены?', reply_markup=markup)
    bot.register_next_step_handler(sent, delete_all_orders)


def create_message(users_id, order_brand, order_name, order_id, old_price, new_price, url_order, url_order_original):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Перейти', url=url_order_original)
    markup.add(btn1)
    printed_info = f'Изменение цены:\n {order_brand} {order_name} {order_id}. {old_price} руб. -> {new_price} руб.'
    bot.send_message(users_id, printed_info, reply_markup=markup)


if __name__ == "__main__":
    print(f'Запущено {__name__}')
else:
    print(f'Импортируется {__name__}')
