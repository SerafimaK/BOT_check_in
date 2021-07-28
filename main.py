import telebot
import re
import config
import states

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Доброе утро! С радостью отвечу на любые ваши вопросы. Но для начала напишите "
                                      "ваш номер телефона или email. ")


@bot.message_handler(func=lambda message: states.get_current_state(message.chat.id) == 'Start')
def first_question(message):
    phone = re.compile('((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}')
    email = re.compile('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}')
    if re.search(phone, message.text):
        client_phone = re.search(phone, message.text)
        client_phone = re.sub("\D", "", client_phone.group())
        reply = "Ваш номер телефона: " + client_phone + ", верно?"
        states.set_state(message.chat.id, 'SentPhone')
    elif re.search(email, message.text):
        client_email = re.search(email, message.text)
        reply = "Ваш email: " + client_email + ", верно?"
        states.set_state(message.chat.id, 'SentEmail')
    else:
        reply = "Я не понимаю. Пожалуйста, напишите ваш номер телефона."
    bot.send_message(message.from_user.id, reply)


# тут можно добавить проверку на наличие аккаунта
# предположим, он есть и мы взяли из него ФИО
@bot.message_handler(func=lambda message: states.get_current_state(message.chat.id) == 'SentPhone')
def has_account(message):
    reply = "Вижу, что у вас уже есть аккаунт! Иванов Иван Иванович, это вы?"
    bot.send_message(message.from_user.id, reply)


bot.polling()
