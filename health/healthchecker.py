import time
import uuid
import logging
import os

import telebot
from multiprocessing import Process

logging.basicConfig(filename="logs/sample.log", level=logging.INFO)

bot = telebot.TeleBot(os.environ['API_KEY'])

test_message = 'test message'
logging.info(test_message)

test_chat_id = os.environ['CHAT_ID']


def send_message():
    while True:
        bot.send_message(test_chat_id, test_message)
        time.sleep(5)


@bot.channel_post_handler(content_types=['text'])
def check_text(message):
    print(message.text.lower())
    print(test_message)
    print(message.text.lower() == test_message)
    if message.text.lower() == test_message:
        logging.info('OK ' + message.text)
    else:
        logging.info('OTHER ' + message.text)


if __name__ == '__main__':
    p1 = Process(target=send_message, daemon=True)
    p1.start()
    bot.polling()
