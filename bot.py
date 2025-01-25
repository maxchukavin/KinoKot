from telebot import types
import telebot
import math
import pandas as pd
from datetime import datetime

bot = telebot.TeleBot('token')

# Инициализация кэша страниц
page_cache = {}

# Читаем таблицу с фильмами из CSV
Kinopoisk_movies_df = pd.read_csv('MovieBot/kinopoisk_top30-2.csv', sep=";")
Kinopoisk_catastrophe_df = pd.read_csv('MovieBot/catastrophe_movies.csv', sep=";")
Kinopoisk_action_films_df = pd.read_csv('MovieBot/thrillers.csv', sep=";")
Kinopoisk_drama_films_df = pd.read_csv('MovieBot/dramas.csv', sep=";")
IVI_movies_df = pd.read_csv('MovieBot/ivi_top30.csv', sep=";")
IVI_catastrophe_df = pd.read_csv('MovieBot/ivi_catastrophies.csv', sep=";")
ivi_adventure_films_df = pd.read_csv('MovieBot/ivi_adventures.csv', sep=";")
IVI_drama_films_df = pd.read_csv('MovieBot/ivi_dramas.csv', sep=";")
OKKO_movies_df = pd.read_csv('MovieBot/okko_top30.csv', sep=";")
OKKO_drama_df = pd.read_csv('MovieBot/okko_dramas.csv', sep=";")
OKKO_adventure_films_df = pd.read_csv('MovieBot/okko_adventure.csv', sep=";")
OKKO_action_films_df = pd.read_csv('MovieBot/okko_action.csv', sep=";")
other_good_movies_df = pd.read_csv('MovieBot/with_love.csv', sep=";")
other_art_house_df = pd.read_csv('MovieBot/art_house.csv', sep=";")
other_best_animation_df = pd.read_csv('MovieBot/best_animation.csv', sep=";")

# Время последней компиляции программы
last_compilation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_version = types.KeyboardButton("Актуальная версия") # Инициализация кнопок главной страницы
    btn_info = types.KeyboardButton("Информация")
    btn_services = types.KeyboardButton("Сервисы")
    keyboard.add(btn_version, btn_info, btn_services)

    bot.send_message(
        message.chat.id,
        "Возвращение в главное меню",
        reply_markup=keyboard
    )

# Обработчик кнопки "Информация"
@bot.message_handler(func=lambda message: message.text == "Информация")
def information(message):
    bot.send_message(
        message.chat.id,
        "Привет! Это бот с подборкой фильмов, в котором можно найти интересующий фильм и получить ссылку на него.\nВыбери команду, чтобы начать:",
    )

# Обработчик кнопки "Актуальная версия"
@bot.message_handler(func=lambda message: message.text == "Актуальная версия")
def version_command(message):
    bot.send_message(
        message.chat.id,
        f"Версия программы актуальна.\nПоследняя компиляция: {last_compilation_time}"
    )

# Обработчик кнопки "Сервисы"
@bot.message_handler(func=lambda message: message.text == "Сервисы")
def services_command(message):
    services_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_kinopoisk = types.KeyboardButton("Кинопоиск")
    btn_IVI = types.KeyboardButton("IVI")
    btn_okko = types.KeyboardButton("OKKO")
    btn_other = types.KeyboardButton("Подборка от авторов")
    btn_main_menu = types.KeyboardButton("В главное меню")
    services_keyboard.add(btn_kinopoisk, btn_IVI, btn_okko, btn_other, btn_main_menu)

    bot.send_message(
        message.chat.id,
        "Выбери сервис для просмотра фильмов:",
        reply_markup=services_keyboard
    )

# Обработчик кнопки "Кинопоиск"
@bot.message_handler(func=lambda message: message.text == "Кинопоиск")
def kinopoisk_handler(message):
    kinopoisk_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_top_movies = types.KeyboardButton("Топ фильмов Кинопоиска")
    btn_catastrophe = types.KeyboardButton("Фильмы-катастрофы")
    btn_action_films = types.KeyboardButton("Боевики")
    btn_drama_films = types.KeyboardButton("Драмы")
    btn_main_menu = types.KeyboardButton("В главное меню")
    kinopoisk_keyboard.add(btn_top_movies, btn_catastrophe, btn_action_films, btn_drama_films, btn_main_menu)

    bot.send_message(
        message.chat.id,
        "Выбери категорию фильмов в Кинопоиске:",
        reply_markup=kinopoisk_keyboard
    )

