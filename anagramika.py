import telebot
from flask import Flask, request
import os
import random
import random_words as rw
from emojis import Emojis
from nltk.chat.util import Chat, reflections
from anagramika_data import *

class QuizUserDataPrivate():
    def __init__(self, score=0, b_game_begin=0):
        self.score = score
        self.b_game_begin = b_game_begin
        self.answer = ""
        self.difficulty_level = 1

class QuizUserDataGroup():
    def __init__(self, score=0, name="Player1"):
        self.name = name
        self.score = score

class QuizGroupData():
	def __init__(self, b_game_active=0):
		self.active_user_data = dict()
		self.b_game_active = b_game_active
		self.answer = ""
		self.difficulty_level = 1

class AMutex():
	def __init__(self):
		self.is_locked=0

	def release(self):
		self.is_locked=0

	def lock(self):
		while(self.is_locked!=0):
			pass
		self.is_locked=1

API_TOKEN = str(os.environ.get("API_TOKEN"))
MY_ID = int(os.environ.get("MY_ID"))

bot = telebot.TeleBot(token=API_TOKEN)

chat = Chat(pairs, reflections)

server = Flask(__name__)

g_user_data_private = dict()
g_group_data = dict()

g_group_data_mutex = AMutex()
g_user_data_private_mutex = AMutex()

my_words_list = rw.easy_words + rw.med_words + rw.hard_words

def take_second_entry(x):
	return x[1]

def debug_print(group_data):
	for chat in group_data:
		print("CHAT ID= {}".format(chat))
		chat_data = group_data[chat]
		for user in chat_data.active_user_data:
			print("USER ID= {}".format(user))
			print("NAME = {}".format(chat_data.active_user_data[user].name))

def get_random_word(diff_level=1):
	words = my_words_list
	random_index = random.randint(0, len(words)-1)
	return words[random_index].upper()

def bot_send_anagram(chat_id, r_word):
	word = list(r_word)
	random.shuffle(word)
	ag = ' '.join(word)
	bot.send_message(chat_id, ag)

@bot.message_handler(commands=['start'])
def start_anagram(m):
	bot.send_message(m.chat.id, welcome_msg)

@bot.message_handler(commands=['anstart'])
def start_anagram(m):
	if("group"==m.chat.type):
		u_id = str(m.chat.id)
		if(u_id in g_group_data):
			if(g_group_data[u_id].b_game_active==1):
				bot.send_message(m.chat.id, "Can't you see I am already running here! Don't make Anagramika an 'Angry'gamika XD ..")
			else:
				g_group_data_mutex.lock()
				g_group_data[u_id].b_game_active = 1
				my_word = get_random_word()
				g_group_data[u_id].answer = my_word
				g_group_data_mutex.release()
				bot.send_message(m.chat.id, anagram_welcome_msg)
				bot.send_message(m.chat.id, rules_group_msg)
				bot_send_anagram(m.chat.id, my_word)
		else:
			g_group_data_mutex.lock()
			g_group_data[u_id] = QuizGroupData()
			g_group_data[u_id].b_game_active = 1
			my_word = get_random_word()
			g_group_data[u_id].answer = my_word
			g_group_data_mutex.release()
			bot.send_message(m.chat.id, anagram_welcome_msg)
			bot.send_message(m.chat.id, rules_group_msg)
			bot_send_anagram(m.chat.id, my_word)
	elif("private"==m.chat.type):
		u_id = str(m.chat.id)
		if(u_id in g_user_data_private):
			bot.send_message(m.chat.id, "Can't you see I am already running here! Don't make Anagramika an 'Angry'gamika XD ..")
		else:
			g_user_data_private_mutex.lock()
			g_user_data_private[u_id] = QuizUserDataPrivate()
			g_user_data_private[u_id].b_game_begin = 1
			g_user_data_private[u_id].score = 0
			my_word = get_random_word()
			g_user_data_private[u_id].answer = my_word
			g_user_data_private_mutex.release()
			bot.send_message(m.chat.id, anagram_welcome_msg)
			bot.send_message(m.chat.id, rules_priv_msg)
			bot_send_anagram(m.chat.id, my_word)
	else:
		pass


