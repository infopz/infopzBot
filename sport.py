import requests
from datetime import datetime, timedelta
import apiKey

keyMash = apiKey.apiMashape()


def trovaGiornata():
  ri = requests.get("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/serie-a/seasons/16-17/rounds", headers={"X-Mashape-Key": keyMash, "Accept": "application/json"})
  ri = ri.json()
  giorn=1
  dc = datetime.now()
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
   print(dt)
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

