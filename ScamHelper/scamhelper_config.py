import telebot
from telebot import types
from telebot.types import InputMediaPhoto

import threading, scamhelper_keyboard, scamhelper_database, random, textwrap, requests

from PIL import Image, ImageFont, ImageDraw

from time import sleep

import datetime

bot = telebot.TeleBot('2201142867:AAHZAOWEbatee2rdFwSUPH2ogDZIotL9cuQ/test') # Сюда токен вашего бота!

db = scamhelper_database
keyboard = scamhelper_keyboard

support = 'kwiken' # Username админа без @
admin = '2200117397' # ID админа 

banned = ['🕵️ Отрисовка', '👨‍💻 Готовые скриншоты', '👨‍💻 Диалоги', '💁🏻‍♀️ Информация', 'Назад ↩️']


# Регистрация

def profile_user(message):
	try:
		
 		username = db.user_username(message.chat.id)

 		if (username == 'None') or (username == '@None'):
 			if (message.from_user.username is not None):
 				db.user_update_username(message.chat.id, f'@{message.chat.username}')
	 		elif (message.from_user.first_name is not None):
	 			db.user_update_username(message.chat.id, message.from_user.first_name)
	 	elif (message.from_user.username is not None):
	 		db.user_update_username(message.chat.id, f'@{message.chat.username}')
	 	elif (message.from_user.first_name is not None):
	 		db.user_update_username(message.chat.id, message.from_user.first_name)

	except Exception as e:
		print(e)				

# Функции

def plural_days(n):
    days = ['день', 'дня', 'дней']
    
    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return str(n) + ' ' + days[p]

def user_date(user_id):
	try:
		date = datetime.datetime.strptime(db.user_date(user_id), '%Y-%m-%d')
		date = str(date - datetime.datetime.now()).split(',')
		date = date[0]
		date = date.replace('-', '')

		if ('days' in date):
			date = date.replace('days', '')
		elif ('day' in date):
			date = date.replace('day', '')

		return plural_days(int(date))
	except Exception as e:
		print(e)

def Comissions(value):
    try:

        return str("{0:.2f}".format(float(value)))

    except:
        return 0

def show_adverting(user_id):
	try:
		
		config = open('adverting.txt', 'r', encoding = 'utf-8')
		adverting = config.read()

		if (adverting != '00'):
			bot.send_message(user_id, adverting, parse_mode='html')
 

	except:
		pass


# Register Next Step Handler

def send_all_ad(message):
    try:
        if (len(message.text) > 1):

            if ';' in message.text:
                text = message.text.split(';')

                rows = db.user_id_db()

                p = requests.get(text[1])
                out = open("temp.jpg", "wb")
                out.write(p.content)
                out.close()

                photo = open('temp.jpg', 'rb')

                i = 0
                for row in rows:

                    try:
                        bot.send_photo(row, photo, caption = text[0], parse_mode = 'html')
                        i += 1
                    except:
                        pass

                bot.send_message(message.chat.id, f'Сообщений отправлено - {i}')

            else:
                rows = db.user_id_db()
                i = 0
                for row in rows:

                    try:
                        bot.send_message(row, message.text, parse_mode='html')
                        i += 1
                    except:
                        pass

                bot.send_message(message.chat.id, f'Сообщений отправлено - {i}')
        else:
            bot.send_message(message.chat.id, 'Отменено')

    except Exception as e:
        print(e)

def add_all_ad(message):
	try:

		if (len(message.text) > 1):

			config = open('adverting.txt', 'w', encoding = 'utf-8')
			config.write(message.text)

			inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
			inline_1 = types.InlineKeyboardButton(text = "Просмотр", callback_data = 'SHOW_AD')
			inline_keyboard.add(inline_1)

			bot.send_message(message.chat.id, 'Рекламное сообщение обновлено', reply_markup=inline_keyboard)
		else:
			bot.send_message(message.chat.id, 'Отменено')

	except:
		pass	

def fake_qiwi_balance(message):
	try:

		if (message.text not in banned):
			text = message.text + ' ₽'
			qiwi = Image.open("Image source/Qiwi/qiwi_balance.png")
			fnt = ImageFont.truetype("Fonts/Roboto-Bold.ttf", 100)
			W = 1080
			w, h = fnt.getsize(text)
			d = ImageDraw.Draw(qiwi)
			d.text(((W - w) / 2, 296), text, font=fnt, fill=(255, 255, 255, 255))
			del d
			qiwi.save("Image cache/file_qiwi.png", "PNG")
			img = open('Image cache/file_qiwi.png', 'rb')

			bot.send_photo(message.chat.id, img)
			show_adverting(message.chat.id)
		else:
			bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())

	except Exception as e:
		print(e)

