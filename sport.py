import requests
import time
from datetime import datetime
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
    di = i['start_date']
    Y=int(di[:4])
    m=int(di[5:7])
    d=int(di[8:10])
    df = i['end_date']
    Y2=int(df[:4])
    m2=int(df[5:7])
    d2=int(df[8:10])
    dig=[Y, m, d]
    dfg=[Y2, m2, d2]
    tf=(datetime(dig[0], dig[1], dig[2]) <= datetime(dt[0], dt[1], dt[2])) and (datetime(dfg[0], dfg[1], dfg[2]) >= datetime(dt[0], dt[1], dt[2]))
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
  ri = requests.get("https://sportsop-soccer-sports-open-data-v1.p.mashape.com/v1/leagues/serie-a/seasons/16-17/rounds/"+giorS+"/matches", headers={"X-Mashape-Key":keyMash, "Accept": "application/json"})
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









