import time
import uuid
import logging

import telebot
from multiprocessing import Process

logging.basicConfig(filename="sample.log", level=logging.INFO)

bot = telebot.TeleBot('1428953537:AAGXZr4wTMQAUCvjZnyo1-nbEf5QDsT3j3w')

test_message = 'test {}'.format(uuid.uuid4())

test_chat_id = 501631688


def send_message():
    while True:
        bot.send_message(test_chat_id, test_message)
        time.sleep(5)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == test_message:
        logging.debug('OK', message.text)


if __name__ == '__main__':
    p1 = Process(target=send_message, daemon=True)
    p1.start()
    bot.polling()
