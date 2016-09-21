import botogram
import requests
import datetime
import time

'''comando Read
   cambio Euro-Dollaro'''

def dataTempo():
   current_time = time.localtime()
   dt=time.strftime('%Y.%m.%d,%H.%M', current_time)
   return dt

bot = botogram.create("290577957:AAGu15bceNMkGllsC8Hk7M6AhE2vbkItfCE")
bot.about="Questo è il bot di Infopz"
bot.owner="@infopz"

text_file = open("CoseSalvate.txt", "a")

@bot.command("hello")
def hello_command(chat, message, args):
    chat.send("Hello World")

@bot.command("ds") #salva messaggio ricevuto con ora e data
def save_command(chat, message, args):
    mr=message.text
    mr=mr[4:]
    dt=dataTempo()
    ms=dt+" _ "+mr+"\n"
    text_file.write(ms)
    text_file.close()
    message.reply("Messaggio Salvato!", preview=True, syntax=None, extra=None, notify=True)

@bot.message_contains("infopz")
def send_botogram_link(chat, message):
    chat.send("A Rega Bongiorno")

@bot.message_matches(r'([a-zA-Z0-9\-]+)/([a-zA-Z0-9\-\._]+)', multiple=True)
def apple_links(chat, message, matches):
    url = "http://www.{}.com/{}".format(*matches)
    if requests.head(url).status_code != 404:
        chat.send(url)

if __name__ == "__main__":
    bot.run()


text_file.close()
