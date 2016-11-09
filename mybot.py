import botogram
import requests
import time
from datetime import datetime
from urllib.request import urlopen
from wakeonlan import wol

import sport
import apiKey
import altriCom

keyBot = apiKey.apiBot()

bot = botogram.create(keyBot)
bot.about ="Questo è il bot di Infopz\nUtilizza l'opzione /help per ottenere un elenco di tutti i comandi e delle possibili opzioni"
bot.owner="@infopz"


@bot.command("hello", hidden=True)
def hello_command(chat, message, args):
    '''Ciaone!
       \nTi saluta con un bel ciao'''
    control(message)
    chat.send("Hello World")

#SERIEA COMMANDS
@bot.command('seriea')
def seriea_command(chat, message, args, shared):
    '''Visualizza Partite e Classifica Serie A
    \nOpzioni:
    \nSe non specificato niente mostra le partite della prossima giornata
    \nSe viene specificata una giornata mostra le partite di quella giornata e gli eventuali risultati
    \nSe aggiungi oggi dopo il comando mostra le partite in programma per oggi con i relativi orari
    \nSe si aggiunge l'opzione domani esegue la stessa cosa di 'oggi' ma con la giornata di domani
    \nCon l'opzione 'classifica' viene viasulizzata la classifica di serie a'''
    control(message)
    shared['comm'] = 'seriea'
    bot.api.call("sendMessage", {"chat_id": chat.id, "text": '/seriea: seleziona una opzione', "parse_mode": "HTML", "reply_markup": '{"keyboard": [[{"text": "\U0001F5DEPartite Giornata"}, {"text": "\U0001F51BPartite di Oggi"}], [{"text": "\U0001F51CPartite di Domani"}, {"text": "\U0001F4CAClassifica"}], [{"text":"\U000023F1RisultatiLive"}, {"text":"ScorsaGiorn"}]], "one_time_keyboard": false, "resize_keyboard": true}'})

def serieaOutput(m, chat, shared):
  a=["",""]
  oggi=shared['giornata']
  if m=="\U0001F5DEPartite Giornata":
    a=shared['seriea']
  elif m=="\U000023F1RisultatiLive":
    a[0] = sport.live(oggi, shared['contLive'])
    shared['contLive']+=1
  elif m=="\U0001F4CAClassifica":
    a[1]=sport.classifica()
    a[0]="Ecco la classifica di Serie A"
  elif m=='\U0001F51BPartite di Oggi':
    a[0]='Ecco le partite di oggi'
    a[1]=sport.partiteOggiDom(oggi, 'oggi')
    if a[1]=='':
      a[0]='Non ci sono parite oggi'
  elif m=="ScorsaGiorn":
    a = sport.partiteGior((oggi-1))
  elif m=='\U0001F51CPartite di Domani':
    a[0]='Ecco le partite di domani'
    a[1]=sport.partiteOggiDom(oggi, 'dom')
    if a[1]=='':
      a[0]='Non sono previste partite per domani'
  if a[0]!='': 
    bot.api.call("sendMessage", {"chat_id": chat.id, "text": a[0], "syntax": "HTML", "parse_mode": "HTML", "reply_markup": '{"keyboard": [[{"text": "/seriea"}, {"text": "/cambio"}], [{"text": "/meteo"}]], "one_time_keyboard": false, "resize_keyboard": true}'})
  if a[1]!='': 
    bot.api.call("sendMessage", {"chat_id": chat.id, "text": a[1], "parse_mode": "HTML", "reply_markup": '{"keyboard": [[{"text": "/seriea"}, {"text": "/cambio"}], [{"text": "/meteo"}]], "one_time_keyboard": false, "resize_keyboard": true}'})

#WEATHER COMMANDS
@bot.command('meteo')
def meteo_command(chat, message, args, shared):
  '''Visualizza il Meteo Orario o Giornaliero
    \nOpzioni:
    \nSe non specificato niente mostra il meteo orario per Modena
    \nSe viene specificato l'opzione 'd' viene visualizzato il meteo per i prossimi giorni
    \nSe viene specifica una citta' mostra il meteo (orario o giornaliero) per quella determinata citta', se non viene specificato niente la citta' di default e' Modena'''
  control(message)
  shared['comm'] = 'meteo'
  shared['citta'] = ''
  shared['tipoMet'] = ''
  bot.api.call("sendMessage", {"chat_id": chat.id, "text": '/meteo: seleziona una opzione', "parse_mode": "HTML", "reply_markup": '{"keyboard": [[{"text": "\U0001F4CDModena"}, {"text": "\U0001F30DAltra città"}]], "one_time_keyboard": false, "resize_keyboard": true}'})

