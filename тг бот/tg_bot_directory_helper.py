import telebot
from telebot import types
import config
import json


def load():
    with open('BD.json', 'r', encoding='utf-8') as file:
        bd_local = json.load(file)
        print("БД успешно загружена.")
    return bd_local


def save(data):
    with open('BD.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False))
    print("БД успешно сохранена.")


bot = telebot.TeleBot(config.TOKEN)
contacts = {'Маша': {'phone': '89524578854', 'birthday': '17.11.2001', 'email': 'blabla@gmail.com'}}


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name}! Я бот, который ты ' \
           f'можешь использовать как телефонный справочник.'
    stik = open('AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, stik)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton('/find_contact')
    item_2 = types.KeyboardButton('/add_contact')
    item_3 = types.KeyboardButton('/all_contacts')
    item_4 = types.KeyboardButton('/delete_contact')
    item_5 = types.KeyboardButton('/help')

    markup.add(item_1, item_2, item_3, item_4, item_5)

    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def helper(message):
    mess = 'Я бот, который ты можешь использовать как телефонный справочник. Ты можешь созавать, искать и удалять контакты!'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=['find_contact'])
def get(message):
    send = bot.send_message(message.chat.id, 'Введите имя контакта')
    bot.register_next_step_handler(send, get_name)


def get_name(mes):
    name_get = mes.text
    data_contacts = load()
    try:
        for i in data_contacts[name_get]:
            bot.send_message(mes.chat.id, data_contacts[name_get][i])
    except KeyError:
        bot.send_message(mes.chat.id, 'Не нашли такого человека в Ваших контактах...')


@bot.message_handler(commands=['add_contact'])
def get(message):
    send = bot.send_message(message.chat.id, 'Введите имя, номер телефона, день рождения и почту контакта')
    bot.register_next_step_handler(send, add_contact)


def add_contact(mes):
    info_get = mes.text
    list1 = info_get.split(',')
    try:
        new_dict = {'phone': list1[1], 'birthday': f'{list1[2]}', 'email': f'{list1[3]}'}
        contacts[list1[0]] = new_dict
        save(contacts)
        bot.send_message(mes.chat.id, 'Информация успешно сохранена!')
    except IndexError:
        bot.send_message(mes.chat.id, 'Что-то пошло не так...')
        bot.send_message(mes.chat.id, 'Попробуйте ввести данные таким образом "Петя, 89763564546, 12.01.2001, Petya@gmail.com"')


@bot.message_handler(commands=['all_contacts'])
def get(message):
    data_bd = load()
    for i in data_bd:
        bot.send_message(message.chat.id, i.upper())
        for h in data_bd[i]:
            bot.send_message(message.chat.id, data_bd[i][h])


@bot.message_handler(commands=['delete_contact'])
def get(message):
    send = bot.send_message(message.chat.id, 'Введите имя человека, которого хотите удалить из справочника...')
    bot.register_next_step_handler(send, del_contact)


def del_contact(mes):
    del_name = mes.text
    data_bd = load()
    data_bd.pop(del_name)
    save(data_bd)
    bot.send_message(mes.chat.id, 'Контакт успешно удален!')


bot.polling(none_stop=True)
