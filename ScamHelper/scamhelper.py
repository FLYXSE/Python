import scamhelper_config
from scamhelper_config import (bot, types, InputMediaPhoto, support, db, keyboard, admin, show_adverting)
from scamhelper_config import (profile_user, user_date, fake_qiwi_balance, fake_qiwi_transfer, fake_tinkoff_transaction,add_all_ad,
							   fake_sber_balance, fake_sber_transfer, fake_yandex_balance, fake_tinkoff_refund,fake_mailto_avito,
							   fake_tinkoff_transfer, fake_tinkoff_youla_transfer, fake_tinkoff_avito_transfer,fake_mailto_youla,
							   fake_kufar_c2c, fake_kufar_transfer, fake_kaspi_balance, fake_monobank_balance, fake_parimatch,send_all_ad,
							   fake_olxpl_transfer, fake_olxkz_transfer, fake_nova_poshta, fake_boxberry, fake_betwinner,fake_refundto_youla,
							   fake_qiwi_get_pc, fake_sportbank_transfer, add_warning)



@bot.message_handler(commands=['start'])  
def callback_run(message):
	try:
		chat_id = message.chat.id
		code = message.text.split()

		if (not db.user_exists_database(chat_id)):

			db.user_add_database(chat_id, '0')
			profile_user(message)

		username = db.user_username(chat_id)
		bot.send_message(chat_id, f'🍀 Привет, <b>{username}</b>!\nНадеюсь, тебе у нас понравится!', parse_mode="html", reply_markup=keyboard.main_keyboard())

	except Exception as e:
		bot.send_message(chat_id, "⚠️ Ошибка при *регистрации* пользователя. Повторите попытку снова написав /start", parse_mode="Markdown")

@bot.message_handler(commands=['auth'])  
def callback_auth(message):
	try:
		chat_id = message.chat.id

		inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
		inline_1 = types.InlineKeyboardButton(text = "Рассылка", callback_data = 'SEND_ALL_AD')
		inline_2 = types.InlineKeyboardButton(text = "Добавить рекламу в сообщения", callback_data = 'ADD_ALL_AD')
		inline_3 = types.InlineKeyboardButton(text = 'Выдать предупреждение', callback_data = 'ADD_WARNING')
		inline_keyboard.add(inline_1, inline_2, inline_3)

		if chat_id == admin:
			bot.send_message(chat_id, '👨‍💻 Меню <b>администратора</b>', parse_mode='html', reply_markup=inline_keyboard)

	except Exception as e:
		pass

