import botogram
import requests
import datetime

'''mettere bagaglio due cifre mese e anno
   provare ad aggiustare roba prima riga'''

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
    i=datetime.datetime.now()
    dt=str(i.year)+"."+str(i.month)+"."+str(i.day)+"."+str(i.hour)+"."+str(i.minute)
    ms="\r"+dt+"_"+mr
    text_file.write(ms)
    text_file.close()
    chat.send("Messaggio "+mr+" salvato correttamente!")

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