def chiediTipoPrev(chat, message, shared):
  bot.api.call("sendMessage", {"chat_id": chat.id, "text": '/meteo: seleziona il tipo di previsione', "parse_mode": "HTML", "reply_markup": '{"keyboard": [[{"text": "\U0001F5DEGiornata"}, {"text": "\U0001F4C5Settimanale"}]], "one_time_keyboard": false, "resize_keyboard": true}'})
  shared['tipoMet'] = 'chiedo'

def inviaMeteo(citt, tip, chat, message, shared):
  if tip == 'day':
    if citt == 'modena':    
      mess = shared['meteo']
    else:
      cord=altriCom.trovaCord(citt)
      dat=altriCom.ottieniDati(str(cord[0]),str(cord[1]))
      mess=altriCom.mOrario(dat, 10)
  if tip == 'week':
    if citt == 'modena':
      dat=altriCom.ottieniDati(str(44.647128),str(10.9252269))
      mess=altriCom.mGiorni(dat)
    else:
      cord=altriCom.trovaCord(citt)
      dat=altriCom.ottieniDati(str(cord[0]),str(cord[1]))
      mess=altriCom.mGiorni(dat)
  bot.api.call("sendMessage", {"chat_id": chat.id, "text": mess, "parse_mode": "HTML", "reply_markup": '{"keyboard": [[{"text": "/seriea"}, {"text": "/cambio"}], [{"text": "/meteo"}]], "one_time_keyboard": false, "resize_keyboard": true}'})
  shared['comm'] = ''
  shared['citta'] = ''
  shared['tipoMet'] = ''

#CAMBIO COMMANDS
@bot.command("cambio")
def cambio_command(chat, message, args, shared):
    '''Cambia dollari in euro e viceversa
       \nCambia i Dollari in euro e Euro in dollari in base al simbolo di valuta messo dopo il numero. \nSe viene fornita la parola Tasso viene fornito il tasso di cambio €/$'''
    control(message)
    shared['comm'] = 'cambio'
    chat.send('/cambio: inserisci un valore seguito dal simbolo')

def effettuaCambio(chat, message, shared):
  cambio=altriCom.ottieniCambio()
  n=message.text
  if (n[-1:])=='€':
     n=float(n[:-1])
     ris=round(float(n/cambio), 3)
     ris=str(n)+"€ sono "+str(ris)+"$"
  elif (n[-1:])=='$':
     n=float(n[:-1])
     ris=round(float(n*cambio), 3)
     ris=str(n)+"$ sono "+str(ris)+"€"
  else:
     ris="Valuta inserita non corretta o non data\nInserici un valore con € o $ alla fine"
  bot.api.call("sendMessage", {"chat_id": chat.id, "text": ris, "parse_mode": "HTML", "reply_markup": '{"keyboard": [[{"text": "/seriea"}, {"text": "/cambio"}], [{"text": "/meteo"}]], "one_time_keyboard": false, "resize_keyboard": true}'})
  shared['comm'] = ''


#OTHER COMMANDS
@bot.command('start', hidden=True)
def start_command(chat, message):
  control(message)
  mess='Ciao, benevenuto su @infopzBot\nPer iniziare seleziona un comando tra quelli presenti\n\nPer avere informazioni più dettagliate su cosa fanno i singoli comandi puoi usare il comando /help\n\nNel caso incontrassi difficoltà o problemi non esitare a contattarmi! (@infopz)'
  bot.api.call("sendMessage", {"chat_id": chat.id, "text": mess, "parse_mode": "HTML", "reply_markup": '{"keyboard": [[{"text": "/seriea"}, {"text": "/cambio"}], [{"text": "/meteo"}]], "one_time_keyboard": false, "resize_keyboard": true}'})

@bot.command('ip', hidden=True)
def ip_command(chat, message, args):
   '''Visualizza l'ip pubblico di Infopz
    \nComando da usare per aggiornate il mio ip dinamico nel caso non lo facesse in automatico'''
   if controlInfopz(message)==True:
     data=urlopen("http://www.whatismypublicip.com/")
     page= str(data.read())
     page=page[5480:]
     page=page[:15]
     chat.send("L'indirizzo pubblico di infopz è "+page)
   else:
     chat.send('Solo @infopz puo eseguire questo comando')

@bot.command('inviaID', hidden=True)
def inviaID_command(chat, message, args):
  '''Invia il tuo chat ID a Infopz
    \nInvia a Infopz l'ID della tua chat con il Bot'''
  control(message)
  bot.chat(20403805).send('ID di @'+message.sender.username+':\n'+str(message.sender.id))

