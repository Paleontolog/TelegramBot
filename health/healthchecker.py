import time
import uuid
import logging
import os

import telebot
from multiprocessing import Process

logging.basicConfig(filename="sample.log", level=logging.INFO)

bot = telebot.TeleBot(os.environ['API_KEY'])
target = telebot.TeleBot(os.environ['API_KEY_TARGET'])

test_message = 'test {}'.format(uuid.uuid4())

test_chat_id = target


def send_message():
    while True:
        bot.send_message(test_chat_id, test_message)
        time.sleep(5)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == test_message:
        logging.debug('OK', message.text)
    else:
        logging.debug('OTHER', message.text)


if __name__ == '__main__':
    p1 = Process(target=send_message, daemon=True)
    p1.start()
    bot.polling()
