import time
from config import Binance
import telebot
import logging
from binance.um_futures import UMFutures as Client
from binance.error import ClientError
from datetime import datetime
from config import API_SECRET, API_KEY, token
from binance.lib.utils import config_logging
from binance.error import ClientError



bot = telebot.TeleBot('5663149478:AAHwr72sS5ha52g9Lo9pytsnwpvB7ohPf14')
ID_slava = '847449845'

def message_slava(text: str):
    bot.send_message(ID_slava, text)




def loss6_massage_success_slava():
    message_slava('Вошла в сделку, монета: ZEN')




# loss6_massage_success_slava()





class TeleBot:
    def __init__(self):
        self.bot = telebot.TeleBot(token)

    def message(self, id: str, text: str):
        self.bot.send_message(id, text)


obj = TeleBot().message('847449845', 'Salam')