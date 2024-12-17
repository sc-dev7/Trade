#!/usr/bin/python3

__version__ = "1.6"

import sys

MIN_TRADE_AMOUNT = 0.001

class Bot:
    def __init__(self):
        self.botState = BotState()

    def run(self):
        while True:
            reading = input().strip()
            if not reading:
                continue
            self.parse(reading)

    def parse(self, info: str):
        parts = info.split(" ", 2)
        if parts[0] == "settings":
            self.botState.update_settings(parts[1], parts[2])
        elif parts[0] == "update":
            if parts[1] == "game":
                game_parts = parts[2].split(" ", 1)
                self.botState.update_game(game_parts[0], game_parts[1])
        elif parts[0] == "action":
            self.make_decision()

    def make_decision(self):
        dollars = self.botState.stacks.get("USDT", 0)
        btc = self.botState.stacks.get("BTC", 0)
        chart = self.botState.charts.get("USDT_BTC", Chart())
        
        if len(chart.closes) < 20:
            print("no_moves", flush=True)
            return

        psar = self.calculate_psar(chart.highs, chart.lows, chart.closes)
        current_price = chart.closes[-1]

        if psar is None:
            print("no_moves", flush=True)
            return
        print(f'My stacks: USDT = {dollars}, BTC = {btc}', file=sys.stderr)
        print(f'Current price = {current_price}, PSAR = {psar}', file=sys.stderr)
        if current_price > psar and dollars >= 100:
            affordable = dollars / current_price
            if 0.5 * affordable > MIN_TRADE_AMOUNT:
                print(f'buy USDT_BTC {0.5 * affordable}', flush=True)
            else:
                print("no_moves", flush=True)
        elif current_price < psar and btc > 0:
            if 0.5 * btc > MIN_TRADE_AMOUNT:
                print(f'sell USDT_BTC {0.5 * btc}', flush=True)
            else:
                print("no_moves", flush=True)
        else:
            print("no_moves", flush=True)

    def calculate_psar(self, highs, lows, closes, af=0.02, af_step=0.02, af_max=0.2):
        psar = [closes[0]]
        ep = highs[0]
        bull = True
        af = af

        for i in range(1, len(closes)):
            if bull:
                psar.append(psar[-1] + af * (ep - psar[-1]))
                if highs[i] > ep:
                    ep = highs[i]
                    af = min(af + af_step, af_max)
                if closes[i] < psar[-1]:
                    bull = False
                    psar[-1] = ep
                    ep = lows[i]
                    af = af_step
            else:
                psar.append(psar[-1] + af * (ep - psar[-1]))
                if lows[i] < ep:
                    ep = lows[i]
                    af = min(af + af_step, af_max)
                if closes[i] > psar[-1]:
                    bull = True
                    psar[-1] = ep
                    ep = highs[i]
                    af = af_step

        return psar[-1] if len(psar) > 0 else None

class Candle:
    def __init__(self, format, intel):
        tmp = intel.split(",")
        self.pair = tmp[0]
        self.date = int(tmp[1])
        self.high = float(tmp[2])
        self.low = float(tmp[3])
        self.open = float(tmp[4])
        self.close = float(tmp[5])
        self.volume = float(tmp[6])

    def __repr__(self):
        return f'{self.pair} {self.date} {self.close} {self.volume}'

class Chart:
    def __init__(self):
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.indicators = {}

    def add_candle(self, candle: Candle):
        self.dates.append(candle.date)
        self.opens.append(candle.open)
        self.highs.append(candle.high)
        self.lows.append(candle.low)
        self.closes.append(candle.close)
        self.volumes.append(candle.volume)

class BotState:
    def __init__(self):
        self.timeBank = 0
        self.maxTimeBank = 0
        self.timePerMove = 1
        self.candleInterval = 1
        self.candleFormat = []
        self.candlesTotal = 0
        self.candlesGiven = 0
        self.initialStack = 0
        self.transactionFee = 0.1
        self.date = 0
        self.stacks = dict()
        self.charts = dict()

    def update_chart(self, pair: str, new_candle_str: str):
        if pair not in self.charts:
            self.charts[pair] = Chart()
        new_candle_obj = Candle(self.candleFormat, new_candle_str)
        self.charts[pair].add_candle(new_candle_obj)

    def update_stack(self, key: str, value: float):
        self.stacks[key] = value

    def update_settings(self, key: str, value: str):
        if key == "timebank":
            self.maxTimeBank = int(value)
            self.timeBank = int(value)
        elif key == "time_per_move":
            self.timePerMove = int(value)
        elif key == "candle_interval":
            self.candleInterval = int(value)
        elif key == "candle_format":
            self.candleFormat = value.split(",")
        elif key == "candles_total":
            self.candlesTotal = int(value)
        elif key == "candles_given":
            self.candlesGiven = int(value)
        elif key == "initial_stack":
            self.initialStack = int(value)
        elif key == "transaction_fee_percent":
            self.transactionFee = float(value)

    def update_game(self, key: str, value: str):
        if key == "next_candles":
            new_candles = value.split(";")
            self.date = int(new_candles[0].split(",")[1])
            for candle_str in new_candles:
                candle_infos = candle_str.strip().split(",")
                self.update_chart(candle_infos[0], candle_str)
        elif key == "stacks":
            new_stacks = value.split(",")
            for stack_str in new_stacks:
                stack_infos = stack_str.strip().split(":")
                self.update_stack(stack_infos[0], float(stack_infos[1]))

if __name__ == "__main__":
    mybot = Bot()
    mybot.run()
