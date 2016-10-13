import requests
import time
from datetime import datetime, timedelta
import apiKey

keyMash = apiKey.apiMashape()

def dataOra():
  current_time= time.localtime()
  Y=int(time.strftime('%Y'))
  m=int(time.strftime('%m'))
  d=int(time.strftime('%d'))
  H=int(time.strftime('%H'))
  M=int(time.strftime('%M'))
  dt=[Y, m, d, H, M]
  return dt

def trovaGiornata():
  dt=dataOra()
  giorn=1 
  ri = requests.get("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/serie-a/seasons/16-17/rounds", headers={"X-Mashape-Key":keyMash, "Accept": "application/json"})
  ri = ri.json()
  for i in ri['data']['rounds']:
    if giorn == 1:
      a='2016-08-20T18:00:00+0200'
      Y=int(a[:4])
      m=int(a[5:7])
      d=int(a[8:10])
      di =  datetime(Y, m, d)
    else:
      di = a + timedelta(days=1)
    df = i['end_date']
    Y=int(df[:4])
    m=int(df[5:7])
    d=int(df[8:10])
    df =  datetime(Y, m, d)
    dfe = df + timedelta(days=1)
    a = dfe
    do = datetime(dt[0], dt[1], dt[2])
    tf = (do >= di) and (do <= dfe)
    if tf==False:
      giorn+=1
    else:
      break
  return giorn

def stampaPart(ri):
  d=''
  for i in ri['data']['matches']:
    squad1=i['home']['team']
    squad2=i['away']['team']
    risultato=i['match_result']
    r=squad1+'-'+squad2+' '+risultato+'\n'
    d+=r
  return d

def partiteGior(gior):
  giorS = 'giornata-'+str(gior)
  ri = requests.get(("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/serie-a/seasons/16-17/rounds/"+giorS+"/matches"), headers={"X-Mashape-Key":keyMash, "Accept": "application/json"})
  ri = ri.json()
  mes='Ecco le partite della '+str(gior)+'a giornata'
  par=stampaPart(ri)
  ret=[mes, par]
  return ret

def classifica():
  ri = requests.get("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/serie-a/seasons/16-17/standings", headers={"X-Mashape-Key":keyMash, "Accept": "application/json"})
  ri = ri.json()
  cl=''
  for i in ri['data']['standings']:
    pos=str(i['position'])
    point=str(i['overall']['points'])
    team=str(i['team'])
    v=str(i['overall']['wins'])
    p=str(i['overall']['draws'])
    per=str(i['overall']['losts'])
    lin=(pos+'. '+team+' ('+point+')('+v+','+p+','+per+')\n')
    cl=cl+lin
  return(cl)


def partiteOggi(gior):
  giorS = 'giornata-'+str(gior)
  ri = requests.get(("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/serie-a/seasons/16-17/rounds/"+giorS), headers={"X-Mashape-Key":keyMash, "Accept": "application/json"})
  ri = ri.json()
  dtO = dataOra()
  el=''
  for i in ri['data']['rounds'][0]['matches']:
    dp = i['date_match']
    Y=int(dp[:4])
    m=int(dp[5:7])
    d=int(dp[8:10])
    pO = (datetime(dtO[0], dtO[1], dtO[2])) == (datetime(Y, m, d))
    if pO == True:
      squad1=i['home_team']
      squad2=i['away_team']
      ora=i['date_match'][11:16]
      risult=i['match_result']
      part = (ora+' '+squad1+'-'+squad2+' '+risult+'\n')
      el = el+part
  return(el)


def partiteDomani(gior):
  giorS = 'giornata-'+str(gior)
  ri = requests.get(("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/serie-a/seasons/16-17/rounds/"+giorS), headers={"X-Mashape-Key":keyMash, "Accept": "application/json"})
  ri = ri.json()
  dtO = dataOra()
  el=''
  for i in ri['data']['rounds'][0]['matches']:
    dp = i['date_match']
    Y=int(dp[:4])
    m=int(dp[5:7])
    d=int(dp[8:10])
    tomorrow = datetime(dtO[0], dtO[1], dtO[2])+timedelta(days=1)
    pO = tomorrow == datetime(Y, m, d)
    if pO == True:
      squad1=i['home_team']
      squad2=i['away_team']
      ora=i['date_match'][11:16]
      part = (ora+' '+squad1+'-'+squad2+' '+'\n')
      el = el+part
  return(el)




