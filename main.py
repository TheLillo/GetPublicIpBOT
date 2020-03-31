from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
import configparser
import subprocess
from pathlib import Path

config_file = Path("config.ini")
if config_file.is_file():
    with config_file.open() as f:
        config = configparser.ConfigParser()
        config.read_file(f)
        TOKEN = config.get('DEFAULT', 'Token')
        USERID = config.get('DEFAULT', 'UserId')

else:
    print("config.ini non trovato")
    exit(1)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

all_commands = {}
task = lambda f: all_commands.setdefault(f.__name__, f)


@task
def send_public_ip(update, context):
    if update.effective_chat.type == 'private':
        if str(update.effective_user.id) == USERID:
            try:
                my_public_ip = subprocess.run(["dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"], check=True,
                                 capture_output=True, encoding='utf-8').stdout
                update.message.reply_text("Il Tuo Ip : {}".format(str(my_public_ip)))
            except :
                update.message.reply_text("Something went wrong :)")
        else:
            update.message.reply_text("This bot is not for you ! :)")
    else:
        update.message.reply_text("I'm Sorry. This is Command is only for private chat :)")


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    send_public_ip_handler = CommandHandler('sendPublicIp', send_public_ip)
    dispatcher.add_handler(send_public_ip_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