@bot.command('wake', hidden=True)
def wake_command(chat, message, args):
  if controlInfopz(message)==True:
    wol.send_magic_packet('d8:cb:8a:9d:ec:50')
    chat.send('Pacchetto inviato')
  else:
    chat.send('Solo @infopz puo eseguire questo comando')

@bot.command('me', hidden=True)
def provashames(chat, message):
  print(message.text)
  chat.send('Prova <b>Grassetto</b>', syntax='HTML')

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

#OTHER FUNCTIONS
def control(mess):
  a=mess.text
  st = ''
  if a[0]=='/':
    st = '  COMMAND  '
  else: st = '  MESSAGE  '
  b='@'+str(mess.sender.username)
  now = datetime.now()
  h=str(time.strftime('%H'))
  m=str(time.strftime('%M'))
  s=str(time.strftime('%S'))
  mes=h+':'+m+'.'+s+' -'+st+'- '+b+' '+a
  print(mes)

def controlInfopz(mess):
  perm=False
  if mess.sender.username=='infopz':
     perm=True
     a=mess.text
     b='@'+mess.sender.username
     now = datetime.now()
     h=str(time.strftime('%H'))
     m=str(time.strftime('%M'))
     s=str(time.strftime('%S'))
     mes=str(h)+':'+str(m)+'.'+str(s)+' -  COMMAND  - '+b+' '+a
     print(mes)
  else:
     a=mess.text
     b='@'+mess.sender.username
     now = datetime.now()
     h=str(time.strftime('%H'))
     m=str(time.strftime('%M'))
     s=str(time.strftime('%S'))
     mes=str(h)+':'+str(m)+'.'+str(s)+' -   DENIED  - '+b+' '+a
     print(mes)
  return perm

def fmeteoDom(num, nome):
   cord=altriCom.trovaCord('Modena')
   dat=altriCom.ottieniDati(str(cord[0]),str(cord[1]))
   mess=altriCom.mOrario(dat, 12)
   bot.chat(num).send('Ciao '+nome+'!\nEcco le previsioni meteo per la giornata di domani')
   bot.chat(num).send(mess)


#BOT TIMERS
@bot.timer(300)
def aggMeteo(bot, shared):
  dat=altriCom.ottieniDati(str(44.647128),str(10.9252269))
  mess=altriCom.mOrario(dat, 10)
  shared['meteo'] = mess


@bot.timer(3600)
def resetLive(bot, shared):
  now = datetime.now()
  h=now.hour
  if h==1:
    shared['contLive'] = 0

@bot.timer(7200)
def aggSeriea(bot, shared):
  shared['giornata'] = sport.trovaGiornata()
  shared['seriea'] = sport.partiteGior(shared['giornata'])


@bot.timer(60)
def meteoDomani(bot):
   now = datetime.now()
   h=now.hour
   m=now.minute
   if h==21 and m==00: 
     buong = open('listMeteo', 'r')
     for lines in buong.readlines():
        l = lines.split(' ', 2)
        fmeteoDom(l[0], l[1][:-1])
     buong.close()


#USEFUL-BOT FUNCTIONS
@bot.prepare_memory
def prepare_memory(shared):
  dat=altriCom.ottieniDati(str(44.647128),str(10.9252269))
  mess=altriCom.mOrario(dat, 10)
  oggi=sport.trovaGiornata()
  ser = sport.partiteGior(oggi)
  shared['meteo'] = mess
  shared['giornata'] = oggi
  shared['seriea'] = ser
  shared['tipoMet'] = ''
  shared['citta'] = ''
  shared['contLive'] = 0

@bot.process_message
def message_received(chat, message, shared):
  control(message)
  if shared['comm'] == 'seriea':
    serieaOutput(message.text, chat, shared)

  if shared['comm'] == 'cambio':
    effettuaCambio(chat, message, shared)

  if shared['tipoMet'] == 'chiedo':
    if message.text == '\U0001F5DEGiornata':
      shared['tipoMet'] = 'day'
    elif message.text == '\U0001F4C5Settimanale':
      shared['tipoMet'] = 'week'
    inviaMeteo(shared['citta'], shared['tipoMet'], chat, message, shared)
    shared['comm'] = ''
  
  if shared['citta'] == 'altra':
    shared['citta'] = message.text

  if shared['comm'] == 'meteo':
    if shared['citta'] == '':
      if message.text == '\U0001F30DAltra città':
        shared['citta'] = 'altra'
        chat.send('/meteo: dimmi di quale cità vuoi avere il meteo')
      elif message.text == '\U0001F4CDModena':
        shared['citta'] = 'modena'
        chiediTipoPrev(chat, message, shared)
    else:
      if shared['tipoMet'] != 'chiedo':
        chiediTipoPrev(chat, message, shared)

if __name__ == "__main__":
    bot.run()
