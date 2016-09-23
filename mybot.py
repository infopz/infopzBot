import botogram
import requests
import datetime
import time
from urllib.request import urlopen

def dataTempo():
   current_time = time.localtime()
   dt=time.strftime('%Y.%m.%d,%H.%M', current_time)
   return dt

def ottieniCambio():
   data=urlopen("http://dollaro-euro.it/")
   page= str(data.read())
   page=page[3035:]
   page=float(page[0:6])
   return(page)

bot = botogram.create("290577957:AAGu15bceNMkGllsC8Hk7M6AhE2vbkItfCE")
bot.about="Questo è il bot di Infopz"
bot.owner="@infopz"

@bot.command("hello")
def hello_command(chat, message, args):
    '''Ciaone!
       \nTi saluta con un bel ciao'''
    chat.send("Hello World")

@bot.command("ds") #salva messaggio ricevuto con ora e data
def save_command(chat, message, args):
    '''Salva il messaggio
       \nQuesto comando salva in un file txt il messaggio indicando a fianco data e ora'''
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
    \nLegge n righe a partire dal fondo nel file CoseSalvate.txt, se non vengono forniti legge l'intero file'''
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

@bot.command("cambio")
def cambio_command(chat, message, args):
    '''Cambia dollari in euro e viceversa
       \nCambia i Dollari in euro e Euro in dollari in base al simbolo di valuta messo dopo il numero. \nSe viene fornita la parola Tasso viene fornito il tasso di cambio €/$'''
    cambio=ottieniCambio()
    n=message.text
    n=n[8:]
    if n=='tasso':
       ris="Il tasso di oggi è "+str(cambio)+" €/$"
    elif (n[-1:])=='€':
       n=float(n[:-1])
       ris=round(float(n/cambio), 3)
       ris=str(n)+"€ sono "+str(ris)+"$"
    elif (n[-1:])=='$':
       n=float(n[:-1])
       ris=round(float(n*cambio), 3)
       ris=str(n)+"$ sono "+str(ris)+"€"
    else:
       ris="Valuta inserita non corretta o non data\nInserici un valore con € o $ alla fine"
    chat.send(ris)

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
