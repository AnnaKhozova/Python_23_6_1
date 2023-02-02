import telebot
from config import TOKEN, keys
from extensions import ExchangeException, Exchange

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Здравствуйте! Чтобы начать работу, введите команду боту в следующем формате: \n<имя валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты> \nПосмотреть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию, введите команду боту в следующем формате: \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\nЧтобы увидеть список всех доступных валют, введите команду\n/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ExchangeException('Введена некорректная команда или неверное количество параметров')

        try:
            amount = float(values[2])
        except ValueError:
            raise ExchangeException(f'Не удалось обработать количество {values[2]}')

        quote = values[0]
        base = values[1]
        total_base = Exchange.get_price(quote, base, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()