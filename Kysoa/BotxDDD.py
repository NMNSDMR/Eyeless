import telebot
from telebot import types
import random
TOKEN = '6640244474:AAGlpJHtSBb7ilATPMp4lqQBgrzML0oxGkU'
bot = telebot.TeleBot(TOKEN)

user_state = {}
MIN_HEIGHT = 120
MAX_HEIGHT = 230
MIN_WEIGHT = 20
MAX_WEIGHT = 250
MIN_AGE = 7
MAX_AGE = 120
food_calories = {
    'Гранатовый морс (320 ml)': 208,
    'Кекс лимонный (50g)': 203,
    'Пирог домашний с маком (70g)': 290,
    'Яблоко (240g)': 120,
    'Апельсин (250g)': 115,
}

@bot.message_handler(commands=['faq'])
def handle_faq(message):
    chat_id = message.chat.id
    if chat_id in user_state:
        del user_state[chat_id]

    faq_text = "*Что такое калорийность?* _Это количество энергии, которое получает наш организм при переваривании еды_\n"\
               "*Есть ли разница между килокалориями (ккал) и калориями (кал)?* _Калорийность обычно измеряется в килокалориях: 1 килокалория (ккал) равна 1000 калорий (кал). Но есть один нюанс, который порой может сбить с толку: люди часто используют слово «калории» вместо «килокалории». Почему? Да просто так проще выговорить_\n"\
               "*Как мы считаем норму калорий?* _Мы используем формулу Миффлин-Сан Жеора для поддержания веса_"
    bot.send_message(chat_id, faq_text, parse_mode="Markdown")
    bot.send_message(chat_id, "Для нового расчета воспользуйтесь командой /start")

@bot.message_handler(commands=['menu'])
def handle_menu(message):
    chat_id = message.chat.id
    if chat_id in user_state:
        del user_state[chat_id]
    with open('/images/menu.jpg', 'rb') as menu_image:
        bot.send_photo(chat_id, menu_image)
    
    bot.send_message(chat_id, "Для нового расчета используйте команду /start")

@bot.message_handler(commands=['start'])
def handle_start(message):
    user = message.from_user
    chat_id = message.chat.id
    if chat_id in user_state:
        del user_state[chat_id]

    keyboard = types.InlineKeyboardMarkup()
    menu_button = types.InlineKeyboardButton("Меню столовой", callback_data="menu")
    faq_button = types.InlineKeyboardButton("Ответы на вопросы", callback_data="faq")
    keyboard.row(menu_button, faq_button)

    bot.send_message(chat_id, "Добро пожаловать!\nНаш бот посчитает для Вас норму калорий и проанализирует школьное меню", reply_markup=keyboard)
    bot.send_message(chat_id, "Введите ваш рост (в см):")
    bot.register_next_step_handler(message, ask_height)

def ask_height(message):
    chat_id = message.chat.id
    if message.text.lower() == '/start':
        handle_start(message)
    elif message.text.lower() == '/faq':
        handle_faq(message)
    elif message.text.lower() == '/menu':
        handle_menu(message)
    else:
        try:
            height = float(message.text)
            if MIN_HEIGHT <= height <= MAX_HEIGHT:
                user_state[chat_id] = {'height': height}
                bot.send_message(chat_id, "Введите ваш вес (в кг):")
                bot.register_next_step_handler(message, ask_weight)
            else:
                bot.send_message(chat_id, f"Рост должен быть в диапазоне от {MIN_HEIGHT} см до {MAX_HEIGHT} см. Попробуйте еще раз.")
                bot.register_next_step_handler(message, ask_height)
        except ValueError:
            bot.send_message(chat_id, "Я воспринимаю только числа. Пожалуйста, введите число.")
            bot.register_next_step_handler(message, ask_height)

