# подключаем модуль для Телеграма
import telebot
import requests
from creds import TOKEN
# указываем токен для доступа к боту
bot = telebot.TeleBot(TOKEN)

# приветственный текст
start_txt = 'Привет! Это бот прогноза погоды. \n\nОтправьте боту название города и он скажет, какая там температура и как она ощущается.'


# обрабатываем старт бота
@bot.message_handler(commands=['start'])
def start(message):
    # выводим приветственное сообщение
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')

# обрабатываем любой текстовый запрос
@bot.message_handler(content_types=['text'])
def weather(message):
    # получаем город из сообщения пользователя
  city = message.text
  # формируем запрос
  url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&'+key
  # отправляем запрос на сервер и сразу получаем результат
  weather_data = requests.get(url).json()
  # получаем данные о температуре и о том, как она ощущается
  description = str(weather_data["weather"][0]["description"])
  temperature = round(weather_data['main']['temp'])
  temperature_feels = round(weather_data['main']['feels_like'])
  # формируем ответы
  w_now6 = 'Сейчас в городе ' + city + ' ' + str(description) + '.'
  w_now = 'Сейчас в городе ' + city + ' ' + str(temperature) + ' °C'
  w_feels = 'Ощущается как ' + str(temperature_feels) + ' °C'
  # отправляем значения пользователю
  bot.send_message(message.from_user.id, w_now6)
  bot.send_message(message.from_user.id, w_now)
  bot.send_message(message.from_user.id, w_feels)
  wind_speed = round(weather_data['wind']['speed'])
  if wind_speed < 5:
      bot.send_message(message.from_user.id, '✅ Погода хорошая, ветра почти нет')
  elif wind_speed < 10:
      bot.send_message(message.from_user.id, '🤔 На улице ветрено, оденьтесь чуть теплее')
  elif wind_speed < 20:
      bot.send_message(message.from_user.id, '❗ Ветер очень сильный, будьте осторожны, выходя из дома')
  else:
      bot.send_message(message.from_user.id, '❌ На улице шторм, на улицу лучше не выходить')  
  cloudse = round(weather_data['clouds']['all'])
  if cloudse != ' ':
    w_now1 = 'Сейчас в городе ' + city + ' ' + 'облачность ' + str(cloudse) + '%.'
    bot.send_message(message.from_user.id, w_now1)
  raine = round(weather_data['rain']['1h']) * 10
  if raine != ' ':
    w_now2 = 'Сейчас в городе ' + city + ' ' + 'дождь ' + str(raine) + 'мм.'
    bot.send_message(message.from_user.id, w_now2)
  raine1 = round(weather_data['rain']['3h']) * 10
  if raine1 != ' ':
    w_now3 = 'Сейчас в городе ' + city + ' ' + 'дождь ' + str(raine) + 'мм.'
    bot.send_message(message.from_user.id, w_now3)
  snowe = round(weather_data['snow']['1h']) * 10
  if snowe != ' ':
    w_now4 = 'Сейчас в городе ' + city + ' ' + 'снега ' + str(snowe) + 'мм.'
    bot.send_message(message.from_user.id, w_now4)
  snowe1 = round(weather_data['snow']['3h']) * 10
  if snowe1 != ' ':
    w_now5 = 'Сейчас в городе ' + city + ' ' + 'снега ' + str(snowe1) + 'мм.'
    bot.send_message(message.from_user.id, w_now5)
  wiethers = round(weather_data['weather']['weather.main'])
  if wiethers != ' ':
    w_now6 = 'Сейчас в городе ' + city + ' ' + str(wiethers) + '.'
    bot.send_message(message.from_user.id, w_now6)
  cloudse = round(weather_data['clouds']['all'])


# запускаем бота
if __name__ == '__main__':
    while True:
        # в бесконечном цикле постоянно опрашиваем бота — есть ли новые сообщения
        try:
            bot.polling(none_stop=True, interval=0)
        # если возникла ошибка — сообщаем про исключение и продолжаем работу
        except Exception as e: 
            print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌')
