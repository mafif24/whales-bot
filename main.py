import os
from pprint import pprint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.bot import Bot
from database_handle import SqliteHandle
from urllib.parse import urlparse
from whalealert.whalealert import WhaleAlert
import time
import sched
import threading
import messages

db_file = "./data.db"

sender_bot = Bot(token='1949271919:AAFC-zoz2l6aOddZnL9I2oSoyulVddzza8s')
Admin_Chat_Id = '552587607'
msg = {}
msg['App'] = "Music Downloader Bot"

db = SqliteHandle(db_file)

whale = WhaleAlert() 

api_key = 'oDeYXOCSUZR0sHm8666AHiZK4SKSgqA9'
transaction_count_limit = 10
min_value = 10000000
start_time = int(time.time() - 600)

scheduler = sched.scheduler(time.time, time.sleep)


def update_transaction():
    print("Doing stuff...")
    start_time = int(time.time() - 600)
    success, transactions, status = whale.get_transactions(
        start_time, api_key=api_key, limit=transaction_count_limit)
    data={}
    data['blockchain']= transactions[0]['blockchain']
    data['symbol'] =  transactions[0]['symbol']
    data['transaction_type'] = transactions[0]['transaction_type']
    data['from'] = 'unknown' if transactions[0]['from']['owner'] == '' else transactions[0]['from']['owner'] 
    data['to'] = 'unknown' if transactions[0]['to']['owner'] == '' else transactions[0]['to']['owner'] 
    data['amount'] = transactions[0]['amount_usd']
    data['trx_id'] = transactions[0]['id']
    SUDAH_DISI = messages._HEADER
    SUDAH_DISI += messages._TRANSACTION.format_map(data)
    SUDAH_DISI += messages._FOOTER 
    print(SUDAH_DISI)
    pprint(transactions[0])
    sender_bot.send_message('@whale_b0t', SUDAH_DISI)
    # do your stuff
    threading.Timer(60, update_transaction).start()


def start(bot, update):
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    chat_id = update.message.chat.id
    uname = user['first_name']
    text = """
    ini bot tele
    """
    update.message.reply_text(text)
    msg['user'] = uname
    msg['chat_id'] = chat_id
    msg['status'] = 'Send Help Message'

def register(bot, update):
    chat_id = update.message.chat.id
    update.message.reply_text(chat_id)
    sender_bot.send_message('@whale_b0t', "dari sender bot")

def from_whale_alert(bot, update):
    start_time = int(time.time() - 600) # UPDATE WAKTU
    success, transactions, status = whale.get_transactions(
        start_time, api_key=api_key, limit=transaction_count_limit)
    data={}
    data['blockchain'] = transactions[0]['blockchain']
    data['symbol'] =  transactions[0]['symbol']
    data['transaction_type'] = transactions[0]['transaction_type']
    data['from'] = 'unknown' if transactions[0]['from']['owner'] == '' else transactions[0]['from']['owner'] 
    data['to'] = 'unknown' if transactions[0]['to']['owner'] == '' else transactions[0]['to']['owner'] 
    data['amount'] = transactions[0]['amount_usd']
    data['trx_id'] = transactions[0]['id']
    SUDAH_DISI = messages._HEADER
    SUDAH_DISI += messages._TRANSACTION.format_map(data)
    SUDAH_DISI += messages._FOOTER
    print(SUDAH_DISI)
    pprint(transactions[0])
    update.message.reply_text(SUDAH_DISI)


def echo(bot, update):
    chat_id = update.message.chat.id
    message_user = update.message.text
    username = update.message.chat.username
    first_name = update.message.chat.first_name
    user_id = update.message.from_user.id
    user_data = (user_id, username, chat_id, first_name)
    update.message.reply_text("TEST")


def main():

    threading.Timer(60, update_transaction).start()
    updater = Updater(
        "1949271919:AAFC-zoz2l6aOddZnL9I2oSoyulVddzza8s", use_context=False)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("whale", from_whale_alert))
    dp.add_handler(CommandHandler("help", start))

    dp.add_handler(MessageHandler(Filters.regex('^(http|https)://'), echo))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
