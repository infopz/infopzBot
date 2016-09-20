import botogram
import requests

bot = botogram.create("290577957:AAGu15bceNMkGllsC8Hk7M6AhE2vbkItfCE")
bot.about="Questo è il bot di Infopz"
bot.owner="@infopz"

text_file = open("Voti.txt", "w")

@bot.command("hello")
def hello_command(chat, message, args):
    chat.send("Hello World")

@bot.command("voto")
def voto_command(chat, message, args):
    a=message.text
    a=a[6:]
    a= a + "\n"
    text_file.write(a)
    text_file.close()
    chat.send("Messaggio "+a+" salvato correttamente!")

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
