import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, ConvertionException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help', ])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду в формате: \n\n<имя валюты> \
<в какую валюту перевести> \
<количество>\n\nПример: рубль доллар 10 \n\n Увидеть список всех доступных валют: /values '
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: \n'
    for key in keys.keys():
        text = '\n > '.join((text, key.capitalize(), ))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def basic(message: telebot.types.Message):

    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное чило параметров!')

        quote = values[0].lower()
        base = values[1].lower()
        amount = values[2]

        total_base = CryptoConverter.get_price(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except ValueError as e:
        bot.reply_to(message, f'Неверное количество валюты.')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} x {quote.capitalize()} = {round(total_base, 2)} {base.capitalize()}'
        bot.send_message(message.chat.id, text)


bot.polling()
