import requests
import time

import apiKey


def trovaCord(cit):
  keyGM = apiKey.apiGoogleMaps()
  risG = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+str(cit)+'&key='+keyGM)
  risG = risG.json()
  lat=risG['results'][0]['geometry']['location']['lat']
  lng=risG['results'][0]['geometry']['location']['lng']
  cord=[lat, lng]
  return cord
  

def ottieniDati(lat, lon):
  keyDS = apiKey.apiDarkSky()
  risp = requests.get('https://api.darksky.net/forecast/'+keyDS+'/'+lat+','+lon+'?units=ca&lang=it')
  risp = risp.json()
  return risp

def convertiGiorno(giorno):
   giCor=''
   if giorno=='Mon': giCor='Lu'
   elif giorno=='Tue': giCor='Ma'
   elif giorno=='Wed': giCor='Me'
   elif giorno=='Thu': giCor='Gio'
   elif giorno=='Fri': giCor='Ve'
   elif giorno=='Sat': giCor='Sa'
   elif giorno=='Sun': giCor='Do'
   return giCor


def mOrario(risp):
  a=0
  dati=''
  e=''
  dati=risp['hourly']['summary']+'\n'
  for i in risp['hourly']['data']:
    if a==8: break
    o=int(time.strftime('%H', time.gmtime(i['time'])))
    if (o+2)>=24: o=o-24
    o=str(o+2)
    p=i['summary']
    t=str(round(i['temperature'], 1))
    if p=='Sereno': e='\U00002600'
    elif p=='Nubi Sparse': e='\U0001F325'
    elif p=='Poco Nuvoloso': e='\U0001F324'
    elif p=='Pioggia Molto Leggera': e='\U0001F326'
    #elif p=='Nuvoloso': e=''
    elif p=='Pioggia Leggera': e='\U0001F326'
    #elif p=='Pioggia': 
    if int(o)%2==0: 
      dati+=o+': '+e+' '+t+'° '+p+'\n'
      a+=1
    e=''
  return dati

def mGiorni(risp):
  b=0
  dati=''
  e=''
  dati=risp['daily']['summary']+'\n\n'
  for i in risp['daily']['data']:
    if b==8: break
    orGius=i['time']+86400
    num=time.strftime('%d', time.gmtime(orGius))
    nom=time.strftime('%a', time.gmtime(orGius))
    gC=convertiGiorno(nom)
    p=i['summary']
    ed=p.split(' ', 3)
    if ed[0]=='Pioggia':
      if ed[1]!='leggera':
          e='\U0001F327'
      else:
          e='\U0001F326'
    elif ed[0]=='Nubi': e='\U0001F325'
    elif ed[0]=='Sereno': e='\U00002600'
    elif ed[1]=='nuvoloso': e='\U0001F324'
    tm=str(round(i['temperatureMin'], 1))
    tM=str(round(i['temperatureMax'], 1))
    dati+=gC+' '+num+': '+e+' '+tm+'°-'+tM+'° '+p+'\n'
    e=''
    b+=1
  return dati

  
