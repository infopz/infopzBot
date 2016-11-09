import requests
from datetime import datetime, timedelta
import apiKey
import json

keyMash = apiKey.apiMashape()


def trovaGiornata():
  ri = requests.get("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/serie-a/seasons/16-17/rounds", headers={"X-Mashape-Key": keyMash, "Accept": "application/json"})
  ri = ri.json()
  giorn=1
  dc = datetime.now()
  dc = datetime(dc.year, dc.month, dc.day)
  for i in ri['data']['rounds']:
    df = i['end_date']
    df = datetime(int(df[:4]), int(df[5:7]), int(df[8:10]))
    if dc<=df:
      break
    else:
      giorn+=1
  return giorn

def partiteGior(gior):
  giorS = 'giornata-'+str(gior)
  ri = requests.get(("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/serie-a/seasons/16-17/rounds/"+giorS+"/matches"), headers={"X-Mashape-Key": keyMash, "Accept": "application/json"})
  ri = ri.json()
  d=''
  for i in ri['data']['matches']:
    squad1=i['home']['team']
    squad2=i['away']['team']
    risultato=i['match_result']
    r=squad1+'-'+squad2+' '+risultato+'\n'
    d+=r
  mes = 'Ecco le partite della '+str(gior)+'a giornata'
  ret=[mes, d]
  return ret

def partiteOggiDom(gior, st):
  giorS = 'giornata-'+str(gior)
  ri = requests.get(("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/serie-a/seasons/16-17/rounds/"+giorS), headers={"X-Mashape-Key": keyMash, "Accept": "application/json"})
  ri = ri.json()
  now = datetime.now()
  if st == 'oggi':
   dt = datetime(now.year, now.month, now.day)
  else:
   dt = datetime(now.year, now.month, now.day)+timedelta(days=1)
  el = ''
  for i in ri['data']['rounds'][0]['matches']:
    dp = i['date_match']
    dg = datetime(int(dp[:4]), int(dp[5:7]), int(dp[8:10]))
    if dg == dt:
      squad1=i['home_team']
      squad2=i['away_team']
      ora=i['date_match'][11:16]
      part = (ora+' '+squad1+'-'+squad2+' '+'\n')
      el = el+part
  return el

def classifica():
  ri = requests.get("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/serie-a/seasons/16-17/standings", headers={"X-Mashape-Key":keyMash, "Accept": "application/json"})
  ri = ri.json()
  cl=''
  for i in ri['data']['standings']:
    pos=str(i['position'])
    point=str(i['overall']['points'])
    team=(i['team'])
    v=str(i['overall']['wins'])
    p=str(i['overall']['draws'])
    per=str(i['overall']['losts'])
    lin=(pos+'. '+team+' ('+point+')(V:'+v+',P:'+per+',Pa:'+p+')\n')
    cl=cl+lin
  return cl

def live(giorn, num):
  cont = num
  mes = 'Ecco i risultati live delle partite: '
  if cont < 20:
    ri = requests.get("https://heisenbug-seriea-essentials-v1.p.mashape.com/api/live/seriea?gamenumber="+str(giorn), headers={"X-Mashape-Key":keyMash, "Accept": "application/json"})
    d = ri.json()
    for i in d['matches']:
      gt1=''; gt2=''; st1=''; st2=''
      if 'teamScore' in i['team1']:
        st1 = str(i['team1']['teamScore'])
        if 'goals' in i['team1']:
          for g in i['team1']['goals']:
            if gt1 != '':
              gt1+='\n'+g['minute']+'  '+g['player']
            else:
              gt1=g['minute']+'  '+g['player']
      if 'teamScore' in i['team2']:
        st2 = str(i['team2']['teamScore'])
        if 'goals' in i['team2']:
          for g in i['team2']['goals']:
            if gt2 != '':
              gt2+='\n'+g['minute']+'  '+g['player']
            else:
              gt2=g['minute']+'  '+g['player']
      if st1 == '':
        continue
      else:
        mes+='\n<b>'+i['team1']['teamName']+' '+st1+' - '+st2+' '+i['team2']['teamName']+'</b>'
        if gt1 != '':mes+='\n'+gt1
        if gt2 != '':mes+='\n'+gt2
    if mes == 'Ecco i risultati live delle partite: ':
      mes = 'Le partite della prossima giornata non sono ancora iniziate'
  else:
    mes='Numero massimo richieste gionaliere raggiunto\nContatta @infopz per maggiori infomazioni'
  return mes