def fake_qiwi_transfer(message):
	try:

		if (message.text not in banned):
			text = message.text.split('\n')
			money = text[0] + " ₽"
			money2 = "- " + text[0].strip() + " ₽"
			phone = text[1].strip()
			date_time = text[2].strip()
			qiwi = Image.open('Image source/Qiwi/qiwi_check.png')
			font1 = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 53)
			font2 = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 38)
			font3 = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 45)
			font4 = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 45)
			W = 1080
			w1, h1 = font1.getsize(money2)
			w2, h2 = font1.getsize(phone)
			d = ImageDraw.Draw(qiwi)
			d.text(((W-w1)/2,685), money2, font=font1, fill=(0,0,0,255))
			d.text(((W-w2)/2 + 60,614), phone, font=font2, fill=(153,153,153,255))
			d.text((56,1890), date_time, font=font3, fill=(0,0,0,255))
			d.text((56,2072), money, font=font4, fill=(0,0,0,255))
			qiwi.save("Image cache/file_qiwi_1.png", "PNG")
			img = open('Image cache/file_qiwi_1.png', 'rb')
			bot.send_photo(message.chat.id, img)
			show_adverting(message.chat.id)
		else:
			bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())

	except Exception as e:
		print(e)	

def fake_qiwi_get_pc(message):
    try:
        if (message.text not in banned):

        	text = message.text.split('\n')

        	phone = text[0]
        	money = text[1] + ' ₽'
        	name = text[2]
        	payment = Comissions(float(text[3]) - float(text[4])).replace('.', ',')
        	comission = text[4]
        	date = text[5]
        	phone1 = phone.replace(' ', '').replace('‑', '')

        	tink = Image.open('Image source/Qiwi/qiwi_check_pc.png')
        	font1 = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 20)
        	font2 = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 14)
        	font3 = ImageFont.truetype('Fonts/MuseoSans-300.ttf', 21)
        	font4 = ImageFont.truetype('Fonts/MuseoSans-300.ttf', 29)
        	font5 = ImageFont.truetype('Fonts/MuseoSans-300.ttf', 16)
        	font6 = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 15)
        	font7 = ImageFont.truetype('Fonts/MuseoSans-500.ttf', 16)

        	d = ImageDraw.Draw(tink)

        	d.text((1404,20), phone, font=font2, fill=(153,153,153,255))
        	d.text((1404,40), money, font=font1, fill=(0,0,0,255))
        	d.text((497,494), name, font=font3, fill=(0,0,0,255))

        	d.text((677,553), payment, font=font5, fill=(0,0,0,255))
        	d.text((677,583), comission, font=font5, fill=(0,0,0,255))
        	d.text((677,613), payment, font=font7, fill=(0,0,0,255))
        	d.text((677,708), date, font=font5, fill=(0,0,0,255))
        	d.text((677,770), phone1, font=font5, fill=(0,0,0,255))

        	W = 1903
        	w, h = font4.getsize(payment)
        	w1, h1 = font5.getsize(payment)
        	w2, h2 = font5.getsize(comission)
        	w3, h3 = font7.getsize(payment)

        	d.text(((W - w - 810), 489), payment, font=font4, fill='#4bbd5c')
        	d.text(((677 + w1 + 7), 555), '₽', font=font6, fill='#000')
        	d.text(((677 + w2 + 7), 585), '₽', font=font6, fill='#000')
        	d.text(((677 + w3 + 7), 615), '₽', font=font6, fill='#000')

        	tink.save("Image cache/file_qiwi_check_pc.png", "PNG")
        	img = open('Image cache/file_qiwi_check_pc.png', 'rb')
        	bot.send_photo(message.chat.id, img)
        	show_adverting(message.chat.id)
        else:
        	bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_sber_balance(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")
            time = text[0]
            name = text[1] + " ₽"
            money = text[2]
            tink = Image.open('Image source/Sber/sber_balance.png')
            font_time = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 16)
            font_name = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 24)
            font_money = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 18)
            d = ImageDraw.Draw(tink)
            d.text((15,20), time, font=font_time, fill=(225, 238, 229,255))

            if (len(text[1]) == 4):
                d.text((490,543), name, font=font_name, fill=(37,152,97,255))
            elif (len(text[1]) <= 3):
                d.text((500,543), name, font=font_name, fill=(37,152,97,255))
            elif (len(text[1]) == 5):
                d.text((480,543), name, font=font_name, fill=(37,152,97,255))
            elif (len(text[1]) == 6):
                d.text((455,543), name, font=font_name, fill=(37,152,97,255))
            elif (len(text[1]) == 7):
            	d.text((430,543), name, font=font_name, fill=(37,152,97,255))
            elif (len(text[1]) == 8):
            	d.text((400,543), name, font=font_name, fill=(37,152,97,255))
            elif (len(text[1]) == 9):
            	d.text((370,543), name, font=font_name, fill=(37,152,97,255))	

            d.text((115, 580), money, font=font_money, fill=(132,132,132,255))
            tink.save("Image cache/file_sber.png", "PNG")
            img = open('Image cache/file_sber.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
        	bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_sber_transfer(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")
            time = text[0]
            name = text[1] + " ₽"
            money = text[2]
            tink = Image.open('Image source/Sber/sber_transfer.png')
            font_time = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 16)
            font_name = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 43)
            font_money = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 21)
            d = ImageDraw.Draw(tink)
            d.text((15,20), time, font=font_time, fill=(225, 238, 229,255))
            if (len(text[1]) == 4):
                d.text((185,270), name, font=font_name, fill=(255,255,255,255))
            elif (len(text[1]) == 3):
                d.text((195,270), name, font=font_name, fill=(255,255,255,255))
            elif (len(text[1]) == 5):
                d.text((170,270), name, font=font_name, fill=(255,255,255,255))
            d.text((80, 835), money, font=font_money, fill=(73,73,73,255))
            tink.save("Image cache/file_sber_1.png", "PNG")
            img = open('Image cache/file_sber_1.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
        	bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_yandex_balance(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")
            time = text[0]
            name = text[1]
            money = text[2]
            tink = Image.open('Image source/Yandex/ya_balance.png')
            font_money = ImageFont.truetype('Fonts/ArialRegular.ttf', 96)
            font_name = ImageFont.truetype('Fonts/ArialRegular.ttf', 30)
            font_time = ImageFont.truetype('Fonts/Roboto-Medium.ttf', 21)
            d = ImageDraw.Draw(tink)

            d.text((330,9), time, font=font_time, fill=(255,255,255,255))
            d.text((140,90), name, font=font_name, fill=(255,255,255,255))  
            d.text((50,380), money, font=font_money, fill=(255,255,255,255))

            tink.save("Image cache/file_yandex.png", "PNG")
            img = open('Image cache/file_yandex.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_tinkoff_transfer(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")
            time = text[0]
            money = text[1] + " ₽"
            tink = Image.open('Image source/Tinkoff/tinkoff_transfer.png')
            font_money = ImageFont.truetype('Fonts/ArialRegular.ttf', 54)
            font_time = ImageFont.truetype('Fonts/Roboto-Medium.ttf', 21)
            d = ImageDraw.Draw(tink)

            d.text((340,6), time, font=font_time, fill=(255,255,255,255))

            if (len(text[1]) == 3):
                d.text((290,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 4):
                d.text((280,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 5):
                d.text((270,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 6):    
                d.text((260,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 7):    
                d.text((240,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 8):    
                d.text((220,600), money, font=font_money, fill=(255,255,255,255))

            tink.save("Image cache/file_tinkoff_transfer.png", "PNG")
            img = open('Image cache/file_tinkoff_transfer.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_tinkoff_youla_transfer(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")
            time = text[0]
            money = text[1] + " ₽"
            tink = Image.open('Image source/Tinkoff/tk_youla_transfer.png')
            font_money = ImageFont.truetype('Fonts/ArialRegular.ttf', 54)
            font_time = ImageFont.truetype('Fonts/Roboto-Medium.ttf', 21)
            d = ImageDraw.Draw(tink)

            d.text((340,6), time, font=font_time, fill=(255,255,255,255))

            if (len(text[1]) == 3):
                d.text((290,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 4):
                d.text((280,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 5):
                d.text((270,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 6):    
                d.text((260,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 7):    
                d.text((240,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 8):    
                d.text((220,600), money, font=font_money, fill=(255,255,255,255))

            tink.save("Image cache/file_tk_youla_transfer.png", "PNG")
            img = open('Image cache/file_tk_youla_transfer.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_tinkoff_avito_transfer(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")
            time = text[0]
            money = text[1] + " ₽"
            tink = Image.open('Image source/Tinkoff/tk_avito_transfer.png')
            font_money = ImageFont.truetype('Fonts/ArialRegular.ttf', 54)
            font_time = ImageFont.truetype('Fonts/Roboto-Medium.ttf', 21)
            d = ImageDraw.Draw(tink)

            d.text((340,6), time, font=font_time, fill=(255,255,255,255))

            if (len(text[1]) == 3):
                d.text((290,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 4):
                d.text((280,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 5):
                d.text((270,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 6):    
                d.text((260,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 7):    
                d.text((240,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 8):    
                d.text((220,600), money, font=font_money, fill=(255,255,255,255))

            tink.save("Image cache/file_tk_avito_transfer.png", "PNG")
            img = open('Image cache/file_tk_avito_transfer.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e) 

def fake_tinkoff_refund(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")
            time = text[0]
            money = text[1] + " ₽"
            tink = Image.open('Image source/Tinkoff/tinkoff_refund.png')
            font_money = ImageFont.truetype('Fonts/ArialRegular.ttf', 54)
            font_time = ImageFont.truetype('Fonts/Roboto-Medium.ttf', 21)
            d = ImageDraw.Draw(tink)

            d.text((340,6), time, font=font_time, fill=(255,255,255,255))

            if (len(text[1]) == 3):
                d.text((290,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 4):
                d.text((280,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 5):
                d.text((270,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 6):    
                d.text((260,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 7):    
                d.text((240,600), money, font=font_money, fill=(255,255,255,255))
            elif (len(text[1]) == 8):    
                d.text((220,600), money, font=font_money, fill=(255,255,255,255))

            tink.save("Image cache/file_tk_refund.png", "PNG")
            img = open('Image cache/file_tk_refund.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e) 

def fake_tinkoff_transaction(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")

            date = datetime.date.today()
            date = date.strftime("%d.%m.%Y")

            time = text[0]
            name = text[1]
            money = text[2] + " RUB"
            description = text[3]

            tink = Image.open('Image source/Tinkoff/tk_transaction.png')

            font_main = ImageFont.truetype('Fonts/ArialRegular.ttf', 15)
            font_name = ImageFont.truetype('Fonts/Roboto-Medium.ttf', 13)
            
            d = ImageDraw.Draw(tink)

            d.text((100,178.5), date, font=font_main, fill=(0,0,0,255))
            d.text((85,497), time, font=font_main, fill=(0,0,0,255))

            d.text((615,394), name, font=font_name, fill=(0,0,0,255))

            if (len(text[3]) == 19) or (len(text[3]) == 20):
                d.text((600,497), description, font=font_main, fill=(0,0,0,255))
            elif (len(text[3]) == 17) or (len(text[3]) == 18):
                d.text((625,497), description, font=font_main, fill=(0,0,0,255))
            elif (len(text[3]) == 15) or (len(text[3]) == 16):
                d.text((640,497), description, font=font_main, fill=(0,0,0,255))
            elif (len(text[3]) == 13) or (len(text[3]) == 14):
                d.text((652,497), description, font=font_main, fill=(0,0,0,255))
            elif (len(text[3]) == 11) or (len(text[3]) == 12):
                d.text((660,497), description, font=font_main, fill=(0,0,0,255))
            elif (len(text[3]) == 9) or (len(text[3]) == 10):
                d.text((665,497), description, font=font_main, fill=(0,0,0,255))

            if (len(text[2]) == 6):
                d.text((275,497), money, font=font_main, fill=(0,0,0,255))
                d.text((443,497), money, font=font_main, fill=(0,0,0,255))
            elif (len(text[2]) == 7):
                d.text((273,497), money, font=font_main, fill=(0,0,0,255))
                d.text((440,497), money, font=font_main, fill=(0,0,0,255))
            elif (len(text[2]) == 8):
                d.text((268,497), money, font=font_main, fill=(0,0,0,255))
                d.text((435,497), money, font=font_main, fill=(0,0,0,255))


            tink.save("Image cache/file_tk_transaction.png", "PNG")
            img = open('Image cache/file_tk_transaction.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_kufar_c2c(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")

            time = text[0]
            date = text[1]
            card = text[2]
            card_name = f"Карта 1 ({card[-4:]})"
            purchase = text[3] + " BYN"
            comission = text[4] + " BYN"
            payments = Comissions(float(text[3]) + float(text[4])) + " BYN"

            tink = Image.open('Image source/Kufar/kufar_c2c.png')

            font_time = ImageFont.truetype('Fonts/Iphone-Regular.ttf', 21)
            font_main = ImageFont.truetype('Fonts/Iphone-Regular.ttf', 32)
            
            d = ImageDraw.Draw(tink)

            d.text((330,6), time, font=font_time, fill=(255,255,255,255))

            d.text((439,266), date, font=font_main, fill=(0,0,0,255))
            d.text((390,330), card, font=font_main, fill=(0,0,0,255))
                   
            W = 720
            w1, h1 = font_main.getsize(comission)
            w2, h2 = font_main.getsize(purchase)
            w3, h3 = font_main.getsize(payments)
            w4, h4 = font_main.getsize(card_name)


            d.text(((W - 35 - w1), 470), comission, font=font_main, fill=(0,0,0,255))
            d.text(((W - 35 - w2), 399), purchase, font=font_main, fill=(0,0,0,255))
            d.text(((W - 35 - w3), 533), payments, font=font_main, fill=(0,0,0,255))
            d.text(((W - 35 - w4), 600), card_name, font=font_main, fill=(0,0,0,255))

            tink.save("Image cache/file_kufar_c2c.png", "PNG")
            img = open('Image cache/file_kufar_c2c.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_kufar_transfer(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")

            time = text[0]
            date = text[1]
            profit = text[2]
            summ = text[2] + " BYN"
            card = text[3]

            tink = Image.open('Image source/Kufar/kufar_transfer.png')

            font_time = ImageFont.truetype('Fonts/Iphone-Regular.ttf', 21)
            font_main = ImageFont.truetype('Fonts/Iphone-Regular.ttf', 32)
            
            d = ImageDraw.Draw(tink)

            d.text((330,6), time, font=font_time, fill=(255,255,255,255))
            d.text((439,266), date, font=font_main, fill=(0,0,0,255))
            d.text((598,851), card, font=font_main, fill=(0,0,0,255))

            W = 720
            w1, h1 = font_main.getsize(profit)
            w2, h2 = font_main.getsize(summ)


            d.text(((W - 35 - w1), 720), profit, font=font_main, fill=(0,0,0,255))
            d.text(((W - 35 - w2), 782), summ, font=font_main, fill=(0,0,0,255))


            tink.save("Image cache/file_kufar_transfer.png", "PNG")
            img = open('Image cache/file_kufar_transfer.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_kaspi_balance(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")

            time = text[0]
            balance = text[1]
            last = text[2]

            tink = Image.open('Image source/Kaspi/kaspi_balance.png')

            font_time = ImageFont.truetype('Fonts/ArialRegular.ttf', 21)
            font_card = ImageFont.truetype('Fonts/ArialRegular.ttf', 17)
            font_main = ImageFont.truetype('Fonts/ArialRegular.ttf', 28)
            
            d = ImageDraw.Draw(tink)

            d.text((20,21), time, font=font_time, fill=(255,255,255,255))
            d.text((128,259.6), last, font=font_card, fill=(159,159,159,255))

            W = 576
            w1, h1 = font_main.getsize(balance)

            d.text(((W - 48 - w1), 220), balance, font=font_main, fill=(48,48,48,255))

            tink.save("Image cache/file_kaspi_balance.png", "PNG")
            img = open('Image cache/file_kaspi_balance.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)        

def fake_monobank_balance(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")

            operator = text[0]
            time = text[1]
            money = "₴"

            tink = Image.open('Image source/Monobank/mb_balance.png')

            font_time = ImageFont.truetype('Fonts/ArialRegular.ttf', 21)
            font_card = ImageFont.truetype('Fonts/ArialRegular.ttf', 17)
            font_money = ImageFont.truetype('Fonts/ArialRegular.ttf', 48)
            font_main = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 64)
            
            d = ImageDraw.Draw(tink)

            d.text((331,6), time, font=font_time, fill=(255,255,255,255))
            d.text((50,6), operator, font=font_time, fill=(255,255,255,255))

            W = 720
            W1 = 0
            w1, h1 = font_main.getsize(money)
            w2, h2 = font_main.getsize(text[2])

            d.text(((W - 335 - w1), 240), money, font=font_money, fill=(255,255,255,255))
            d.text(((W1 + 80), 223), text[2], font=font_main, fill=(255,255,255,255))

            tink.save("Image cache/file_mb_balance.png", "PNG")
            img = open('Image cache/file_mb_balance.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)   

def fake_olxpl_transfer(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")

            date = text[0]
            payment = '-' + text[1]
            money = 'PLN'


            today = datetime.date.today()
            today = today.strftime("%d.%m.%Y")


            tink = Image.open('Image source/OLX.pl/olx_transfer.png')

            font_time = ImageFont.truetype('Fonts/ArialRegular.ttf', 19)
            font_main = ImageFont.truetype('Fonts/ArialRegular.ttf', 24)
            font_money = ImageFont.truetype('Fonts/ArialBold.ttf', 54)
            
            d = ImageDraw.Draw(tink)

            d.text((160,140), today, font=font_time, fill=(125,125,125,255))
            d.text((25,830), date, font=font_main, fill=(255,255,255,255))

            W = 0
            w1, h1 = font_money.getsize(payment)

            d.text((30, 250), payment, font=font_money, fill=(0,0,0,255))

            d.text(((W + 48 + w1), 275), money, font=font_main, fill=(0,0,0,255))

            tink.save("Image cache/file_olxpl_transfer.png", "PNG")
            img = open('Image cache/file_olxpl_transfer.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)   

def fake_olxkz_transfer(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")

            date = text[0]
            name = text[1]
            payment = text[2]


            tink = Image.open('Image source/OLX.kz/olx_transfer.png')

            font_main = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 13)
            font_money = ImageFont.truetype('Fonts/Iphone-Regular.ttf', 24)
            
            d = ImageDraw.Draw(tink)

            d.text((179,459), date, font=font_main, fill=(60,60,60,255))
            d.text((179,487), name, font=font_main, fill=(60,60,60,255))
            d.text((20,362), payment, font=font_money, fill=(60,60,60,255))

            tink.save("Image cache/file_olxkz_transfer.png", "PNG")
            img = open('Image cache/file_olxkz_transfer.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_nova_poshta(message):
    try:
        if (message.text not in banned):
            text = message.text.split('\n')


            city = text[0] # город
            street = text[1] # адрес
            name_send = text[2] # имя отправителя
            phone_send = text[3] # номер отправителя
            city_get = text[4] # город получателя
            name_get = text[5] # имя получателя
            street_get = text[6] # адрес получателя
            phone_get = text[7] # номер получателя
            amount = text[8] # кол-во мест на складе
            gram = text[9] # вес поссылки
            price_delivery = text[10] # цена доставки
            price_tovar = text[11] # цена поссылки
            desc = text[12]


            tink = Image.open('Image source/NovaPoshta/transaction.png')
            font_main = ImageFont.truetype('Fonts/ArialNova.ttf', 18)
            font_price = ImageFont.truetype('Fonts/ArialNova-Bold.ttf', 21)
            
            d = ImageDraw.Draw(tink)

            d.text((130,183), city, font=font_main, fill="#3E3E3E") # 
            d.text((70,300), street, font=font_main, fill="#3E3E3E") # 
            d.text((70,242), name_send, font=font_main, fill="#3E3E3E") # 
            d.text((70,356), phone_send, font=font_main, fill="#3E3E3E") # 
            d.text((130,580), city_get, font=font_main, fill="#3E3E3E") #
            d.text((70,638), name_get, font=font_main, fill="#3E3E3E") # 
            d.text((70,696), street_get, font=font_main, fill="#3E3E3E") # 
            d.text((70,755), phone_get, font=font_main, fill="#3E3E3E") #
            d.text((460,193), amount, font=font_main, fill="#3E3E3E") #
            d.text((580,193), gram, font=font_main, fill="#3E3E3E") #
            d.text((460,267), price_tovar, font=font_main, fill="#3E3E3E") #
            d.text((460,320), desc, font=font_main, fill="#3E3E3E") #
            d.text((480,638), price_delivery, font=font_price, fill="#3E3E3E") #

            tink.save("Image cache/file_nova_poshta.png", "PNG")
            img = open('Image cache/file_nova_poshta.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
    except Exception as e:
        print(e)

def fake_boxberry(message):
    try:
        if (message.text not in banned):
            text = message.text.split('\n')


            name = text[0]
            surname = text[1]
            ves = text[2] + 'кг'
            tovar = text[3]


            tink = Image.open('Image source/Boxberry/transaction.png')
            font_main = ImageFont.truetype('Fonts/ArialBold.ttf', 15)
            font_price = ImageFont.truetype('Fonts/ArialRegular.ttf', 24)
            
            d = ImageDraw.Draw(tink)

            d.text((354,414), name, font=font_main, fill="#6E7681") # 
            d.text((350,454), surname, font=font_main, fill="#6E7681") # 

            W = 920
            w, h = font_price.getsize(tovar)
            w1, h1 = font_price.getsize(ves)
            w2, h2 = font_price.getsize(surname)

            d.text(((W - w1) / 2, 704), ves, font=font_price, fill="#525866")
            d.text(((W - w - 20) / 2, 733), tovar, font=font_price, fill="#525866")
            d.text(((W - w2 - 20) / 2, 763), surname, font=font_price, fill="#525866")

            tink.save("Image cache/file_boxberry_tr.png", "PNG")
            img = open('Image cache/file_boxberry_tr.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_betwinner(message):
    try:
        if (message.text not in banned):
            text = message.text.split('\n')

            name = text[0]
            time = text[1]
            money = text[2]
            k = text[3]
            title = text[4]
            community = text[5]
            time_1 = text[6]

            payment = Comissions(float(money) * float(k))

            tink = Image.open('Image source/BetWinner/transaction.png')
            font_main = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 21)
            font_title = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 19)
            font_price = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 21)
            
            d = ImageDraw.Draw(tink)

            d.text((48,110), name, font=font_main, fill="#000000") #
            d.text((47,140), time, font=font_main, fill="#808080") #  

            W = 720
            w, h = font_price.getsize(money)
            w1, h1 = font_price.getsize(k)
            w2, h2 = font_price.getsize(payment + ' ₽')

            d.text(((W - w - 70), 114), money, font=font_price, fill="#000000")
            d.text(((W - w1 - 70), 145), k, font=font_main, fill="#808080")
            d.text(((W - w2 - 70), 180), payment + ' ₽', font=font_main, fill="#00B245")

            d.text((47,260), title, font=font_title, fill="#000000") # 

            if (len(text[5]) < 45):
                d.text((47,290), community, font=font_main, fill="#000000")
                d.text((47,320), time_1, font=font_main, fill="#808080") # 
                d.text((48,385), 'П1', font=font_main, fill="#000000") #
            else:
                first = community[:40]
                a = len(community) - 40
                second = community[-a:]

                if (second[0] == ' '):
                    second = second[1:]

                d.text((47,290), first, font=font_main, fill="#000000")
                d.text((47,320), second, font=font_main, fill="#000000")
                d.text((47,350), time_1, font=font_main, fill="#808080") #

                d.text((48,385), 'П1', font=font_main, fill="#000000") # 


            d.text(((W - w1 - 70), 410), k, font=font_main, fill="#00B245")

            tink.save("Image cache/file_betwinner.png", "PNG")
            img = open('Image cache/file_betwinner.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())

    except Exception as e:
        print(e)

def fake_parimatch(message):
    try:
        if (message.text not in banned):
            text = message.text.split('\n')


            time = text[0]
            balance = text[1]
            date = text[2]
            name = text[3]
            k = text[4]
            payment = text[5] + ' UAH'
            refund = text[6] + ' UAH'


            express = '#' + str(random.randint(0, 99))
            bet = Comissions(float(text[5]) * float(text[4])) + ' UAH'


            tink = Image.open('Image source/PariMatch/transaction.png')
            font_other = ImageFont.truetype('Fonts/ArialRegular.ttf', 21)
            font_bold = ImageFont.truetype('Fonts/ArialBold.ttf', 20)
            font_name = ImageFont.truetype('Fonts/ArialBold.ttf', 21)
            font_refund = ImageFont.truetype('Fonts/ArialBold.ttf', 25)
            
            d = ImageDraw.Draw(tink)

            d.text((20,10), time, font=font_other, fill='#646464')
            d.text((165,328), date, font=font_other, fill='#646464')
            d.text((115,330), express, font=font_bold, fill='#646464')
            d.text((28,400), name, font=font_name, fill='#000000')
            d.text((165,452), payment, font=font_bold, fill='#000000')
            d.text((215,487), bet, font=font_bold, fill='#454545')
            d.text((315,585), refund, font=font_refund, fill='#080200')


            W = 623
            w1, h1 = font_bold.getsize(balance)
            w2, h2 = font_name.getsize(k)

            d.text(((W - 66 - w1), 180), balance, font=font_bold, fill=(255,255,255,255))
            d.text(((W - 35 - w2), 400), k, font=font_name, fill=(0,0,0,255))

            tink.save("Image cache/file_parimatch.png", "PNG")
            img = open('Image cache/file_parimatch.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_mailto_youla(message):
    try:
        if (message.text not in banned):


            tink = Image.open('Image source/Youla/mail.png')
            font_other = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 24)
            
            d = ImageDraw.Draw(tink)
            offset = 550

            if '\n' in message.text:
                text = message.text.split('\n')

            if len(message.text) > 50:
                for txt in text:
                    messages = textwrap.wrap(txt, width = 50)
                    for msg in messages:
                        d.text((30, offset), msg, font=font_other, fill="#000000")
                        offset += 25
                    offset += 25   
            else:
                d.text((93, offset), message.text, font=font_other, fill="#000000")


            tink.save("Image cache/file_youla.png", "PNG")
            img = open('Image cache/file_youla.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_refundto_youla(message):
    try:
        if (message.text not in banned):


            tink = Image.open('Image source/Youla/refund.png')
            font_other = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 24)
            
            d = ImageDraw.Draw(tink)

            d.text((40,25), message.text, font=font_other, fill='#000000')


            tink.save("Image cache/file_refundyoula.png", "PNG")
            img = open('Image cache/file_refundyoula.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_mailto_avito(message):
    try:
        if (message.text not in banned):


            tink = Image.open('Image source/Avito/mail.png')
            font_other = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 24)
            
            d = ImageDraw.Draw(tink)
            offset = 510

            if '\n' in message.text:
                text = message.text.split('\n')


            if len(message.text) > 45:
                for txt in text:
                    messages = textwrap.wrap(txt, width = 45)
                    for msg in messages:
                        d.text((20, offset), msg, font=font_other, fill="#000000")
                        offset += 25
                    offset += 25  
            else:
                d.text((20, offset), message.text, font=font_other, fill="#000000")

            tink.save("Image cache/file_avito.png", "PNG")
            img = open('Image cache/file_avito.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_sportbank_transfer(message):
    try:
        if (message.text not in banned):
            text = message.text.split('\n')

            time = text[0]
            paytime = text[1]
            money_1 = text[2]
            money_2 = '.' + text[3] + ' ₴'
            balance = text[4] + ' ₴'

            tink = Image.open('Image source/SportBank/sportbank.png')

            font_21 = ImageFont.truetype('Fonts/Iphone-Regular.ttf', 21)
            font_31 = ImageFont.truetype('Fonts/Iphone-Regular.ttf', 31)
            font_40 = ImageFont.truetype('Fonts/Iphone-Medium.ttf', 48)
            font_48 = ImageFont.truetype('Fonts/Iphone-Medium.ttf', 100)

            d = ImageDraw.Draw(tink)

            d.text((340,6), time, font=font_21, fill=(255,255,255,255))
            d.text((130,675), balance, font=font_31, fill=(0,0,0,255))

            W, H = (719, 1280)

            w, h = font_31.getsize(paytime)
            w1, h1 = font_48.getsize(money_1)
            w2, h2 = font_40.getsize(money_2)
            
            d.text(((W - w) / 2 , 385), paytime, font = font_31, fill='#6B6B6B')
            d.text(((W - w1 - w2) / 2, 430), money_1, font = font_48, fill='#000')
            d.text(((W + w1 - w2) / 2, 480), money_2, font = font_40, fill='#000')

            tink.save("Image cache/sportbank_transfer.png", "PNG")
            img = open('Image cache/sportbank_transfer.png', 'rb')
            bot.send_photo(message.chat.id, img)
            show_adverting(message.chat.id)
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)




def add_warning(message):
    try:

        array = message.text.split(' ')

        ID = array[0]
        WARNING = array[1]


        if not db.user_exists_database(ID):

            bot.send_message(message.chat.id, 'Пользователь не найден')

        else:

            db.user_update_warning(ID, WARNING)

            if int(WARNING) > 0:
                bot.send_message(ID, f'⚠️ ТС {message.from_user.first_name} выдал вам баллы, при достижении трёх баллов доступ к боту будет ограничен')

            bot.send_message(message.chat.id, f'Количество баллов у пользователя {ID}: {db.user_warning(ID)}')

    except:
    	pass

