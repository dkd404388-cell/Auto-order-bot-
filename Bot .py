import telebot, time, requests
from bs4 import BeautifulSoup

TOKEN = "8422335582:AAFKMoPKxnEtzESZEMmnEarz7wEgUo2Q6UI"
ADMIN = 1974904572

bot = telebot.TeleBot(TOKEN)

watchlist = {}

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "🤖 Shein Auto Buyer Online\nUse /add <url>")

@bot.message_handler(commands=['add'])
def add(m):
    try:
        url = m.text.split(" ",1)[1]
        watchlist[url] = False
        bot.send_message(ADMIN, "Added:\n"+url)
    except:
        bot.send_message(m.chat.id, "Usage: /add <shein product url>")

def check_loop():
    while True:
        for url in watchlist:
            try:
                r = requests.get(url, timeout=10)
                if "Out of stock" not in r.text:
                    if not watchlist[url]:
                        bot.send_message(ADMIN, "🔥 IN STOCK!\n"+url)
                        watchlist[url] = True
                else:
                    watchlist[url] = False
            except:
                pass
        time.sleep(15)

import threading
threading.Thread(target=check_loop).start()

bot.infinity_polling()
