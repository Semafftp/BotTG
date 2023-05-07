
import telebot
from config import keys, bot
from extensions import ConvertionException, СurrencyConverter


@bot.message_handler(commands=['start', 'help'])  # func=lambda n: True)
def help(message: telebot.types.Message):
    text = "Я не прошу я требую ввести команду в формате : \n<имя валюты>  \
<в какую валюту перевести> \
<количество переводимой валюты>\n список валют = values "
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты"
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Количество параметров не совпадает. Используйте формат:\n<имя валюты> ' \
                                      '<в какую валюту перевести> <количество переводимой валюты> \n')

        quote, base, amount = values
        total_base = СurrencyConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'ВОТ ЭТА ШО:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
         text = f'Цена {amount} {quote} B {base} - {total_base}'
         bot.send_message(message.chat.id, text)


bot.polling()
