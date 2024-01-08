import os
from dotenv import load_dotenv
import telebot
import webbrowser
from random import randrange
from telebot import types
import requests, json
import googlemaps
load_dotenv()
# enter your api key here
api_key = os.environ.get("GOOGLE_api_key")
bot = telebot.TeleBot(os.environ.get("TGTOKEN"))

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['whoisgay'])
def who_is_gay(message):
    rand = randrange(0, 5)
    if rand == 0:
        bot.send_message(message.chat.id, "Артём Пидр!", parse_mode='html')
    elif rand == 1:
        bot.send_message(message.chat.id, "Саша Пидр!", parse_mode='html')
    elif rand == 2:
        bot.send_message(message.chat.id, "Сергей Пидр!", parse_mode='html')
    elif rand == 3:
        bot.send_message(message.chat.id, "Никита Пидр!", parse_mode='html')
    elif rand == 4:
        bot.send_message(message.chat.id, "Давид Пидр!", parse_mode='html')
        
        

        
        
@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Перейти на сайт', url='https://google.com'))
    
    bot.send_message(message.chat.id, 'Перейдите на сайтик', reply_markup=markup)
    
    
@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    website = types.KeyboardButton('Сайт') 
    start = types.KeyboardButton('Начать')
    markup.add(website, start)
    bot.send_message(message.chat.id, 'Кнопочки, тык', reply_markup=markup)
    
    
@bot.message_handler(commands=['travel'])
def user_depart(message):
    msgDest = bot.send_message(message.chat.id, 'Куда поедем?') 
     #bot.register_next_step_handler(msgDest, travel)
    bot.register_next_step_handler(message, lambda msg: user_dest(msgDest, msg))
    
def user_dest(msgDest, message):
         
    userDest = message.text
    msgStart = bot.send_message(message.chat.id, 'Где находимся?')
    bot.register_next_step_handler(message, lambda msg: fuel_price(userDest, msgDest, msg)) #Передаём
    
    
def fuel_price(userDest, msgDest, message):
    userStart = message.text
    price_fuel = bot.send_message(message.chat.id, 'Цена топлива?')
    bot.register_next_step_handler(message, lambda msg: avg_consumption(price_fuel, userDest, userStart, msg)) #Передаём
     
def avg_consumption(price_fuel, userDest, userStart, message):
    price = message.text
    consumpt = bot.send_message(message.chat.id, 'Средний расход машины на 100км?')
    bot.register_next_step_handler(message, lambda msg: travel(consumpt, price, userDest, userStart, msg)) #Передаём
    
    
    
def travel(consumpt, price, userDest, userStart, message):
    while True:
        avg_consumption = message.text
        # Requires API key
        gmaps = googlemaps.Client(key='AIzaSyAn8hB5p8_EKxqRQ728gRIqwlfLYQ-GZmI')
        #Requires cities name
        my_dist = gmaps.distance_matrix(userStart, userDest)['rows'][0]['elements'][0]
        # Printing the result
        print (my_dist)

        if not my_dist['status'] == 'OK':
            bot.send_message(message.chat.id, 'Ошибка, маршрут не найден. Попробуйте ещё раз.')
        break
    while True:
        if not my_dist['status'] == 'OK':
            break
        print(my_dist)
        my_dist2 = my_dist['distance']['text']
        my_dist3 = my_dist['duration']['text']
        print(my_dist2)
        print(my_dist3)
        print(userStart)
        print(userDest)
        print (price)
        print(avg_consumption)
        
        if 'km' in my_dist2:
            Range = my_dist2.replace(' km', '')
        else:
            Range = my_dist2.replace(' m', '')
        
        print (Range)
        Range = Range.replace(',', '')
        range = int(Range)
        
        

        cost =  range/100 * float(avg_consumption) * float(price)
        cost = round(cost, 2)
        print(cost, "EUR")

        bot.send_message(message.chat.id, my_dist2)
        bot.send_message(message.chat.id, my_dist3)
        message_fuel_cost = f"Стоимость топлива составит: {cost} EUR"
        bot.send_message(message.chat.id, message_fuel_cost)
        
        break
    
    
#Добавить ввод цены на топлива и расчёт стоимости.
#Расход машины?
#TODO: Добавить обработку ошибки ввода. Чтобы вводились только слова и буквы, там, где это необходимо.
    

    
    

        
        
        

#@bot.message_handler(content_types=['text'])
#def get_user_text(message):
 #   if message.text == "Кто ты?":
  #      bot.send_message(message.chat.id, "Я - Олег!", parse_mode='html')
        
        
@bot.message_handler(commands=['text'])
def rock_paper_scissors(message):
    if message.text == "кмн":
        bot.send_message(message.chat.id, "Я - Олег!", parse_mode='html')
        
@bot.message_handler(commands=['rps'])
def INPUTrock_paper_scissors(message):
    Player_Score = 0
    Program_Score = 0
    bot.send_message(message.chat.id, 'Welcome to the game "Rock, Paper, Scissors"', parse_mode='html')
    bot.send_message(message.chat.id,'Please, make your choice: \n' '(1) - rock \n' '(2) - paper \n' '(3) - scissors', parse_mode='html')
    bot.send_message(message.chat.id, 'Your choice is:')
    bot.register_next_step_handler(message, lambda msg:OUTPUTrock_paper_scissors(msg, Player_Score, Program_Score))
            
def OUTPUTrock_paper_scissors(message, Player_Score, Program_Score):
    PlayerInput = message.text
    print(PlayerInput)
    if  not (PlayerInput == '1' or PlayerInput == '2' or PlayerInput == '3'):
        bot.send_message(message.chat.id, 'Ломай меня полностью...', parse_mode='html')
        return
    else:
        PlayerInput = int(PlayerInput)
        ProgramInput = randrange(1, 4)
        bot.reply_to(message, f'Program Input: {ProgramInput}')
    
    
    print ('PlayerInput', PlayerInput)
    print ('ProgramInput', ProgramInput)
    if PlayerInput == 1 and ProgramInput == 1 or PlayerInput == 2 and ProgramInput == 2 or PlayerInput == 3 and ProgramInput == 3:
        bot.send_message(message.chat.id, '----------Draw----------', parse_mode='html')
        bot.reply_to(message, f'Current score is: {Player_Score} : {Program_Score}')
            
    elif PlayerInput == 1 and ProgramInput == 2 or PlayerInput == 2 and ProgramInput == 3 or PlayerInput == 3 and ProgramInput == 1:
        bot.send_message(message.chat.id, '----------You lose----------', parse_mode='html')
        Program_Score = Program_Score + 1
        bot.reply_to(message, f'Current score is: {Player_Score} : {Program_Score}')
            
    elif PlayerInput == 1 and ProgramInput == 3 or PlayerInput == 2 and ProgramInput == 1 or PlayerInput == 3 and ProgramInput == 2:
        bot.send_message(message.chat.id, '----------You win----------', parse_mode='html')
        Player_Score = Player_Score + 1
        bot.reply_to(message, f'Current score is: {Player_Score} : {Program_Score}')
    else:
        bot.send_message(message.chat.id, 'Быдлокод не работает', parse_mode='html')
       # retry = int(input('Want to play again? (1 - yes, 2 - no):'))
        #if retry == 2:
            #break       

    
    
    
    
#@bot.message_handler(content_types=['text'])
#def redirect(message):
    #if message.text == "Сайт":
        #webbrowser.open('https://google.com')
        
        
        
@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == "@yeap4ik":
        bot.send_message(message.chat.id, "PIDORASI", parse_mode='html')





bot.polling(none_stop=True)

#Pogoda