@bot.message_handler(commands=['anstop'])
def end_quiz(m):
	if("group"==m.chat.type):
		u_id = str(m.chat.id)
		if(u_id in g_group_data):
			g_group_data_mutex.lock()
			if(1==g_group_data[u_id].b_game_active):
				bot.reply_to(m, "Everyone, "+good_bye_msg)
				#Display Scores
				if(not g_group_data[u_id].active_user_data):
					bot.send_message(m.chat.id, "Nobody has played yet.")
				else:
					score_list = list()
					for key in g_group_data[u_id].active_user_data:
						score_list.append([g_group_data[u_id].active_user_data[key].name, g_group_data[u_id].active_user_data[key].score])
						score_list.sort(reverse=True, key=take_second_entry)
					res_str = ""
					for score in score_list:
						res_str += "{} - {}\n".format(score[0], score[1])
				g_group_data[u_id].b_game_active = 0
				g_group_data[u_id].active_user_data = dict()
				g_group_data_mutex.release()
				if(res_str!=""):
					bot.send_message(m.chat.id, "Scoreboard : \n\n"+res_str)
				else:
					bot.send_message(m.chat.id, "Ah! Disappointing. Nobody played. Start me again with /start")
			else:
				bot.send_message(m.chat.id, "Already killed me once. Don't kill me more :P !!")
	elif("private"==m.chat.type):
		u_id = str(m.chat.id)
		if(u_id in g_user_data_private):
			user_name = m.from_user.first_name
			bot.reply_to(m, "{}, ".format(user_name)+good_bye_msg)
			#Display Scores
			res_str = "You scored {}\n".format(g_user_data_private[u_id].score)
			bot.send_message(m.chat.id, res_str)
			del g_user_data_private[u_id]
	else:
		pass

@bot.message_handler(commands=['pass'])
def pass_anagram(m):
	if("group"==m.chat.type):
		u_id = str(m.chat.id)
		user_id = str(m.from_user.id)
		admin_ids = list()
		for admin in bot.get_chat_administrators(m.chat.id):
			admin_ids.append(str(admin.user.id))
		if(u_id in g_group_data):
			if(1==g_group_data[u_id].b_game_active):
				if(user_id in admin_ids):
					#pass the question
					bot.send_message(m.chat.id, "Bailed you cowards! Alas. Here is the answer :")
					bot.send_message(m.chat.id, g_group_data[u_id].answer)
					bot.send_message(m.chat.id, "And here is the next question :")
					my_word = get_random_word()
					g_group_data[u_id].answer = my_word
					bot_send_anagram(m.chat.id, my_word)
				else:
					bot.send_message(m.chat.id, "Who are you? Call the Admin {}!!".format(Emojis["angry_face"]))
			else:
				bot.send_message(m.chat.id, "Pass? What pass? First start the game!")
		else:
			bot.send_message(m.chat.id, "Pass? What pass? First start the game!")
	elif("private"==m.chat.type):
		u_id = str(m.chat.id)
		if(u_id in g_user_data_private):
			if(1==g_user_data_private[u_id].b_game_begin):
				#pass the question
				bot.send_message(m.chat.id, "Here is the answer :")
				bot.send_message(m.chat.id, g_user_data_private[u_id].answer)
				bot.send_message(m.chat.id, "And here is the next question :")
				my_word = get_random_word()
				g_user_data_private[u_id].answer = my_word
				bot_send_anagram(m.chat.id, my_word)
			else:
				bot.send_message(m.chat.id,"Please start the game first!")
		else:
			bot.send_message(m.chat.id,"Please start the game first!")
	else:
		pass

@bot.message_handler(commands=['score'])
def display_score(m):
	if("group"==m.chat.type):
		u_id = str(m.chat.id)
		user_id = str(m.from_user.id)
		if(u_id in g_group_data):
			g_group_data_mutex.lock()
			if(1==g_group_data[u_id].b_game_active):
				if(user_id in g_group_data[u_id].active_user_data):
					score = g_group_data[u_id].active_user_data[user_id].score
					name = g_group_data[u_id].active_user_data[user_id].name
					bot.reply_to(m, "{}, your score is {}.".format(name, score))
				else:
					bot.reply_to(m, "Please attempt atleast one question before seeking your score.")
			else:
				bot.reply_to(m, "There is no game active!")
			g_group_data_mutex.release()
		else:
			bot.reply_to(m, "There is no game active!")
	elif("private"==m.chat.type):
		u_id = str(m.chat.id)
		if(u_id in g_user_data_private):
			if(1==g_user_data_private[u_id].b_game_begin):
				score = g_user_data_private[u_id].score
				bot.reply_to(m, "Your score is {}.".format(score))
			else:
				bot.send_message(m.chat.id,"Please start the game first!")
		else:
			bot.send_message(m.chat.id,"Please start the game first!")
	else:
		pass


