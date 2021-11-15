from pyrogram import Client
from config import session_name
from TeleBot.bot import bot_do_job


def run():

    try:
        print('running...')
        print('use ctrl+C to stop')
        client_obj = Client(session_name)
        bot_do_job(client_obj)

    except KeyboardInterrupt:
        print('Stopped by KeyboardInterrupt')


if __name__ == '__main__':
    run()
