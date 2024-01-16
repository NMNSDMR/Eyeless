import telebot
from telebot import types

TOKEN = 'qwerty'
bot = telebot.TeleBot(TOKEN)

user_state = {}
MIN_HEIGHT = 120
MAX_HEIGHT = 230
MIN_WEIGHT = 20
MAX_WEIGHT = 250
MIN_AGE = 7
MAX_AGE = 120
food_calories = {
    'гранатовый морс (320 ml)': 208,
    'кекс лимонный (50g)': 203,
    'пирог домашний с маком (70g)': 290,
    'яблоко (240g)': 120,
    'апельсин (250g)': 115,
}

def suggest_food(chat_id, missing_calories):
    sorted_food = []

    food_calories = {
        'гранатовый морс (320 ml)': 208,
        'кекс лимонный (50g)': 203,
        'пирог домашний с маком (70g)': 290,
        'яблоко (240g)': 120,
        'апельсин (250g)': 115,
    }

    sorted_food = sorted(food_calories.items(), key=lambda x: x[1], reverse=True)

    suggested_food = []
    total_calories = 0  

    for food, calories in sorted_food:
        servings = missing_calories // calories
        recommended_calories = servings * calories

        if recommended_calories > 0:
            suggested_food.append(f'{food} - {servings} шт. ({recommended_calories} ккал)')
            total_calories += recommended_calories
            missing_calories -= recommended_calories

            if missing_calories <= 0:
                break

    if total_calories > 0:
        remaining_calories = user_state[chat_id]['remaining_calories']
        if remaining_calories > 0:
            recommendation_message = f'Вам не хватает {int(remaining_calories)} ккал. Рекомендуем съесть {", ".join(suggested_food)}'
        else:
            recommendation_message = f'Вы поели больше на {int(-remaining_calories)} ккал. Рекомендуем уменьшить энергетическую ценность следующих приемов пищи'
        bot.send_message(chat_id, recommendation_message)
    
# Добавим новое сообщение и кнопки "Меню столовой" и "Ответы на вопросы"
@bot.message_handler(commands=['faq'])
def handle_faq(message):
    chat_id = message.chat.id
    if chat_id in user_state:
        del user_state[chat_id]

    faq_text = "Что такое калорийность? Это количество энергии, которое получает организм при переваривании еды\n" \
               "Есть ли разница между килокалориями (ккал) и калориями (кал)? 1 килокалория (ккал) равна 1000 калорий (кал). Часто люди часто используют слово «калории» вместо «килокалории», потому что так проще выговорить\n" \
               "Как мы считаем норму калорий? По формуле Миффлина — Сан-Жеора для поддержания веса\n\n"

    # Создаем инлайн-клавиатуру с кнопкой "назад" и "Меню столовой"
    keyboard = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("Назад", callback_data="back_to_start")
    menu_button = types.InlineKeyboardButton("Меню столовой", callback_data="menu")
    keyboard.add(back_button, menu_button)

    # Изменяем текст и инлайн-клавиатуру в исходном сообщении "Добро пожаловать!"
    bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=faq_text, parse_mode="Markdown", reply_markup=keyboard)

# Обрабатываем кнопку "назад"
@bot.callback_query_handler(func=lambda call: call.data == "back_to_start")
def back_to_start(call):
    chat_id = call.message.chat.id

    # Создаем инлайн-клавиатуру с кнопками "Меню столовой" и "Ответы на вопросы"
    keyboard = types.InlineKeyboardMarkup()
    menu_button = types.InlineKeyboardButton("Меню столовой", callback_data="menu")
    faq_button = types.InlineKeyboardButton("Ответы на вопросы", callback_data="faq")
    keyboard.add(menu_button, faq_button)

    # Изменяем текст и инлайн-клавиатуру в исходном сообщении "Добро пожаловать!"
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Добро пожаловать!\nНаш бот посчитает для Вас норму калорий и проанализирует школьное меню", reply_markup=keyboard)