@bot.message_handler(commands=['board'])
def display_score_all(m):
	if("group"==m.chat.type):
		u_id = str(m.chat.id)
		if(u_id in g_group_data):
			g_group_data_mutex.lock()
			if(1==g_group_data[u_id].b_game_active):
				if(not g_group_data[u_id].active_user_data):
					bot.send_message(m.chat.id, "Nobody has played yet.")
				else:
					score_list = list()
					for key in g_group_data[u_id].active_user_data:
						score_list.append([g_group_data[u_id].active_user_data[key].name, g_group_data[u_id].active_user_data[key].score])
						score_list.sort(reverse=True, key=take_second_entry)
					res_str = ""
					for score in score_list:
						res_str += "{} - {}\n".format(score[0], score[1])
					bot.send_message(m.chat.id, "Scoreboard : \n\n"+res_str)
			else:
				bot.reply_to(m, "There is no game active!")
			g_group_data_mutex.release()
		else:
			bot.reply_to(m, "There is no game active!")
	elif("private"==m.chat.type):
		bot.send_message("This command is only applicable in groups.")
	else:
		pass

#Anagramika is kicked from the group
@bot.message_handler(func=lambda msg: msg.left_chat_member is not None and msg.left_chat_member.id==MY_ID)
def got_kicked(m):
	u_id = str(m.chat.id)
	del g_group_data[u_id]


@bot.message_handler(func=lambda msg: msg.text is not None)
def answer_handler(m):
	if("group"==m.chat.type):
		u_id = str(m.chat.id)
		user_id = str(m.from_user.id)
		#If u_id is not there in db, it means bot is kicked. Then this msg shouldn't come.
		#So if msg comes from a particular u_id, it means bot is in the group. We need to
		#pay attention to the game_active flag
		if(u_id in g_group_data and 1==g_group_data[u_id].b_game_active):
			ans = m.text.upper()
			var = user_id not in g_group_data[u_id].active_user_data
			if(user_id not in g_group_data[u_id].active_user_data):
				#Answering first time, add to active players
				g_group_data_mutex.lock()
				g_group_data[u_id].active_user_data[user_id] = QuizUserDataGroup()
				g_group_data[u_id].active_user_data[user_id].name = m.from_user.first_name
				g_group_data[u_id].active_user_data[user_id].score = 0
				g_group_data_mutex.release()
			
			if(g_group_data[u_id].answer==ans):
				#This is to avoid delay between two correct answers
				g_group_data[u_id].answer="#"
				g_group_data[u_id].active_user_data[user_id].score += 10
				bot.reply_to(m, "Correct {}! {}, you have earned 10 points!".format(Emojis["face_throwing_a_kiss"], m.from_user.first_name))
				my_word = get_random_word()
				g_group_data[u_id].answer = my_word
				bot_send_anagram(m.chat.id, my_word)
			else:
				#Don't give this response when playing in group, will end up like spam
				pass
		else:
			#Game is not active, this is generic chat message, let it pass
			pass
	elif("private"==m.chat.type):
		u_id = str(m.chat.id)
		if(u_id in g_user_data_private):
			ans = m.text.upper()
			if(ans==g_user_data_private[u_id].answer):
				g_user_data_private[u_id].score += 10
				bot.reply_to(m, "Correct! {}, you have earned 10 points!".format(m.from_user.first_name))
				my_word = get_random_word()
				g_user_data_private[u_id].answer = my_word
				bot_send_anagram(m.chat.id, my_word)
			else:
				bot.reply_to(m, "Not quite right..")
		else:
			# User not in DB. Means the game hasn't been started after an endgram. Say something!
			req = m.text.lower()
			resp = chat.respond(req)
			if(resp is not None):
				bot.send_message(m.chat.id, resp)
			else:
				bot.send_message(m.chat.id, "Sorry, I didn't quite get that.")
	else:
		pass

@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://anagramika.herokuapp.com/' + API_TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    random.seed()