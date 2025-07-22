import time
import yfinance as yf
import telebot
import datetime

# Твой Telegram токен
TOKEN = '8094752756:AAFUdZn4XFlHiZOtV-TXzMOhYFlXKCFVoEs'
bot = telebot.TeleBot(TOKEN)

# Твой Telegram ID
CHAT_ID = '5556108366'

# Валютные пары
symbols = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "USD/CHF": "CHF=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD": "NZDUSD=X",
    "USD/CAD": "CAD=X"
}

def analyze(symbol):
    try:
        data = yf.download(tickers=symbol, interval="1m", period="5m")
        if data.empty or len(data) < 2:
            return None, None

        last = data.iloc[-1]
        close_price = float(last['Close'])
        open_price = float(last['Open'])

        signal = ""
        confidence = 0

        if close_price > open_price:
            signal = "📈 Покупка"
            confidence = round((close_price - open_price) / open_price * 100, 2)
        elif close_price < open_price:
            signal = "📉 Продажа"
            confidence = round((open_price - close_price) / open_price * 100, 2)
        else:
            signal = "⏸ Нет сигнала"
            confidence = 0

        return signal, confidence

    except Exception as e:
        return f"❌ Ошибка {symbol}: {str(e)}", None

def run_bot():
    while True:
        now = datetime.datetime.now()
        if 6 <= now.hour < 22:  # Проверка по времени (Астана)
            for name, symbol in symbols.items():
                signal, confidence = analyze(symbol)
                if signal is None:
                    bot.send_message(CHAT_ID, f"❌ Ошибка {name}")
                elif "Ошибка" in signal:
                    bot.send_message(CHAT_ID, signal)
                elif confidence >= 0.1:
                    bot.send_message(CHAT_ID, f"🔔 {name}\nСигнал: {signal}\nУверенность: {confidence}%")
                else:
                    bot.send_message(CHAT_ID, f"🔕 {name}: Нет сильного сигнала")
        else:
            bot.send_message(CHAT_ID, "⏰ Рынок вне времени торговли. Следующее обновление через 30 секунд.")
        
        time.sleep(30)  # Интервал между проверками

if __name__ == "__main__":
    run_bot()
