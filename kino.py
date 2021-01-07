import telebot
from telebot import types
from kinopoisk.movie import Movie
from sys import setrecursionlimit

token = "1572832353:AAFo85rNi-I1jPXcYmzLxx5ohVRM9iG4ySY"
bot = telebot.TeleBot(token)

setrecursionlimit(3000)

@bot.message_handler(commands = ["start"])

def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	item1 = types.KeyboardButton("Найди фильм")

	markup.add(item1)

	bot.send_message(message.chat.id, "<b>Добро пожаловать!</b>\n<b>Я бот, который выдаёт обзор о фильме и где его посмотреть!</b>\nРаспологайся поудобнее.", 
		parse_mode = "html",
		reply_markup = markup)

@bot.message_handler(content_types = ["text"])
def markup(message):
	if message.chat.type == "private":
		if message.text == "Найди фильм":
			bot.send_message(message.chat.id, "Введи фильм: ")

			bot.register_next_step_handler(message, films)	

def films(message):
	movie_list = Movie.objects.search(message.text)
	title = movie_list[0].title
	id_film = movie_list[0].id

	movie = Movie(id = id_film)

	for item in movie_list[:8]:
		title = item.title
		year = item.year
		description = item.plot
		rating = item.rating
		google = "https://google.com/?#q=" + "" +title

		if year is None and description == "" and rating is None:
			bot.send_message(message.chat.id, "Название: " + title + "\nГод выхода: не найдено\nМини-описание: " + "не найдено" + "\nОценка: " + "не найдено\n" + "Посмотреть и почитать более подробную информацию можно здесь: " + "https://www.kinopoisk.ru/film/" + str(id_film) + "\nИ здесь: " + google,
				parse_mode = "html") 

		else:
			bot.send_message(message.chat.id, "Название: " + title + "\nГод выхода: " + str(year) + "\nМини-описание: " + description + "\nОценка: " + str(rating),
				parse_mode = "html")

if __name__ == '__main__':

	bot.infinity_polling()