# Обработчик кнопки "Топ фильмов Кинопоиска"
@bot.message_handler(func=lambda message: message.text == "Топ фильмов Кинопоиска")
def top_movies_handler(message):
    set_current_page(message.chat.id, 1, Kinopoisk_movies_df, "Топ фильмов Кинопоиска")
    send_movie_buttons(message, Kinopoisk_movies_df, page=1, title="Топ фильмов Кинопоиска")

# Обработчик кнопки "Фильмы-катастрофы"
@bot.message_handler(func=lambda message: message.text == "Фильмы-катастрофы")
def catastrophe_handler(message):
    set_current_page(message.chat.id, 1, Kinopoisk_catastrophe_df, "Фильмы-катастрофы")
    send_movie_buttons(message, Kinopoisk_catastrophe_df, page=1, title="Фильмы-катастрофы")

# Обработчик кнопки "Боевики"
@bot.message_handler(func=lambda message: message.text == "Боевики")
def action_films_handler(message):
    set_current_page(message.chat.id, 1, Kinopoisk_action_films_df, "Боевики")
    send_movie_buttons(message, Kinopoisk_action_films_df, page=1, title="Боевики")

# Обработчик кнопки "Драмы"
@bot.message_handler(func=lambda message: message.text == "Драмы")
def drama_films_handler(message):
    set_current_page(message.chat.id, 1, Kinopoisk_drama_films_df, "Драмы")
    send_movie_buttons(message, Kinopoisk_drama_films_df, page=1, title="Драмы")

# Обработчик кнопки "IVI"
@bot.message_handler(func=lambda message: message.text == "IVI")
def IVI_handler(message):
    IVI_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_top_movies = types.KeyboardButton("Топ фильмов IVI")
    btn_catastrophe = types.KeyboardButton("Фильмы-катастрофы IVI")
    btn_action_films = types.KeyboardButton("Приключения IVI")
    btn_drama_films = types.KeyboardButton("Драмы IVI")
    btn_main_menu = types.KeyboardButton("В главное меню")
    IVI_keyboard.add(btn_top_movies, btn_catastrophe, btn_action_films, btn_drama_films, btn_main_menu)

    bot.send_message(
        message.chat.id,
        "Выбери категорию фильмов в IVI:",
        reply_markup=IVI_keyboard
    )

# Обработчик кнопки "Топ фильмов IVI"
@bot.message_handler(func=lambda message: message.text == "Топ фильмов IVI")
def ivi_movies_handler(message):
    set_current_page(message.chat.id, 1, IVI_movies_df, "Топ фильмов IVI")
    send_movie_buttons(message, IVI_movies_df, page=1, title="Топ фильмов IVI")

# Обработчик кнопки "Фильмы катастрофы IVI"
@bot.message_handler(func=lambda message: message.text == "Фильмы-катастрофы IVI")
def IVI_catastrofe(message):
    set_current_page(message.chat.id, 1, IVI_catastrophe_df, "Фильмы-катастрофы IVI")
    send_movie_buttons(message, IVI_catastrophe_df, page=1, title="Фильмы-катастрофы IVI")

# Обработчик кнопки "Приключения"
@bot.message_handler(func=lambda message: message.text == "Приключения IVI")
def IVI_adventure_films(message):
    set_current_page(message.chat.id, 1, ivi_adventure_films_df, "Приключения IVI")
    send_movie_buttons(message, ivi_adventure_films_df, page=1, title="Приключения IVI")

# Обработчик кнопки "Драмы"
@bot.message_handler(func=lambda message: message.text == "Драмы IVI")
def IVI_drama_films(message):
    set_current_page(message.chat.id, 1, IVI_drama_films_df, "Драмы IVI")
    send_movie_buttons(message, IVI_drama_films_df, page=1, title="Драмы IVI")

# Обработчик кнопки "В главное меню"
@bot.message_handler(func=lambda message: message.text == "В главное меню")
def back_to_main_menu(message):
    start_command(message)

# Обработчик кнопки "OKKO"
@bot.message_handler(func=lambda message: message.text == "OKKO")
def okko_handler(message):
    okko_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_top_movies = types.KeyboardButton("Топ фильмов ОККО")
    btn_action_films = types.KeyboardButton("Боевики OKKO")
    btn_adventure_films = types.KeyboardButton("Приключения OKKO")
    btn_drama_films = types.KeyboardButton("Драмы OKKO")
    btn_main_menu = types.KeyboardButton("В главное меню")
    okko_keyboard.add(btn_top_movies, btn_adventure_films, btn_action_films, btn_drama_films, btn_main_menu)

    bot.send_message(
        message.chat.id,
        "Выбери категорию фильмов в ОККО:",
        reply_markup=okko_keyboard
    )

