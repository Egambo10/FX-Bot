import fxcmpy
import pandas as pd 
import json
import requests
from socketIO_client import SocketIO

TRADING_API_URL = 'https://api-demo.fxcm.com:433'
WEBSOCKET_PORT = 433
ACCESS_TOKEN = 'dfb438a1e3d59140aa73314990fb34b94bc89513'

def on_connect():
  print('Websocket Connected:'+ socketIO.engineIO_session.id)

def on_close():
  print('Websocket Closed.')

socketIO = SocketIO(TRADING_API_URL,WEBSOCKET_PORT, params={'access_token': ACCESS_TOKEN})

socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_close)

bearer_access_token = 'Beared' + socketIO._engineIO_session.id + ACCESS_TOKEN

print(bearer_access_token)