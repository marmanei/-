import telebot
import random
import os
import requests
from quiz1 import quiz2
bot = telebot.TeleBot()
user_scores = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton('🎮 Викторина')
    btn2 = telebot.types.KeyboardButton('🦆 Случайная утка')
    btn3 = telebot.types.KeyboardButton('😂 Случайный мем')
    btn4 = telebot.types.KeyboardButton('📊 Мой счет')
    btn5 = telebot.types.KeyboardButton('❓ Помощь')
    markup.add(btn1, btn2, btn3, btn4, btn5)

    welcome_text = """
🤖 Добро пожаловать в Эко-Бота!

Вот что я умею:

🎮 *Викторина* - проверить свои знания по экологии
🦆 *Случайная утка* - получить фото утки (потому что почему бы и нет!)
😂 *Случайный мем* - получить экологический мем
📊 *Мой счет* - узнать текущий результат в викторине
❓ *Помощь* - показать это сообщение снова

*Также можно использовать команды:*
/start - начать работу
/quiz - начать викторину  
/duck - случайная утка
/mem - случайный мем
/help - помощь

Выбери действие ниже 👇
    """
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    
    if message.text == '🎮 Викторина':
        start_quiz(message)
    elif message.text == '🦆 Случайная утка':
        duck(message)
    elif message.text == '😂 Случайный мем':
        send_mem(message)
    elif message.text == '📊 Мой счет':
        show_score(message)
    elif message.text == '❓ Помощь':
        send_welcome(message)
    else:
            handle_quiz_answer(message)


@bot.message_handler(commands=['mem'])
def send_mem(message):
    try:
        img_name = random.choice(os.listdir('images'))
        with open(f'images/{img_name}', 'rb') as f:
            bot.send_photo(message.chat.id, f)
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Ошибка загрузки мема. Проверь папку images/")

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.message_handler(commands=['duck'])
def duck(message):
    try:
        image_url = get_duck_image_url()
        bot.send_photo(message.chat.id, image_url)
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Не удалось загрузить утку")

@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    user_id = message.from_user.id
    user_scores[user_id] = {"current_question": 0, "score": 0}
    send_question(message, user_id)

def send_question(message, user_id):
    current_q = user_scores[user_id]["current_question"]
    
    if current_q >= len(quiz2):
        score = user_scores[user_id]["score"]
        total = len(quiz2)
        bot.send_message(
            message.chat.id, 
            f"🎉 Викторина завершена!\nТвой результат: {score} из {total}!\nНажми '🎮 Викторина' чтобы начать заново.",
            reply_markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add('🎮 Викторина', '❓ Помощь')
        )
        return
    
    question_data = quiz2[current_q]
    question_text = question_data["question"]
    options = question_data["options"]
    
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for i, option in enumerate(options):
        markup.add(f"{i+1}. {option}")
    
    bot.send_message(
        message.chat.id,
        f"❓ Вопрос {current_q + 1}/{len(quiz2)}:\n{question_text}",
        reply_markup=markup
    )

def handle_quiz_answer(message):
    user_id = message.from_user.id
    
    if user_id not in user_scores:
        return
    
    current_q = user_scores[user_id]["current_question"]
    
    if current_q >= len(quiz2):
        return
    
    question_data = quiz2[current_q]
    user_answer = message.text
    
    is_correct = False
    try:
        if user_answer.split('.')[0].strip().isdigit():
            answer_index = int(user_answer.split('.')[0].strip()) - 1
            if answer_index == question_data["correct"]:
                is_correct = True
        elif user_answer.replace(f"{question_data['correct'] + 1}. ", "") == question_data["options"][question_data["correct"]]:
            is_correct = True
    except:
        pass
    
    if is_correct:
        user_scores[user_id]["score"] += 1
        response_text = "✅ Правильно!"
    else:
        correct_answer = question_data["options"][question_data["correct"]]
        response_text = f"❌ Неправильно. Правильный ответ: {correct_answer}"
    
    response_text += f"\n💡 {question_data['explanation']}"
    
    bot.send_message(message.chat.id, response_text, reply_markup=telebot.types.ReplyKeyboardRemove())
    
    user_scores[user_id]["current_question"] += 1
    
    import time
    time.sleep(2)
    send_question(message, user_id)

def show_score(message):
    user_id = message.from_user.id
    if user_id in user_scores:
        score = user_scores[user_id]["score"]
        current_q = user_scores[user_id]["current_question"]
        total = len(quiz2)
        
        if current_q >= total:
            bot.send_message(message.chat.id, f"🏆 Твой финальный счет: {score} из {total}")
        else:
            bot.send_message(message.chat.id, f"📊 Твой текущий счет: {score} из {current_q} (всего вопросов: {total})")
    else:
        bot.send_message(message.chat.id, "📊 Ты еще не участвовал в викторине! Нажми '🎮 Викторина' чтобы начать.")

bot.polling()
