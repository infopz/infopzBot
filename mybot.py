import botogram
import requests
import time
from datetime import datetime
from urllib.request import urlopen

import sport
import apiKey
import topsec
import altriCom

def control(mess):
  usPer = open("utentiPermessi.txt", "r")
  perm=False
  for line in usPer.readlines():
    if mess.sender.username==line[:-1]:
       perm=True
       a=mess.text
       b='@'+mess.sender.username
       now = datetime.now()
       h=str(time.strftime('%H'))
       m=str(time.strftime('%M'))
       s=str(time.strftime('%S'))
       mes=str(h)+':'+str(m)+'.'+str(s)+' -  COMMAND  - '+b+' '+a
    else:
       a=mess.text
       b='@'+mess.sender.username
       now = datetime.now()
       h=str(time.strftime('%H'))
       m=str(time.strftime('%M'))
       s=str(time.strftime('%S'))
       mes=str(h)+':'+str(m)+'.'+str(s)+' -   DENIED   - '+b+' '+a
    print (mes)
  return perm

def dataTempo():
   current_time = time.localtime()
   dt=time.strftime('%Y.%m.%d,%H.%M', current_time)
   return dt

def buongiorno(num, nome):
   cord=altriCom.trovaCord('Modena')
   dat=altriCom.ottieniDati(str(cord[0]),str(cord[1]))
   mess=altriCom.mOrario(dat)
   bot.chat(num).send('Buongiorno '+nome+'!\nEcco le previsioni meteo per questa giornata')
   bot.chat(num).send(mess)

keyBot = apiKey.apiBot()

bot = botogram.create(keyBot)
bot.about ="Questo è il bot di Infopz\nUtilizza l'opzione /help per ottenere un elenco di tutti i comandi e delle possibili opzioni"
bot.owner="@infopz"

@bot.command("hello")
def hello_command(chat, message, args):
    '''Ciaone!
       \nTi saluta con un bel ciao'''
    if control(message)==False:
       chat.send("Non sei autorizzato a eseguire questo comando")
    else: 
       chat.send("Hello World")

@bot.command("ds") #salva messaggio ricevuto con ora e data
def save_command(chat, message, args):
    '''Salva il messaggio
       \nQuesto comando salva in un file txt il messaggio indicando a fianco data e ora'''
    if control(message)==False:
       chat.send("Non sei autorizzato a eseguire questo comando")
    else:
       file = open("CoseSalvate.txt", "a")  
       mr=message.text
       mr=mr[4:]
       if mr=='':
         chat.send('Scrivi qualcosa da salvare!')
       else:
         dt=dataTempo()  
         ms=dt+" | "+mr+"\n"
         file.write(ms)
         message.reply("Messaggio Salvato!", preview=True, syntax=None, extra=None, notify=True)
       file.close()

@bot.command("leggi")
def leggi_command(chat, message, args):
    '''Legge le cose salvate
    \nLegge n righe a partire dal fondo nel file CoseSalvate.txt, se non vengono forniti legge l'intero file'''
    if control(message)==False:
       chat.send("Non sei autorizzato a eseguire questo comando")
    else:
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
    if control(message)==False:
       chat.send("Non sei autorizzato a eseguire questo comando")
    else:
       cambio=altriCom.ottieniCambio()
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

@bot.command('seriea')
def seriea_command(chat, message, args):
    '''Visualizza Partite e Classifica Serie A
    \nOpzioni:
    \nSe non specificato niente mostra le partite della prossima giornata
    \nSe viene specificata una giornata mostra le partite di quella giornata e gli eventuali risultati
    \nSe aggiungi oggi dopo il comando mostra le partite in programma per oggi con i relativi orari
    \nSe si aggiunge l'opzione domani esegue la stessa cosa di 'oggi' ma con la giornata di domani
    \nCon l'opzione 'classifica' viene viasulizzata la classifica di serie a'''
    if control(message)==False:
       chat.send("Non sei autorizzato a eseguire questo comando")
    else:
       m=message.text
       m=m[8:]
       a=["",""]
       oggi=sport.trovaGiornata()
       if m=="":
         a=sport.partiteGior(oggi)
       elif m=="classifica":
         a[1]=sport.classifica()
         a[0]="Ecco la classifica di Serie A"
       elif m=='oggi':
         a[0]='Ecco le partite di oggi'
         a[1]=sport.partiteOggi(oggi)
         if a[1]=='':
           a[0]='Non ci sono parite oggi'
       elif m=='domani':
         a[0]='Ecco le partite di domani'
         a[1]=sport.partiteDomani(oggi)
         if a[1]=='':
           a[0]='Non sono previste partite per domani'
       else:
         a=sport.partiteGior(m)
       if a[0]!='': chat.send(a[0])
       if a[1]!='': chat.send(a[1])


