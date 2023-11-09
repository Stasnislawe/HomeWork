import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

TOKEN = '6620692495:AAEcnz8GJO6M0luoHltd9Ob23SF0F31MORY'

bot = telebot.TeleBot(TOKEN)

keys = {
    'евро':'EURC',
    'доллар':'USDC'
}

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Вы можете посмотреть список валют - /values\nЧтобы начать работу введите команду боту в следующем формате:\n<имя валюты><в какую валюту перевести><количество переводимой валюты>\nПример:"рубль доллар 50"'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неправильное значение параметров.')

        base, quote, amount = values
        priceonlyodnogo = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользвателя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не могу обработать команду\n{e}')
    else:
        total_base = float(priceonlyodnogo) * float(amount)
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
