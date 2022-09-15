import time
from config import Binance
import telebot
import logging
from binance.um_futures import UMFutures as Client
from binance.error import ClientError
from datetime import datetime
from config import API_SECRET, API_KEY, token


class BinanceBot:
    def __init__(self, API_KEY, API_SECRET):
        self.input_coin = input('Введите монету:')
        self.input_deposit = input('Введите депозит:')
        self.bot = Binance(API_KEY, API_SECRET)
        self.api_key = API_KEY
        self.api_secret = API_SECRET

    class TeleBot:
        def __init__(self):
            self.bot = telebot.TeleBot(token)


        def message(self, id: str, text: str):
            self.bot.send_message(id, text)




    def position_short(self):
        client = Client(self.api_key, self.api_secret, base_url="https://fapi.binance.com")
        params = [
            {"symbol": self.input_coin, "side": "SELL", "type": "MARKET", "quantity": self.input_deposit, 'recWindow': '5000'}]
        try:
            response = client.new_batch_order(params)
            logging.info(response)
        except ClientError as error:
            logging.error(
                f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
                )



    def stop_loss(self):
        ticker = self.bot.ticker24hr(
            symbol=self.input_coin
        )
        b = ticker['lastPrice']
        sl = float(b) * 0.3 / 100 + float(b)  # цена открытия
        client = Client(self.api_key, self.api_secret, base_url="https://fapi.binance.com")
        try:
            response = client.new_order(symbol=self.input_coin, type='STOP_MARKET', side='BUY',
                                        quantity=self.input_deposit,
                                        stopPrice=str(round(sl, 4)), closePosition=True)
            logging.info(response)
        except ClientError as error:
            logging.error(
                f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_message}"
            )


    def take_profit(self):
        ticker = self.bot.ticker24hr(
            symbol=self.input_coin
        )
        b = ticker['lastPrice']
        tk = -float(b) * 1 / 100 + float(b)
        client = Client(self.api_key, self.api_secret, base_url="https://fapi.binance.com")
        try:
            response = client.new_order(symbol=self.input_coin, type='TAKE_PROFIT_MARKET', side='BUY',
                                        quantity=self.input_deposit, stopPrice=str(round(tk, 4)),
                                        closePosition=True)
            logging.info(response)
        except ClientError as error:
            logging.error(
                f"Found error. status: {error.status_code}, error code: {error.error_code}, error message: {error.error_code}"

            )


    def trade(self):
        while True:
            print('Проверяем...')
            current_datetime = datetime.now()
            time_zone = current_datetime.minute  # получаем текущее время
            time1 = time_zone + 1  # получаем нужное время
            if time1 == 59:
                time.sleep(120)
                time1 = 2
            while time_zone != time1:
                current_datetime = datetime.now()
                time_zone = current_datetime.minute
            kln = self.bot.klines(
                symbol=self.input_coin,
                interval='1m',
                limit='1'
            )
            for i in kln:
                coin = float(i[1])  # цена открытия
                cl = float(i[4])  # цена закрытия
                spoof = float(200000) / cl
                if cl > coin:
                    print(f'[+] Цена Открытия:, {coin}, Цена закрытия: {cl}, {self.input_coin}')
                    count_asks = 0
                    current_datetime = datetime.now()
                    time_second = current_datetime.second
                    while time_second != 40:
                        current_datetime = datetime.now()
                        time_second = current_datetime.second
                        b = self.bot.tickerBookTicker(
                            symbol=self.input_coin
                        )
                        if float(b['askQty']) >= spoof:
                            count_asks += 1
                    if count_asks >= 1:
                        self.position_short()
                        self.stop_loss()
                        self.take_profit()
                        self.TeleBot().message('847449845', 'Зашла в сделку: Монета - GMTUSDT')
                        print('[+]', 'Второе условие выполнилось')
                        time.sleep(300)

                    else:
                        print('[-]', 'Второе условие не выполнилось')


def main():
    obj = BinanceBot(API_KEY, API_SECRET)
    obj.trade()


if __name__ == '__main__':
    main()