@bot.command('ip')
def ip_command(chat, message, args):
   '''Visualizza l'ip pubblico di Infopz
    \nComando da usare per aggiornate il mio ip dinamico nel caso non lo facesse in automatico'''
   if control(message)==False:
     chat.send("Non sei autorizzato a eseguire questo comando")
   else:
     data=urlopen("http://www.whatismypublicip.com/")
     page= str(data.read())
     page=page[5480:]
     page=page[:11]
     chat.send("L'indirizzo pubblico di infopz è "+page)


#Da Finire
'''@bot.command('orario')
def orario_command(chat, message, args):
   dt=sport.dataOra()
   orar=sport.crGiornS()
   now = datetime.now()
   d=int(now.isoweekday())-1
   chat.send("Ecco l'orario di oggi")
   for i in orar[d]:
     a=i + '\n'
     tot=tot+a'''

@bot.command('meteo')
def meteo_command(chat, message, args):
  '''Visualizza il Meteo Orario o Giornaliero
    \nOpzioni:
    \nSe non specificato niente mostra il meteo orario per Modena
    \nSe viene specificato l'opzione 'd' viene visualizzato il meteo per i prossimi giorni
    \nSe viene specifica una citta' mostra il meteo (orario o giornaliero) per quella determinata citta', se non viene specificato niente la citta' di default e' Modena'''
  if control(message)==False:
       chat.send("Non sei autorizzato a eseguire questo comando")
  else:
    m=message.text
    m=m[7:]+' '
    mes = m.split(' ', 2)
    if mes[0]=='':
      cord=altriCom.trovaCord('Modena')
      dat=altriCom.ottieniDati(str(cord[0]),str(cord[1]))
      mess=altriCom.mOrario(dat)
    elif mes[0]=='d':
      if mes[1]=='':
        cord=altriCom.trovaCord('Modena')
        dat=altriCom.ottieniDati(str(cord[0]),str(cord[1]))
        mess=altriCom.mGiorni(dat)
      else:
        cord=altriCom.trovaCord(mes[1])
        dat=altriCom.ottieniDati(str(cord[0]),str(cord[1]))
        mess=altriCom.mGiorni(dat)
    else:
      cord=altriCom.trovaCord(mes[0])
      dat=altriCom.ottieniDati(str(cord[0]),str(cord[1]))
      mess=altriCom.mOrario(dat)
    chat.send(mess)
   
@bot.command('inviaID')
def prova_command(chat, message, args):
  '''Invia il tuo chat ID a Infopz
    \nInvia a Infopz l'ID della tua chat con il Bot'''
  a=mess.text
  b='@'+mess.sender.username
  now = datetime.now()
  h=str(time.strftime('%H'))
  m=str(time.strftime('%M'))
  s=str(time.strftime('%S'))
  print(str(h)+':'+str(m)+'.'+str(s)+' -  COMMAND  - '+b+' '+a)
  print(message.sender.id)

@bot.timer(60)
def spam(bot):
   now = datetime.now()
   h=now.hour
   m=now.minute
   if h==7 and m==55: 
     buong = open('buongiorno', 'r')
     for lines in buong.readlines():
        l = lines.split(' ', 2)
        buongiorno(l[0], l[1][:-1])
     buong.close()

if __name__ == "__main__":
    bot.run()
