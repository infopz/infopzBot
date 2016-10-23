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

@bot.prepare_memory
def prepare_memory(shared):
  dat=altriCom.ottieniDati(str(44.647128),str(10.9252269))
  mess=altriCom.mOrario(dat, 10)
  oggi=sport.trovaGiornata()
  ser = sport.partiteGior(oggi)
  shared['meteo'] = mess
  shared['giornata'] = oggi
  shared['seriea'] = ser

@bot.process_message
def message_received(chat, message, shared):
  print(shared['comm'])
  if shared['comm'] == 'seriea':
    serieaOutput(message.text, chat, shared)

  if shared['tipoMet'] == 'chiedo':
    if message.text == 'Meteo della Giornata':
      shared['tipoMet'] = 'day'
    elif message.text == 'Meteo Settimanale':
      shared['tipoMet'] = 'week'
    inviaMeteo(shared['citta'], shared['tipoMet'], chat, message, shared)
    shared['comm'] = ''

  if shared['comm'] == 'meteo':
    if shared['citta'] == '':
      if message.text == 'Altra città':
        chat.send('/metoe: dimmi di quale cità vuoi avere il meteo')
        shared['citta'] = 'altra'
      elif message.text == 'Modena':
        shared['citta'] = 'modena'
        chiediTipoPrev(chat, message, shared)
    else:
      if shared['tipoMet'] != 'chiedo':
        chiediTipoPrev(chat, message, shared)
  if shared['citta'] == 'altra':
    shared['citta'] = message.text

  

@bot.command("hello", hidden=True)
def hello_command(chat, message, args):
    '''Ciaone!
       \nTi saluta con un bel ciao'''
    control(message)
    chat.send("Hello World")

@bot.command("cambio")
def cambio_command(chat, message, args):
    '''Cambia dollari in euro e viceversa
       \nCambia i Dollari in euro e Euro in dollari in base al simbolo di valuta messo dopo il numero. \nSe viene fornita la parola Tasso viene fornito il tasso di cambio €/$'''
    control(message)
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
    print(shared['comm'])
    bot.api.call("sendMessage", {"chat_id": chat.id, "text": '/seriea: seleziona una opzione', "parse_mode": "HTML", "reply_markup": '{"keyboard": [[{"text": "Partite della Giornata"}, {"text": "Partite di Oggi"}], [{"text": "Partite di Domani"}, {"text": "Classifica"}]], "one_time_keyboard": true, "resize_keyboard": true}'})


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
  bot.api.call("sendMessage", {"chat_id": chat.id, "text": '/meteo: seleziona una opzione', "parse_mode": "HTML", "reply_markup": '{"keyboard": [[{"text": "Modena"}, {"text": "Altra città"}]], "one_time_keyboard": true, "resize_keyboard": true}'})
  '''if mes[0]=='':
    mess = shared['meteo']
  elif mes[0]=='d':
    if mes[1]=='':
      dat=altriCom.ottieniDati(str(44.647128),str(10.9252269))
      mess=altriCom.mGiorni(dat)
    else:
      cord=altriCom.trovaCord(mes[1])
      dat=altriCom.ottieniDati(str(cord[0]),str(cord[1]))
      mess=altriCom.mGiorni(dat)
  else:
    cord=altriCom.trovaCord(mes[0])
    dat=altriCom.ottieniDati(str(cord[0]),str(cord[1]))
    mess=altriCom.mOrario(dat, 10)
  chat.send(mess)'''
   
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

@bot.command('me')
def provashames(chat, message, args, shared):
  bot.api.call("sendMessage", {"chat_id": chat.id, "text": 'Scegli', "parse_mode": "HTML", "reply_markup": {'{"force_reply": true, "selective": true}', '{"keyboard": [[{"text": "Return back", "text}]], "one_time_keyboard": true, "resize_keyboard": true}'}})


@bot.timer(300)
def aggMeteo(bot, shared):
  dat=altriCom.ottieniDati(str(44.647128),str(10.9252269))
  mess=altriCom.mOrario(dat, 10)
  shared['meteo'] = mess

@bot.timer(43200)
def aggSeriea(bot, shared):
  shared['giornata'] = sport.trovaGiornata()
  shared['seriea'] = sport.partiteGior(shared['giornata'])


@bot.timer(60)
def meteoDomani(bot):
   now = datetime.now()
   h=now.hour
   m=now.minute
   if h==20 and m==00: 
     buong = open('listMeteo', 'r')
     for lines in buong.readlines():
        l = lines.split(' ', 2)
        fmeteoDom(l[0], l[1][:-1])
     buong.close()

def control(mess):
  a=mess.text
  b='@'+str(mess.sender.username)
  now = datetime.now()
  h=str(time.strftime('%H'))
  m=str(time.strftime('%M'))
  s=str(time.strftime('%S'))
  mes=h+':'+m+'.'+s+' -  COMMAND  - '+b+' '+a
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

def serieaOutput(m, chat, shared):
  a=["",""]
  oggi=shared['giornata']
  if m=="Partite della Giornata":
    a=shared['seriea']
  elif m=="Classifica":
    a[1]=sport.classifica()
    a[0]="Ecco la classifica di Serie A"
  elif m=='Partite di Oggi':
    a[0]='Ecco le partite di oggi'
    a[1]=sport.partiteOggi(oggi)
    if a[1]=='':
      a[0]='Non ci sono parite oggi'
  elif m=='Partite di Domani':
    a[0]='Ecco le partite di domani'
    a[1]=sport.partiteDomani(oggi)
    if a[1]=='':
      a[0]='Non sono previste partite per domani'
  if a[0]!='': chat.send(a[0])
  if a[1]!='': chat.send(a[1])

def chiediTipoPrev(chat, message, shared):
  bot.api.call("sendMessage", {"chat_id": chat.id, "text": '/meteo: seleziona il tipo di previsione', "parse_mode": "HTML", "reply_markup": '{"keyboard": [[{"text": "Meteo della Giornata"}, {"text": "Meteo Settimanale"}]], "one_time_keyboard": true, "resize_keyboard": true}'})
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
  chat.send(mess)


if __name__ == "__main__":
    bot.run()