def ask_weight(message):
    chat_id = message.chat.id
    if message.text == '/start':
        handle_start(message)
    elif message.text == '/faq':
        handle_faq(message)
    elif message.text == '/menu':
        handle_menu(message)
    else:
        try:
            weight = float(message.text)
            if MIN_WEIGHT <= weight <= MAX_WEIGHT:
                user_state[chat_id]['weight'] = weight
                bot.send_message(chat_id, "Введите ваш возраст:")
                bot.register_next_step_handler(message, ask_age)
            else:
                bot.send_message(chat_id, f"Вес должен быть в диапазоне от {MIN_WEIGHT} кг до {MAX_WEIGHT} кг. Попробуйте еще раз.")
                bot.register_next_step_handler(message, ask_weight)
        except ValueError:
            bot.send_message(chat_id, "Я воспринимаю только числа. Пожалуйста, введите число.")
            bot.register_next_step_handler(message, ask_weight)

def ask_age(message):
    chat_id = message.chat.id
    if message.text == '/start':
        handle_start(message)
    elif message.text == '/faq':
        handle_faq(message)
    elif message.text == '/menu':
        handle_menu(message)
    else:
        try:
            age = int(message.text)
            if MIN_AGE <= age <= MAX_AGE:
                user_state[chat_id]['age'] = age
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                male_button = types.KeyboardButton("Мужской")
                female_button = types.KeyboardButton("Женский")
                keyboard.add(male_button, female_button)
                bot.send_message(chat_id, "Выберите ваш пол:", reply_markup=keyboard)
                bot.register_next_step_handler(message, ask_activity_level)
            else:
                bot.send_message(chat_id, f"Возраст должен быть в диапазоне от {MIN_AGE} до {MAX_AGE} лет. Пожалуйста, введите число.")
                bot.register_next_step_handler(message, ask_age)
        except ValueError:
            bot.send_message(chat_id, "Я воспринимаю только числа. Пожалуйста, введите число.")
            bot.register_next_step_handler(message, ask_age)

def ask_activity_level(message):
    if message.text == '/start':
        handle_start(message)
    elif message.text == '/faq':
        handle_faq(message)
    elif message.text == '/menu':
        handle_menu(message)
    else:
        chat_id = message.chat.id
        gender = message.text.lower()
        if gender in ["мужской", "женский"]:
            user_state[chat_id]['gender'] = gender

            activity_message = "\n\n" \
                            "1 - сидячая работа, отсутствие спорта\n" \
                            "2 - легкие физические упражнения около 3 раз за неделю, ежедневная утренняя зарядка, пешие прогулки\n" \
                            "3 - тренировки до 3 раз за неделю\n" \
                            "4 - тренировки до 5 раз за неделю\n" \
                            "5 - активный образ жизни с ежедневными интенсивными тренировками\n" \

            bot.send_message(chat_id, activity_message)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            activity_levels = ["1", "2", "3", "4", "5"]
            keyboard.add(*activity_levels)
            bot.send_message(chat_id, "Выберите ваш уровень активности ↑", reply_markup=keyboard)
            bot.register_next_step_handler(message, calculate_calories)
        else:
            bot.send_message(chat_id, "Выберите ваш пол с помощью клавиатуры.")
            bot.register_next_step_handler(message, ask_activity_level)

