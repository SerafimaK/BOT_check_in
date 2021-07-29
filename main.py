import telebot
import re
import config
import states
import user

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Доброе утро! С радостью отвечу на любые ваши вопросы. Но для начала напишите "
                                      "ваш номер телефона. Если хотите использовать номер из Telegram - нажмите на "
                                      "кнопку.")


@bot.message_handler(func=lambda message: states.get_current_state(message.chat.id) == 'Start')
def first_question(message):
    phone = re.compile('((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}')
    if re.search(phone, message.text):
        user_phone = re.search(phone, message.text)
        user_phone = re.sub("\D", "", user_phone.group())
        user.add_info(phone, user_phone)
        # проверка на наличие аккаунта, привязанного к номеру телефона
        # если есть (подтягиваем данные):
        reply = "На этот номер уже зарегистрирован аккаунт. Иванов Иван Иванович, это вы? /допустим, 123456/"
        states.set_state(message.chat.id, 'HasAccount')
        # если нет:
        # reply = "У вас еще нет аккаунта. Но мы быстро это исправим! Пожалуйста, напишите ваши ФИО"
        # states.set_state(message.chat.id, 'NewAccount')
    else:
        reply = "Я не понимаю. Пожалуйста, напишите ваш номер телефона."
    bot.send_message(message.from_user.id, reply)


@bot.message_handler(func=lambda message: states.get_current_state(message.chat.id) == 'HasAccount')
def has_account(message):
    reply = "На указанный номер придет код.  Пришлите его в чат, чтобы мы убедились, что это действительно вы."
    states.set_state(message.chat.id, 'Verify')
    bot.send_message(message.from_user.id, reply)


@bot.message_handler(func=lambda message: states.get_current_state(message.chat.id) == 'Verify')
def has_account(message):
    if message.text == '123456':
        reply = "Бинго :)"
        states.set_state(message.chat.id, 'AccountOwner')
    else:
        reply = "Проверьте корректность кода и попробуйте еще раз."
    bot.send_message(message.from_user.id, reply)


@bot.message_handler(func=lambda message: states.get_current_state(message.chat.id) == 'NewAccount')
def has_account(message):
    reply = "У вас еще нет аккаунта. Но мы быстро это исправим! Пожалуйста, напишите ваши ФИО"
    states.set_state(message.chat.id, 'Name')
    bot.send_message(message.from_user.id, reply)


@bot.message_handler(func=lambda message: states.get_current_state(message.chat.id) == 'Name')
def has_account(message):
    reply = "У вас еще нет аккаунта. Но мы быстро это исправим! Пожалуйста, напишите ваши ФИО"
    states.set_state(message.chat.id, 'Age')
    bot.send_message(message.from_user.id, reply)


@bot.message_handler(func=lambda message: states.get_current_state(message.chat.id) == 'Age')
def has_account(message):
    reply = "Укажите дату вашего рождения в формате ДД.ММ.ГГГГ"
    states.set_state(message.chat.id, 'Email')
    bot.send_message(message.from_user.id, reply)

bot.polling()
