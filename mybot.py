import botogram
import requests
import datetime
import time

#cambio Euro-Dollaro

def dataTempo():
   current_time = time.localtime()
   dt=time.strftime('%Y.%m.%d,%H.%M', current_time)
   return dt

bot = botogram.create("290577957:AAGu15bceNMkGllsC8Hk7M6AhE2vbkItfCE")
bot.about="Questo è il bot di Infopz"
bot.owner="@infopz"



@bot.command("hello")
def hello_command(chat, message, args):
    '''Ciaone!
       Ti saluta con un bel ciao'''
    chat.send("Hello World")

@bot.command("ds") #salva messaggio ricevuto con ora e data
def save_command(chat, message, args):
    '''Salva il messaggio
       Questo comando salva in un file txt il messaggio indicando a fianco data e ora'''
    file = open("CoseSalvate.txt", "a")  
    mr=message.text
    mr=mr[4:]
    dt=dataTempo()  
    ms=dt+" | "+mr+"\n"
    file.write(ms)
    file.close()
    message.reply("Messaggio Salvato!", preview=True, syntax=None, extra=None, notify=True)

@bot.command("leggi")
def leggi_command(chat, message, args):
    '''Legge le cose salvate
    Legge n righe a partire dal fondo nel file CoseSalvate.txt, se non vengono forniti legge l'intero file'''
    file = open("CoseSalvate.txt", "r")
    lines=file.readlines()
    n=message.text
    m=sum(1 for line in open('CoseSalvate.txt')) #calcolo righe file
    if n[7:] is "": #verifica no n
      n=m
    else: n=int(n[7:])
    if n>m:
      chat.send("Non ci sono abbastanza righe\nIl numero massimo è "+str(m)) 
    else: 
      risp=""
      for line in lines[(m-n):m]:
        risp=risp+line
      chat.send(risp[:-1])
      

@bot.message_contains("infopz")
def send_botogram_link(chat, message):
    chat.send("A Rega Bongiorno")

@bot.message_matches(r'([a-zA-Z0-9\-]+)/([a-zA-Z0-9\-\._]+)', multiple=True)
def github_links(chat, message, matches):
    url = "http://www.github.com/{}/{}".format(*matches)
    if requests.head(url).status_code != 404:
        chat.send(url)
    else: chat.send("Il link non puo essere generato")

if __name__ == "__main__":
    bot.run()