def calculate_calories(message):
    if message.text == '/start':
        handle_start(message)
    elif message.text == '/faq':
        handle_faq(message)
    elif message.text == '/menu':
        handle_menu(message)
    else:
        chat_id = message.chat.id
        activity_level = message.text
        if activity_level in ["1", "2", "3", "4", "5"]:
            user_state[chat_id]['activity_level'] = activity_level

            gender = user_state[chat_id]['gender']
            weight = user_state[chat_id]['weight']
            height = user_state[chat_id]['height']
            age = user_state[chat_id]['age']

            if gender == "мужской":
                calories = (9.99 * weight) + (6.25 * height) - (4.92 * age) + 5
            else:
                calories = (9.99 * weight) + (6.25 * height) - (4.92 * age) - 161

            activity_factors = {
                "1": 1.2,
                "2": 1.375,
                "3": 1.46,
                "4": 1.55,
                "5": 1.7,
            }
            calorie_goal = calories * activity_factors[activity_level] * 2 / 3
            calorie_goal = int(calorie_goal)

            # Расчет нормы белков, жиров и углеводов
            protein_goal = calorie_goal * 0.3 / 4
            fat_goal = calorie_goal * 0.3 / 9
            carbohydrate_goal = calorie_goal * 0.4 / 4

            user_state[chat_id]['calorie_goal'] = calorie_goal
            user_state[chat_id]['protein_goal'] = protein_goal
            user_state[chat_id]['fat_goal'] = fat_goal
            user_state[chat_id]['carbohydrate_goal'] = carbohydrate_goal

            calorie_goalperday = calories * activity_factors[activity_level]
            calorie_goalperday = int(calorie_goalperday)
            user_state[chat_id]['calorie_goalperday'] = calorie_goalperday
            user_state[chat_id]['calories_perday'] = calorie_goalperday

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
            keyboard.add(*days)
            bot.send_message(chat_id, f"За завтрак и обед вам нужно - {calorie_goal} ккал\n"
                                      f"За весь день вам нужно - {calorie_goalperday} ккал\n"
                                      f"Белки: {int(protein_goal)} г\n"
                                      f"Жиры: {int(fat_goal)} г\n"
                                      f"Углеводы: {int(carbohydrate_goal)} г\n"
                                      "Выберите день недели для расчета калорийности:", reply_markup=keyboard)
            bot.register_next_step_handler(message, calculate_daily_calories)
        else:
            bot.send_message(chat_id, "Выберите уровень активности с помощью клавиатуры.")
            bot.register_next_step_handler(message, calculate_calories)

def calculate_daily_calories(message):
    if message.text == '/start':
        handle_start(message)
    elif message.text == '/faq':
        handle_faq(message)
    elif message.text == '/menu':
        handle_menu(message)
    else:
        chat_id = message.chat.id
        day = message.text
        user_data = user_state[chat_id]
        calorie_goal = user_data['calorie_goal']
        protein_goal = user_data['protein_goal']
        fat_goal = user_data['fat_goal']
        carbohydrate_goal = user_data['carbohydrate_goal']
        calories_per_day = {
            "Понедельник": 1427,
            "Вторник": 1225,
            "Среда": 1520,
            "Четверг": 1569,
            "Пятница": 1288
        }

        if day in calories_per_day:
            daily_calories = calories_per_day[day]
            calorie_difference = daily_calories - calorie_goal

            if daily_calories >= calorie_goal:
                bot.send_message(chat_id, f"Вы поели больше на {int(calorie_difference)} ккал от своей нормы. Рекомендуем уменьшить энергетическую ценность следующих приемов пищи\n"
                                          f"Белки: {int(protein_goal)} г\n"
                                          f"Жиры: {int(fat_goal)} г\n"
                                          f"Углеводы: {int(carbohydrate_goal)} г")
            else:
                missing_calories = -calorie_difference
                recommended_foods = recommend_foods(missing_calories)
                bot.send_message(chat_id, f"Вам не хватает {int(missing_calories)} ккал для нормы. Рекомендуем следующие продукты:")

                # Создаем список продуктов, сортируя их по убыванию калорий
                sorted_foods = sorted(recommended_foods.items(), key=lambda x: x[1], reverse=True)

                for food, calories in sorted_foods:
                    if missing_calories <= 0:
                        break
                    bot.send_message(chat_id, f"{food}: {calories} ккал")
                    missing_calories -= calories

            bot.send_message(chat_id, "Для нового рассчета воспользуйтесь командой /start")
        else:
            bot.send_message(chat_id, "Выберите день недели с помощью клавиатуры.")
            bot.register_next_step_handler(message, calculate_daily_calories)



def recommend_foods(excess_calories):
    recommended_foods = {}
    extra_calories = excess_calories

    # Создаем список продуктов, сортируя их по возрастанию калорий
    sorted_foods = sorted(food_calories.items(), key=lambda x: x[1])

    for food, calories in sorted_foods:
        if extra_calories <= 0:
            break

        recommended_foods[food] = calories
        extra_calories -= calories

    return recommended_foods




# Добавляем обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    if call.data == "menu":
        handle_menu(call.message)
    elif call.data == "faq":
        handle_faq(call.message)

if __name__ == "__main__":
    bot.polling(none_stop=True)
