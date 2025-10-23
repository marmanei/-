import telebot
import random
# Замени 'TOKEN' на токен твоего бота
# Этот токен ты получаешь от BotFather, чтобы бот мог работать
bot = telebot.TeleBot("8345813412:AAH9t-LBs47RvIuQFq3HWjHYa-Sux4pF574")

def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>123456789"
    password = ""
    for i in range(pass_length):
        password += random.choice(elements)
    return password
@bot.message_handler(commands=['pass'])
def send_password(message):
    password = gen_pass(20)  # Устанавливаем длину пароля, например, 10 символов
    bot.reply_to(message, f"Вот твой сгенерированный пароль: {password}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")

@bot.message_handler(commands=['привет'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['пока'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['ы'])
def send_y(message):
    bot.reply_to(message, "с головой все норм??")

@bot.message_handler(commands=['banana'])
def send_banana(message):
    bot.reply_to(message, "100 рублей за кило!")

@bot.message_handler(commands=['help'])
def send_h(message):
    bot.reply_to(message, "Команды:  /привет  /пока  /ы  /banana")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

def gen_img(image1):
    elements = "☣☢⚠🚸🔴🟠🟡🟢🔵🟣🟤⚫🟫🟪🟦🟩🟨🟧🟥⬛⬜◼◻◾◽▪▫🔳🔲"
    image = ""
    for i in range(image1):
        image += random.choice(elements)
    return image1
@bot.message_handler(commands=['img'])
def send_image(message):
    image1 = gen_pass(20)  
    bot.reply_to(message, f"Вот твой сгенерированный смайлик: {image1}")

bot.polling()