# Обработчик кнопки "Топ фильмов OKKO"
@bot.message_handler(func=lambda message: message.text == "Топ фильмов ОККО")
def okko_movies_handler(message):
    set_current_page(message.chat.id, 1, OKKO_movies_df, "Топ фильмов ОККО")
    send_movie_buttons(message, OKKO_movies_df, page=1, title="Топ фильмов ОККО")

# Обработчик кнопки "Фильмы катастрофы OKKO"
@bot.message_handler(func=lambda message: message.text == "Боевики OKKO")
def okko_catastrofe(message):
    set_current_page(message.chat.id, 1, OKKO_action_films_df, "Боевики OKKO")
    send_movie_buttons(message, OKKO_action_films_df, page=1, title="Боевики OKKO")

# Обработчик кнопки "Приключения OKKO"
@bot.message_handler(func=lambda message: message.text == "Приключения OKKO")
def okko_adventure_films(message):
    set_current_page(message.chat.id, 1, OKKO_adventure_films_df, "Приключения OKKO")
    send_movie_buttons(message, OKKO_adventure_films_df, page=1, title="Приключения OKKO")

# Обработчик кнопки "Драмы OKKO"
@bot.message_handler(func=lambda message: message.text == "Драмы OKKO")
def okko_drama_films(message):
    set_current_page(message.chat.id, 1, OKKO_drama_df, "Драмы OKKO")
    send_movie_buttons(message, OKKO_drama_df, page=1, title="Драмы OKKO")

# Обработчик кнопки "В главное меню"
@bot.message_handler(func=lambda message: message.text == "В главное меню")
def back_to_main_menu(message):
    start_command(message)

# Обработчик кнопки "Подборка от авторов"
@bot.message_handler(func=lambda message: message.text == "Подборка от авторов")
def other_handler(message):
    other_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_artHouse_films = types.KeyboardButton("Нескучный арт-хаус")
    btn_best_animated_films = types.KeyboardButton("Лучшая анимация")
    btn_loved_films = types.KeyboardButton("Любимое кино")
    btn_main_menu = types.KeyboardButton("В главное меню")
    other_keyboard.add(btn_artHouse_films, btn_best_animated_films, btn_loved_films, btn_main_menu)

    bot.send_message(
        message.chat.id,
        "Выбери подборку:",
        reply_markup=other_keyboard
    )

# Обработчик кнопки "Нескучный арт-хаус"
@bot.message_handler(func=lambda message: message.text == "Нескучный арт-хаус")
def other_movies_handler(message):
    set_current_page(message.chat.id, 1, other_art_house_df, "Нескучный арт-хаус")
    send_movie_buttons(message, other_art_house_df, page=1, title="Нескучный арт-хаус")

# Обработчик кнопки "Лучшая анимация"
@bot.message_handler(func=lambda message: message.text == "Лучшая анимация")
def other_catastrofe(message):
    set_current_page(message.chat.id, 1, other_best_animation_df, "Лучшая анимация")
    send_movie_buttons(message, other_best_animation_df, page=1, title="Лучшая анимация")

# Обработчик кнопки "Любимое кино"
@bot.message_handler(func=lambda message: message.text == "Любимое кино")
def other_adventure_films(message):
    set_current_page(message.chat.id, 1, other_good_movies_df, "Любимое кино")
    send_movie_buttons(message, other_good_movies_df, page=1, title="Любимое кино")

# Обработчик кнопки "В главное меню"
@bot.message_handler(func=lambda message: message.text == "В главное меню")
def back_to_main_menu(message):
    start_command(message)

# Функция для отправки списка фильмов с кнопками
def send_movie_buttons(message, dataframe, page, title):
    start_index = (page - 1) * 10 # Переменные являются индексами для страниц фильмов
    end_index = start_index + 10
    movies_to_show = dataframe.iloc[start_index:end_index]

    movie_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for _, movie in movies_to_show.iterrows():
        btn_movie = types.KeyboardButton(f"{movie['Title']}")  # Реализация кнопок с фильмами
        movie_keyboard.add(btn_movie)

    btn_back = types.KeyboardButton("Назад")
    btn_forward = types.KeyboardButton("Вперед")
    btn_main_menu = types.KeyboardButton("В главное меню")
    movie_keyboard.add(btn_back, btn_forward, btn_main_menu)

    bot.send_message(
        message.chat.id,
        f"{title} ({page}/{math.ceil(len(dataframe) / 10)})",
        reply_markup=movie_keyboard
    )