@bot.message_handler(commands=['menu'])
def handle_menu(message):
    chat_id = message.chat.id
    if chat_id in user_state:
        del user_state[chat_id]
    with open('./images//menu.jpg', 'rb') as menu_image:
        bot.send_photo(chat_id, menu_image, caption="Для нового расчета воспользуйтесь командой /start")

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
    if message.text == '/start':
        handle_start(message)
    elif message.text == '/faq':
        handle_faq(message)
    elif message.text == '/menu':
        handle_menu(message)
    else:
        height_str = message.text.replace(',', '.')
        try:
            height = float(height_str)
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
        weight_str = message.text.replace(',', '.')
        try:
            weight = float(weight_str)
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

            with open('/Users/wiktork./Desktop/Food-Research/bot/images/activity.jpg', 'rb') as activity_image:
                activity_photo = activity_image.read()

            keyboard = types.ReplyKeyboardMarkup()
            activity_levels = ["1", "2", "3", "4", "5"]
            keyboard.add(*activity_levels)

            bot.send_photo(chat_id, activity_photo, caption="Выберите ваш уровень активности ↑", reply_markup=keyboard)
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
            user_state[chat_id]['calorie_goal'] = calorie_goal
            user_state[chat_id]['calories_per_day'] = calorie_goal
            calorie_goal_per_day = calories * activity_factors[activity_level]
            calorie_goal_per_day = int(calorie_goal_per_day)
            user_state[chat_id]['calorie_goal_per_day'] = calorie_goal_per_day

            proteins = int(calorie_goal * 0.3 / 4)
            fats = int(calorie_goal * 0.3 / 9)
            carbohydrates = int(calorie_goal * 0.4 / 4)
            proteins1 = int(calorie_goal_per_day * 0.3 / 4)
            fats2 = int(calorie_goal_per_day * 0.3 / 9)
            carbohydrates3 = int(calorie_goal_per_day * 0.4 / 4)
            

            user_state[chat_id]['proteins'] = proteins
            user_state[chat_id]['fats'] = fats
            user_state[chat_id]['carbohydrates'] = carbohydrates
            user_state[chat_id]['proteins1'] = proteins1
            user_state[chat_id]['fats2'] = fats2
            user_state[chat_id]['carbohydrates3'] = carbohydrates3

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
            keyboard.add(*days)
            bot.send_message(chat_id, f"За завтрак и обед вам нужно - {calorie_goal} ккал, {proteins} белков, {fats} жиров, {carbohydrates} углеводов\nЗа весь день вам нужно - {calorie_goal_per_day} ккал, {proteins1} белков, {fats2} жиров, {carbohydrates3} углеводов\nВыберите день недели для расчета калорийности:", reply_markup=keyboard)
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
        calories_per_day = {
            "Понедельник": 1524,
            "Вторник": 1323,
            "Среда": 1109,
            "Четверг": 1371,
            "Пятница": 1583
        }

        if day in calories_per_day:
            daily_calories = calories_per_day[day]
            calorie_difference = daily_calories - calorie_goal

            user_state[chat_id]['remaining_calories'] = calorie_difference

            if daily_calories >= calorie_goal:
                bot.send_message(chat_id, f"Вы поели больше на {int(calorie_difference)} ккал от своей нормы. Рекомендуем уменьшить энергетическую ценность следующих приемов пищи")
            else:
                if 'suggestion_sent' not in user_data:
                    missing_calories = -calorie_difference
                    suggest_food(chat_id, missing_calories)
                    user_data['suggestion_sent'] = True

            hide_day_buttons(chat_id)
        else:
            bot.send_message(chat_id, "Выберите день недели с помощью клавиатуры.")
            bot.register_next_step_handler(message, calculate_daily_calories)

def suggest_food(chat_id, missing_calories):
    sorted_food = []

    food_calories = {
        'гранатовый морс (320 ml)': 208,
        'кекс лимонный (50g)': 203,
        'пирог домашний с маком (70g)': 290,
        'яблоко (240g)': 120,
        'апельсин (250g)': 115,
    }

    sorted_food = sorted(food_calories.items(), key=lambda x: x[1], reverse=True)

    suggested_food = []
    total_calories = 0  

    for food, calories in sorted_food:
        servings = missing_calories // calories
        recommended_calories = servings * calories

        if recommended_calories > 0:
            suggested_food.append(f'{food} - {servings} шт. ({recommended_calories} ккал)')
            total_calories += recommended_calories
            missing_calories -= recommended_calories

            if missing_calories <= 0:
                break

    if total_calories > 0:
        remaining_calories = user_state[chat_id]['remaining_calories']
        if remaining_calories < 0:
            recommendation_message = f'Вам не хватает {int(-remaining_calories)} ккал. Рекомендуем съесть {", ".join(suggested_food)}'
        else:
            recommendation_message = f'Вы поели больше на {int(-remaining_calories)} ккал. Рекомендуем уменьшить энергетическую ценность следующих приемов пищи'
        bot.send_message(chat_id, recommendation_message)

def hide_day_buttons(chat_id):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, "Для нового расчета воспользуйтесь командой /start", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    if call.data == "menu":
        handle_menu(call.message)
    elif call.data == "faq":
        handle_faq(call.message)
if __name__ == "__main__":
    bot.polling(none_stop=True)
    
