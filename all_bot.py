import telebot
import json
import requests
from telebot import types
from extensions import *

bot = telebot.TeleBot(tok)


# функция печати актуальных курсов валют
def printValue(value, buy, sale):
    return "Курс " +'💰' + str(value) + ' покупка ' + str(buy[:5]) + " продажа " + str(sale[:5])

# клавиатура бота для печати курса валют и перехода в вычисление цен по валютам
markup_menu = types.ReplyKeyboardMarkup( resize_keyboard = True, row_width = 2)
btnCurrency = types.KeyboardButton('Валюта')
btnWeather = types.KeyboardButton('Курс Валют')
markup_menu.add(btnWeather, btnCurrency)
# спомагательная клавиатура бота для удобства, пользователь может не вводить данные,
# а нажать на клавиатуру если ему подходят цифры
inline_menu = types.InlineKeyboardMarkup(row_width=1)
btnEURO = types.InlineKeyboardButton(text='Перевод 100 Евро в Долары', callback_data="EUR USD 100")
btnUSD = types.InlineKeyboardButton(text='Перевод 100 Доларов в Евро',callback_data="USD EUR 100")
btnRUB = types.InlineKeyboardButton(text='Перевод 100 Рублей в Долары', callback_data="RUR USD 100")
btnUAH = types.InlineKeyboardButton(text='Перевод 100 Гривень в Рубль',callback_data="UAH RUR 100")
inline_menu.add(btnRUB, btnUAH, btnUSD, btnEURO)

# Ответ бота на ввод команд
@bot.message_handler(commands=['start','help','values'])
def bot_com(message):
    Currency ="Валюты для обработки :"
    for i in Key_C2.keys():
        Currency = "\n".join((Currency,i))
    if message.text == '/start' or message.text == '/help':
        bot.reply_to(message, f'{RULES} {message.chat.first_name}', reply_markup=markup_menu )
    else:
        bot.reply_to (message, f'\n{Currency} \n {message.chat.first_name}')

# Ответ бота на ввод с клавиатуры текста
@bot.message_handler(content_types=['text'])
def currensy_value(message):
    try:
        if message.text == "Курс Валют":
            res = requests.get(url).json()
            for values in res:
                for n, a in Key_C2.items():
                    if a == values['ccy']:
                        name = n
                        bot.send_message(message.chat.id, printValue(name, values['buy'], values['sale']))
        elif message.text == 'Валюта':
            bot.send_message(message.chat.id, "Для расчета Валюты необходимо ввести через пробел валюту какую переводим"
                                              " валюту в какую переводим и суму перевода", reply_markup=inline_menu)
        elif len(message.text.split(' ')) == 3:
            value = message.text.upper().split(' ')
            base, quote, amount = value
            t = Currency(base, quote, int(amount))
            bot.send_message(message.chat.id, t)
        else:
            raise CurrencyErrorFail
    except CurrencyErrorExept as e:
        bot.send_message(message.chat.id, e)
    except ValueError:
        bot.send_message(message.chat.id, "Введите пожалуйста или доступную команду или верно запрос по Валюте")
    except CurrencyErrorFail as e:
        bot.send_message(message.chat.id, e)

# ответ бота на нажатия инлайнклавиатуры
@bot.callback_query_handler(func=lambda call:True)
def answer(call):
    if call.data == "EUR USD 100":
        bt = Currency("EUR", "USD", 100)
        bot.send_message(call.message.chat.id, bt)
    elif call.data == "USD EUR 100":
        bt = Currency("USD", "EUR", 100)
        bot.send_message(call.message.chat.id, bt)
    elif call.data == "RUR USD 100":
        bt = Currency("RUR", "USD", 100)
        bot.send_message(call.message.chat.id, bt)
    elif call.data == "UAH RUR 100":
        bt = Currency("UAH", "RUR", 100)
        bot.send_message(call.message.chat.id, bt)



bot.polling(none_stop=True)