# Обработчик кнопки "Назад"
@bot.message_handler(func=lambda message: message.text == "Назад")
def go_back_handler(message):
    if message.chat.id in page_cache:
        current_page = page_cache[message.chat.id]['current_page']
        dataframe = page_cache[message.chat.id]['dataframe']
        title = page_cache[message.chat.id]['title']

        if current_page > 1:
            set_current_page(message.chat.id, current_page - 1, dataframe, title)
            send_movie_buttons(message, dataframe, current_page - 1, title)
        else:
            bot.send_message(message.chat.id, "Это первая страница.")

# Обработчик кнопки "Вперед"
@bot.message_handler(func=lambda message: message.text == "Вперед")
def go_forward_handler(message):
    if message.chat.id in page_cache:
        current_page = page_cache[message.chat.id]['current_page']
        dataframe = page_cache[message.chat.id]['dataframe']
        title = page_cache[message.chat.id]['title']

        if current_page * 10 < len(dataframe):
            set_current_page(message.chat.id, current_page + 1, dataframe, title)
            send_movie_buttons(message, dataframe, current_page + 1, title)
        else:
            bot.send_message(message.chat.id, "Это последняя страница.")


# Функция для обновления страницы
def set_current_page(chat_id, page, dataframe, title):
    page_cache[chat_id] = {
        'current_page': page,
        'dataframe': dataframe,
        'title': title
    }
    # Сохраняем выбранный фильм в кэше
    page_cache[chat_id]['selected_movie'] = dataframe.iloc[0]  

# Функция для загрузки фильмов из CSV в словарь
def load_movies(file_path):
    movies = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            title, link = line.strip().split(";")
            movies[title] = link
    return movies

# Загружаем фильмы из всех файлов
Kinopoisk_movies = load_movies('MovieBot/kinopoisk_top30-2.csv')
Kinopoisk_catastrophe = load_movies('MovieBot/catastrophe_movies.csv')
Kinopoisk_action_films = load_movies('MovieBot/thrillers.csv')
Kinopoisk_drama_films = load_movies('MovieBot/dramas.csv')
IVI_movies = load_movies('MovieBot/ivi_top30.csv')
IVI_catastrophe = load_movies('MovieBot/ivi_catastrophies.csv')
IVI_adventure_films = load_movies('MovieBot/ivi_adventures.csv')
IVI_drama_films = load_movies('MovieBot/ivi_dramas.csv')
OKKO_movies = load_movies('MovieBot/okko_top30.csv')
OKKO_drama = load_movies('MovieBot/okko_dramas.csv')
OKKO_adventure_films = load_movies('MovieBot/okko_adventure.csv')
OKKO_action_films = load_movies('MovieBot/okko_action.csv')
other_good_movies = load_movies('MovieBot/with_love.csv')
other_art_house = load_movies('MovieBot/art_house.csv')
other_best_animation = load_movies('MovieBot/best_animation.csv')

# Список всех словарей фильмов для поиска
all_movie_dicts = [
    Kinopoisk_movies,
    Kinopoisk_catastrophe,
    Kinopoisk_action_films,
    Kinopoisk_drama_films,
    IVI_movies,
    IVI_catastrophe,
    IVI_adventure_films,
    IVI_drama_films,
    OKKO_drama,
    OKKO_action_films,
    OKKO_adventure_films,
    OKKO_movies,
    other_art_house,
    other_best_animation,
    other_good_movies
]

# Обработчик выбора фильма
@bot.message_handler(func=lambda message: True)
def end_movie_button(message):
    # Поиск фильма в загруженных словарях
    selected_movie = None
    for movie_dict in all_movie_dicts:
        if message.text in movie_dict:
            selected_movie = movie_dict[message.text]
            break

    if selected_movie:
        bot.send_message(
            message.chat.id,
            f"Вы выбрали фильм: {message.text}\nХотите перейти по ссылке?\n{selected_movie}"
        )
    else:
        bot.send_message(message.chat.id, "Фильм не найден. Пожалуйста, выберите фильм из списка.")


bot.polling(none_stop=True)