@bot.message_handler(content_types=['text'])
def callback_messages(message):
	chat_id = message.chat.id
	access = db.user_warning(chat_id)

	if (access is not None):
		if (access < 3):

			if message.text == '👨‍💼 Информация':

				username = db.user_username(chat_id)
				count = int(db.users_db())
				date = user_date(chat_id)

				inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
				inline_1 = types.InlineKeyboardButton(text = "Прямая связь", url = f'https://t.me/{support}')
				inline_keyboard.add(inline_1)

				bot.send_message(chat_id, f'👨‍💼 Ваш <b>личный кабинет</b>\n\n🚀 Telegram ID: {chat_id}\nПользователь: {username}\n\nАдминистратор: @{support}\nПользователей в боте: <b>{count}</b>\n\n⚠️ Предупреждений: <b>[{access}/3]</b>\nВы уже <b>{date}</b> с нами! Спасибо!',
					parse_mode="html", reply_markup=inline_keyboard)
			elif message.text == '💬 Диалоги':

				bot.send_message(chat_id, '💬 Выберите подходящий для Вас <b>диалог</b>', parse_mode="html", reply_markup=keyboard.dialog_keyboard())
			elif message.text == '👋 Приветствие':

				bot.send_message(chat_id, '👋 <b>Лучшее</b> приветствие\n\n— Добрый день, пишу поповоду Вашего объявления «...». Актуально ещё?', parse_mode="html")
			elif message.text == '🧐 Вопросы о товаре':
				bot.send_message(chat_id, '🧐 Список <b>вопросов</b> о товаре:\n\n• В каком состоянии товар?\n• Когда приобретали товар?\n• Есть какие-либо ньюансы / дефекты?'
					+ '• Всё ли рабочее?\n• Можете отправить доп. фото? Видео?', parse_mode='html')
			elif message.text == '🚚 Доставка':
				bot.send_message(chat_id, '🚚 <b>Лучший</b> способ сказать <b>о доставке</b>\n\n— Очень заинтересован(а) к покупке, готов(а) приобрести, но я в «...» '
					+ 'можно оплатить «...» доставкой? После к Вам приедет курьер по указанному Вами адресу и Вы ему отдадите «...»', parse_mode='html')
			elif message.text == '🙄 Другие вопросы':
				bot.send_message(chat_id, '🙄 <b>Другие</b> вопрос\n\n• «Могу отправить наложкой» — Просто очень понравилась Ваш «...», но к сожалению всей семьей '
					+ 'сидим на карантине, есть только один вариант, это курьер', parse_mode="html")
			elif message.text == '🖼 Готовые скриншоты':

				bot.send_message(chat_id, '🖼 Выберите <b>категорию</b> готовых скриншотов', parse_mode='html', reply_markup=keyboard.screenshot_keyboard())
			elif message.text == 'Авито':

				bot.send_message(chat_id, 'Вы выбрали <b>Авито</b>, выберите скриншоты', parse_mode="html", reply_markup=keyboard.avito_keyboard()) 
			elif message.text == '1.0 Запрос почты':
				a1 = open('Screens/Avito/avito_mail_10_1.png', 'rb')
				a2 = open('Screens/Avito/avito_mail_10_2.png', 'rb')
				a3 = open('Screens/Avito/avito_mail_10_3.png', 'rb')
				a4 = open('Screens/Avito/avito_mail_10_4.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1),InputMediaPhoto(a2), InputMediaPhoto(a3), InputMediaPhoto(a4)]) 
			elif message.text == '1.0 Оплата по ссылке':
				a1 = open('Screens/Avito/avito_paylink.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)]) 
			elif message.text == '2.0 Подозрительный':
				a1 = open('Screens/Avito/avito_suspectlink.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)]) 
			elif message.text == '2.0 Запрос почты':
				a1 = open('Screens/Avito/avito_mail_20_1.png', 'rb')
				a2 = open('Screens/Avito/avito_mail_20_2.png', 'rb')
				a3 = open('Screens/Avito/avito_mail_20_3.png', 'rb')
				a4 = open('Screens/Avito/avito_mail_20_4.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1),InputMediaPhoto(a2), InputMediaPhoto(a3), InputMediaPhoto(a4)]) 
			elif message.text == '3.0 Запрос кода':
				a1 = open('Screens/Avito/avito_code_30_1.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)]) 
			elif message.text == 'Списывание / баланс':
				a1 = open('Screens/Avito/avito_receivebalance_1.png', 'rb')
				a2 = open('Screens/Avito/avito_receivebalance_2.png', 'rb')
				a3 = open('Screens/Avito/avito_receivebalance_3.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1),InputMediaPhoto(a2), InputMediaPhoto(a3)]) 
			elif message.text == 'CVC код':
				a1 = open('Screens/Avito/avito_cvc.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)]) 
			elif message.text == 'Нет уведомлений':
				a1 = open('Screens/Avito/avito_notification_1.png', 'rb')
				a2 = open('Screens/Avito/avito_notification_2.png', 'rb')
				a3 = open('Screens/Avito/avito_notification_3.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1),InputMediaPhoto(a2), InputMediaPhoto(a3)]) 
			elif message.text == 'Как работает доставка (ссылка)':
				a1 = open('Screens/Avito/avito_delivery_link_1.png', 'rb')
				a2 = open('Screens/Avito/avito_delivery_link_2.png', 'rb')
				a3 = open('Screens/Avito/avito_delivery_link_3.png', 'rb')
				a4 = open('Screens/Avito/avito_delivery_link_4.png', 'rb')
				a5 = open('Screens/Avito/avito_delivery_link_5.png', 'rb')
				a6 = open('Screens/Avito/avito_delivery_link_6.png', 'rb')
				a7 = open('Screens/Avito/avito_delivery_link_7.png', 'rb')
				a8 = open('Screens/Avito/avito_delivery_link_8.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1),InputMediaPhoto(a2), InputMediaPhoto(a3), InputMediaPhoto(a4), InputMediaPhoto(a5), InputMediaPhoto(a6),
					InputMediaPhoto(a7), InputMediaPhoto(a8)]) 
			elif message.text == 'Как работает доставка (SMS)':
				a1 = open('Screens/Avito/avito_delivery_sms.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)]) 
			elif message.text == 'Как работает доставка (Email)':
				a1 = open('Screens/Avito/avito_delivery_email.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)]) 
			elif message.text == 'Заказ оформлен, продавец получит средства через sms/ссылку':
				a1 = open('Screens/Avito/avito_payment_1.png', 'rb')
				a2 = open('Screens/Avito/avito_payment_2.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1), InputMediaPhoto(a2)]) 
			elif message.text == 'Возврат':
				a1 = open('Screens/Avito/avito_refund.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)]) 
			elif message.text == 'Получить по ссылке':
				a1 = open('Screens/Avito/avito_get_link.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)]) 
			elif message.text == 'Деньги возвращаются на карту после резервирования (sms)':
				a1 = open('Screens/Avito/avito_refund_money.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)]) 
			elif message.text == 'Авито - 900':
				a1 = open('Screens/Avito/avito_900_1.png', 'rb')
				a2 = open('Screens/Avito/avito_900_2.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1), InputMediaPhoto(a2)]) 
			elif message.text == 'Юла':

				bot.send_message(chat_id, 'Вы выбрали <b>Юла</b>, выберите скриншоты', parse_mode="html", reply_markup=keyboard.youla_keyboard()) # ЮЛА 
			elif message.text == '- 1.0 Запрос почты':
				a1 = open('Screens/Youla/youla_mail_10_1.png', 'rb')
				a2 = open('Screens/Youla/youla_mail_10_2.png', 'rb')
				a3 = open('Screens/Youla/youla_mail_10_3.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1),InputMediaPhoto(a2), InputMediaPhoto(a3)]) 
			elif message.text == '- 1.0 Оплата по ссылке':
				a1 = open('Screens/Youla/youla_delivery_link.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)])
			elif message.text == '- 1.0 900':
				a1 = open('Screens/Youla/youla_10_900.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)]) 
			elif message.text == '- 2.0 900':
				a1 = open('Screens/Youla/youla_20_900_1.png', 'rb')
				a2 = open('Screens/Youla/youla_20_900_2.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1), InputMediaPhoto(a2)]) 
			elif message.text == '- 2.0 Подозрительный':
				a1 = open('Screens/Youla/youla_suspectlink.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)]) 
			elif message.text == '- 3.0 Запрос кода':
				a1 = open('Screens/Youla/youla_code_30.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)]) 
			elif message.text == '- Запрос почты':
				a1 = open('Screens/Youla/youla_getmail_1.png', 'rb')
				a2 = open('Screens/Youla/youla_getmail_1.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1), InputMediaPhoto(a2)]) 
			elif message.text == '- CVC код':
				a1 = open('Screens/Youla/youla_cvc_code_1.png', 'rb')
				a2 = open('Screens/Youla/youla_cvc_code_2.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1), InputMediaPhoto(a2)]) 
			elif message.text == '- Нет уведомлений':
				a1 = open('Screens/Youla/youla_notification_1.png', 'rb')
				a2 = open('Screens/Youla/youla_notification_2.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1), InputMediaPhoto(a2)]) 
			elif message.text == '- Получить по ссылке':
				a1 = open('Screens/Youla/youla_getlink.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)]) 
			elif message.text == '- Возврат':
				a1 = open('Screens/Youla/youla_refund_1.png', 'rb')
				a2 = open('Screens/Youla/youla_refund_2.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1), InputMediaPhoto(a2)]) 
			elif message.text == '- Как работает доставка (ссылка)':
				a1 = open('Screens/Youla/youla_delivery_work_1.png', 'rb')
				a2 = open('Screens/Youla/youla_delivery_work_2.png', 'rb')
				a3 = open('Screens/Youla/youla_delivery_work_3.png', 'rb')
				a4 = open('Screens/Youla/youla_delivery_work_4.png', 'rb')
				a5 = open('Screens/Youla/youla_delivery_work_5.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1), InputMediaPhoto(a2), InputMediaPhoto(a3),
					InputMediaPhoto(a4), InputMediaPhoto(a5)]) 
			elif message.text == 'Другие сервисы':

				bot.send_message(chat_id, 'Вы выбрали <b>Другие сервисы</b>, выберите скриншоты', parse_mode="html", reply_markup=keyboard.other_keyboard()) # ЮЛА 
			elif message.text == '🚕 Яндекс.Доставка 2.0 — как работает доставка':
				a1 = open('Screens/Other/yandex.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)])
			elif message.text == '🚐 Dostavista 2.0 — как работает доставка':
				a1 = open('Screens/Other/dostavista.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)])
			elif message.text == '🚎 Почта РФ 2.0 — как работает доставка':
				a1 = open('Screens/Other/mailrf.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)])
			elif message.text == '🚗 Boxberry 2.0 — как работает доставка':
				a1 = open('Screens/Other/boxberry_20.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)])
			elif message.text == '🚚 Boxberry — оплата по ссылке':
				a1 = open('Screens/Other/boxberry_10.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)])
			elif message.text == '🚛 СДЭК — оплата по ссылке':
				a1 = open('Screens/Other/cdek.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)])
			elif message.text == '🛺 СДЭК 2.0 — как работает доставка':
				a1 = open('Screens/Other/cdek_20.png', 'rb')
				bot.send_media_group(chat_id, [InputMediaPhoto(a1)])
			elif message.text == 'Назад ↩️':

				bot.send_message(chat_id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
			elif message.text == '💸 Чеки / Баланс':

				bot.send_message(chat_id, 'Вы выбрали <b>чеки и балансы</b>, выберите <b>сервис</b> для отрисовки', parse_mode='html', reply_markup=keyboard.wallet_keyboard())
			elif message.text == 'QIWI':

				bot.send_message(chat_id, 'Сервис <b>QIWI</b>, что хотите отрисовать?', parse_mode='html', reply_markup=keyboard.qiwi_keyboard())
			elif message.text == 'Баланс Киви':
				photo = open('Image source/Qiwi/qiwi_balance.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='⏫ Это пример готового скрина\n\nВведите желаемый баланс для отрисовки')
				bot.register_next_step_handler(message, fake_qiwi_balance)
			elif message.text == 'Перевод Киви':
				photo = open('Image source/Qiwi/qiwi_check.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введите необходимые данные:\n\n1️⃣ - сумма перевода\n2️⃣ - номер перевода\n3️⃣ - дату и время\n\nПример:\n500\n+79XXXXXXXXX\n04.12.2021 в 00:27')
				bot.register_next_step_handler(message, fake_qiwi_transfer)
			elif message.text == 'Получение Киви (ПК)':

				message = bot.send_message(chat_id, '☺️ Введите номер кошелька, баланс, название перевода, сумму перевода, комиссию и дату операции\n\nПример:\n+7 967 591‑18‑95\n2500,53\nQIWI Кошелек +79255798115\n25000.14\n100\n13.01.2021 в 11:09', parse_mode='Markdown')
				bot.register_next_step_handler(message, fake_qiwi_get_pc)
			elif message.text == 'Sberbank':

				bot.send_message(chat_id, 'Сервис <b>Сбербанк</b>, что хотите отрисовать?', parse_mode='html', reply_markup=keyboard.sberbank_keyboard())
			elif message.text == 'Баланс Сбербанк':
				photo = open('Image source/Sber/access_balance.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введи необходимые данные:\n\n1️⃣ - системное время\n2️⃣ - баланс\n3️⃣ - последние 4 цифры карты\n\nПример:\n14:37\n25000\n5324')
				bot.register_next_step_handler(message, fake_sber_balance)
			elif message.text == 'Перевод Сбербанк':
				photo = open('Image source/Sber/sber_transfer.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введи необходимые данные:\n\n1️⃣ - системное время\n2️⃣ - сумму перевода\n3️⃣ - ФИО\n\nПример:\n14:37\n5000\nГригорьева Анна В', parse_mode='Markdown')
				bot.register_next_step_handler(message, fake_sber_transfer)
			elif message.text == 'Яндекс.Деньги':

				bot.send_message(chat_id, 'Сервис <b>Яндекс.Деньги</b>, что хотите отрисовать?', parse_mode='html', reply_markup=keyboard.yandex_keyboard())
			elif message.text == 'Баланс ЮMoney':
				photo = open('Image source/Yandex/access.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введи сообщение для создания скриншота\n\nПример:\n23:19\nmylogin\n50 000,51')
				bot.register_next_step_handler(message, fake_yandex_balance)
			elif message.text == 'Tinkoff':

				bot.send_message(chat_id, 'Сервис <b>Тинькофф</b>, что хотите отрисовать?', parse_mode='html', reply_markup=keyboard.tinkoff_keyboard())
			elif message.text == 'Перевод Тинькофф':
				photo = open('Image source/Tinkoff/tinkoff_transfer.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введи необходимые данные:\n\n1️⃣ - системное время\n2️⃣ - сумма перевода\n\nПример:\n23:40\n5000')
				bot.register_next_step_handler(message, fake_tinkoff_transfer)
			elif message.text == 'Тинькофф перевод Юла':
				photo = open('Image source/Tinkoff/tk_youla_transfer.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введи необходимые данные:\n\n1️⃣ - системное время\n2️⃣ - сумма перевода\n\nПример:\n23:40\n5000')
				bot.register_next_step_handler(message, fake_tinkoff_youla_transfer)
			elif message.text == 'Тинькофф перевод Авито':
				photo = open('Image source/Tinkoff/tk_avito_transfer.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введи необходимые данные:\n\n1️⃣ - системное время\n2️⃣ - сумма перевода\n\nПример:\n23:40\n5000')
				bot.register_next_step_handler(message, fake_tinkoff_avito_transfer)
			elif message.text == 'Тинькофф возврат':
				photo = open('Image source/Tinkoff/tinkoff_refund.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введи необходимые данные:\n\n1️⃣ - системное время\n2️⃣ - сумма возврата\n\nПример:\n23:40\n5000')
				bot.register_next_step_handler(message, fake_tinkoff_refund)
			elif message.text == 'Чек Тинькофф':
				message = bot.send_message(chat_id, '☺️ Введите дату операции, ФИО, сумма перевода, описание\n\nПример:\n09.08.2020 10:17:05\nПавлов Александр Захарович\n300.00\nОплата на AVITO.RU', parse_mode="html")
				bot.register_next_step_handler(message, fake_tinkoff_transaction)
			elif message.text == 'Kufar':

				bot.send_message(chat_id, 'Сервис <b>Kufar</b>, что хотите отрисовать?', parse_mode='html', reply_markup=keyboard.kufar_keyboard())
			elif message.text == 'Куфар Card2Card':
				message = bot.send_message(chat_id, 'Введите необходимые данные:\n\n1️⃣ - системное время\n2️⃣ - дату операции\n3️⃣ - номер карты\n4️⃣ - сумму перевода\n5️⃣ - комиссия\n\nПример:\n12:43\n17.09.2020 17:33\n4255 19** **** 3851\n125000\n3500')
				bot.register_next_step_handler(message, fake_kufar_c2c)
			elif message.text == 'Перевод Куфар':
				message = bot.send_message(chat_id, 'Введите необходимые данные:\n\n1️⃣ - системное время\n2️⃣ - дату операции\n3️⃣ - сумму перевода\n4️⃣ - последние 4 цифры карты\n\nПример:\n2:43\n17.09.2020 17:33\n500\n5139')
				bot.register_next_step_handler(message, fake_kufar_transfer)
			elif message.text == 'Kaspi':

				bot.send_message(chat_id, 'Сервис <b>Kaspi</b>, что хотите отрисовать?', parse_mode='html', reply_markup=keyboard.kaspi_keyboard())
			elif message.text == 'Баланс Каспи':
				message = bot.send_message(chat_id, 'Введите необходимые данные:\n\n1️⃣ - системное время\n2️⃣ - желаемый баланс\n3️⃣ - последние 4 цифры карты\n\nПример:\n12:43\n500,10\n3124')
				bot.register_next_step_handler(message, fake_kaspi_balance)
			elif message.text == 'MonoBank':

				bot.send_message(chat_id, 'Сервис <b>MonoBank</b>, что хотите отрисовать?', parse_mode='html', reply_markup=keyboard.monobank_keyboard())
			elif message.text == 'Баланс Monobank':
				photo = open('Image source/Monobank/mb_balance.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введите необходимые данные\n\n1️⃣  - системное время\n2️⃣  - баланс\n\nПример:\nMegaFon LTE\n12:43\n25000')
				bot.register_next_step_handler(message, fake_monobank_balance)
			elif message.text == 'OLX PL':

				bot.send_message(chat_id, 'Сервис <b>OLX PL</b>, что хотите отрисовать?', parse_mode='html', reply_markup=keyboard.olxpl_keyboard())
			elif message.text == 'Перевод OLX (PL)':
				photo = open('Image source/OLX.pl/olx_transfer.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введите необходимые данные:\n\n1️⃣ - дату операции\n2️⃣ - сумму перевода\n\nПример:\n2020-08-12 19:23:25\n8,00')
				bot.register_next_step_handler(message, fake_olxpl_transfer)
			elif message.text == 'OLX KZ':

				bot.send_message(chat_id, 'Сервис <b>OLX KZ</b>, что хотите отрисовать?', parse_mode='html', reply_markup=keyboard.olxkz_keyboard())
			elif message.text == 'Перевод OLX (KZ)':
				photo = open('Image source/OLX.kz/olx_transfer.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введите необходимые данные:\n\n1️⃣ - дату операции\n2️⃣ - ФИО\n3️⃣ - сумму перевода\n\nПример:\n2020-08-12 19:23:25\nАвстралиец В. У.\n80 600,00')
				bot.register_next_step_handler(message, fake_olxkz_transfer)
			elif message.text == '📪 Накладные / поссылки':

				bot.send_message(chat_id, 'Вы выбрали <b>накладные и поссылки</b>, выберите <b>сервис</b> для отрисовки', parse_mode='html', reply_markup=keyboard.delivery_keyboard())
			elif message.text == 'Нова Пошта':
				photo = open('Image source/NovaPoshta/transaction.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введите необходимые данные:\n\n• Город отправителя\n• Адрес отправителя\n• Имя отправителя\n• Номер отправителя'
				+ '\n• Город получателя\n• Имя получателя\n• Адрес получателя\n• Номер получателя\n• Количество мест на складе\n• Вес поссылки\n• Цена доставки\n• Цена поссылки\n• Описание поссылки', parse_mode="html")
				bot.register_next_step_handler(message, fake_nova_poshta)
			elif message.text == 'Boxberry':
				photo = open('Image source/Boxberry/transaction.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введите необходимые данные:\n\n• Имя отправителя\n• Имя получателя\n• Вес поссылки (кг)\n• Название товара\n\nПример:\nСмирнова Анна\nЕфимов Алексей\n70\nКирпичи', parse_mode="html")
				bot.register_next_step_handler(message, fake_boxberry)
			elif message.text == '🎲 Ставки':

				bot.send_message(chat_id, 'Вы выбрали <b>ставки</b>, выберите <b>сервис</b> для отрисовки', parse_mode='html', reply_markup=keyboard.bet_keyboard())
			elif message.text == 'BetWinner':
				photo = open('Image source/BetWinner/access_transaction.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введи необходимые данные для создания скриншота:\n\n1️⃣ - title1\n2️⃣ - time1\n3️⃣ - amount\n4️⃣ - coefficient\n5️⃣ - title2\n6️⃣ - title3\n7️⃣ - time2\n7️⃣ - bet1'
					+ '\n\nПример:\nОДИНОЧНАЯ №11878593025\n19.04.20 | 21:08\n50000.00\n1.732\nSpike volleyball. Товарищеские матчи. Женщины\nМЕКСИКА (LENIN19188) - ТУРЦИЯ (OPTIC777) 3-Й СЕТ 1:0 (26:24)\n19.04.20 | 20:30')
				bot.register_next_step_handler(message, fake_betwinner)
			elif message.text == 'PariMatch':
				photo = open('Image source/PariMatch/access_transaction.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введи необходимые данные для создания скриншота:\n\n1️⃣ - Системное время\n2️⃣ - Баланс с копейками\n3️⃣ - Дату ставки\n4️⃣ - Название ставки\n5️⃣ - Коэффицент\n6️⃣ - Сумма ставки\n7️⃣ - Возврат'
					+ '\n\nПример:\n12:47\n53183.51\n14 сен 2020, 11:45\n5 исходов\n14.381\n500\n40', parse_mode='html')
				bot.register_next_step_handler(message, fake_parimatch)
			elif message.text == '📩 Письма':

				bot.send_message(chat_id, 'Вы выбрали <b>письма</b>, выберите <b>сервис</b> для отрисовки', parse_mode='html', reply_markup=keyboard.mailto_keyboard())
			elif message.text == 'Письмо Юла':
				photo = open('Image source/Youla/access_mail.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='⏫ Это пример готового скрина\n\nВведи сообщение для создания скриншота')
				bot.register_next_step_handler(message, fake_mailto_youla)
			elif message.text == 'Письмо Авито':
				photo = open('Image source/Avito/access_mail.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='⏫ Это пример готового скрина\n\nВведи сообщение для создания скриншота')
				bot.register_next_step_handler(message, fake_mailto_avito)
			elif message.text == 'Юла возврат':
				photo = open('Image source/Youla/access_refund.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='⏫ Это пример готового скрина\n\nВведите системное время')
				bot.register_next_step_handler(message, fake_refundto_youla)
			elif message.text == 'SportBank':
				photo = open('Image source/SportBank/access.png', 'rb')
				message = bot.send_photo(chat_id, photo, caption='Введи необходимые данные для создания скриншота:\n\n1 - системное время\n2 - дата операции\n3 - сумма (без копеек)\n4 - копейки\n5 - баланс\n\nПример:\n21:03\n14 января 2021, 14:37\n500\n00\n2 490.50')
				bot.register_next_step_handler(message, fake_sportbank_transfer)

	else:
		bot.send_message(chat_id, '⚠️ Вы не <b>авторизованы</b>, напишите /start', parse_mode='html')

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
	try:
		chat_id = call.message.chat.id

		if call.data == 'SEND_ALL_AD' and chat_id == admin:
			message = bot.send_message(chat_id, 'Введите рекламное сообщение\nЕсли Вы хотите прикрепить фото разделите сообщение и ссылку на фото знаком (imgur) ;', parse_mode='html')
			bot.register_next_step_handler(message, send_all_ad)
		elif call.data == 'ADD_ALL_AD' and chat_id == admin:
			message = bot.send_message(chat_id, 'Введите рекламное сообщение\n<i>Оно будет появляться при любом действии пользователя</i>', parse_mode='html')
			bot.register_next_step_handler(message, add_all_ad)
		elif call.data == 'SHOW_AD' and chat_id == admin:
			show_adverting(chat_id)
		elif call.data == 'ADD_WARNING' and chat_id == admin:
			message = bot.send_message(chat_id, 'Введите Telegram ID пользователя и количество баллов\n', parse_mode='html')
			bot.register_next_step_handler(message, add_warning)



	except:
		pass


bot.polling(none_stop = True, interval = 0)		