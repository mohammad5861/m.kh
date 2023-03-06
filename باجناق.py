
import telebot
import requests
from datetime import date

bot_token = '5788944112:AAFUbjzurrT-pgGrpBzsA4glrSzrMGlA'
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(message):
bot.send_message(message.chat.id, 'به ربات پیش‌بینی شرط‌بندی ورزشی خوش آمدید! لطفاً نام لیگی که می‌خواهید برای آن پیش‌بینی شرط‌بندی دریافت کنید را وارد کنید.')

@bot.message_handler(func=lambda message: True)
def get_predictions(message):
league_name = message.text
today = date.today().strftime('%Y-%m-%d')
url = f'https://api.sportsdata.io/v4/soccer/scores/json/Areas?key=INSERT_VALID_API_KEY_HERE'
response = requests.get(url).json()
area_id = None
for area in response:
if area['Name'] == league_name:
area_id = area['AreaId']
break
if area_id is not None:
url = f'https://api.sportsdata.io/v3/soccer/odds/json/GameOddsByDate/{today}?key=INSERT_VALID_API_KEY_HERE'
response = requests.get(url).json()
odds = []
for item in response:
if item['LeagueId'] == area_id:
odds.append(item['Odds'])
if len(odds) > 0:
average_odds = sum(odds) / len(odds)
if average_odds > 1:
bot.send_message(message.chat.id, f'میانگین شانس‌های شرط‌بندی برای {league_name} برابر با {average_odds:.2f} است. شما می‌توانید در نظر داشته باشید که شرطی برای این بازی بگذارید.')
else:
bot.send_message(message.chat.id, 'میانگین شانس‌ها کمتر از یک است، لذا شاید ایده خوبی برای شرط‌بندی نباشد.')
else:
bot.send_message(message.chat.id, 'هیچ شانسی برای این لیگ یافت نشد.')
else:
bot.send_message(message.chat.id, 'نام لیگ نامعتبر است. لطفاً دوباره امتحان کنید.')   
