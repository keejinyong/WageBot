# Authors : JZ, KJ, BK
from uuid import uuid4

import re
import time
from random import *

from telegram.utils.helpers import escape_markdown

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, ReplyKeyboardMarkup, KeyboardButton, ChatMember
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, JobQueue
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

big_small_started = False
big_array = []
small_array = []


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Welcome to Wage Bot!')
    keyboard = [[(KeyboardButton('/big_small'))],[(KeyboardButton('/blackjack'))],[(KeyboardButton('/devil'))]]

    keyboardmarkup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id,
                     text="help your mom",
                     reply_markup=keyboardmarkup)

def stop_big_small(bot, job):
    global big_small_started
    big_small_started = False
    rand_num = randint(1,2)
    if rand_num==1:
        for i in big_array:
            bot.send_message(chat_id=i,
                     text="Small! You lose fucker!")
        for i in small_array:
            bot.send_message(chat_id=i,
                         text="Small! Good job asshole!")
    else:
        for i in big_array:
            bot.send_message(chat_id=i,
                     text="Big! Good job asshole!")
        for i in small_array:
            bot.send_message(chat_id=i,
                         text="Big! You lose fucker!")
    big_array[:] = []
    small_array[:] = []    

                     
def big_small(bot, update, job_queue):
    global big_small_started
    if not big_small_started:
        update.message.reply_text('Place your bets!')
        keyboard = [[(KeyboardButton('/big'))],[(KeyboardButton('/small'))]]
        keyboardmarkup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Pick one of the following:",
                         reply_markup=keyboardmarkup)
        big_small_started = True
        job_queue.run_once(stop_big_small, 5)
        

    

def big(bot, update):
    if big_small_started:
        big_array.append(update.message.from_user.id)
        update.message.reply_text('Big Registered')
        update.message.reply_text(big_array) 
    else:
        update.message.reply_text('Start a new game')
        

def small(bot, update):
    if big_small_started:
        small_array.append(update.message.from_user.id)
        update.message.reply_text('Small Registered')
        update.message.reply_text(small_array) 
    else:
        update.message.reply_text('Start a new game')

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help your mother la!')


def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    if not query:
     return
    results = list()
    results.append(
        InlineQueryResultArticle(
         id=query.upper(),
         title='Caps',
         input_message_content=InputTextMessageContent(query.upper())
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def unknown(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text="Fuck you. Type something coherent, you imbecile.")


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token='493877665:AAGn4U1SOBu04mcWO-6JRS6PCWZL-RhGhoo')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    uh = MessageHandler(Filters.command, unknown)
    inline_handler = InlineQueryHandler(inlinequery)

    
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("big_small", big_small,
                                  pass_job_queue=True))
    dp.add_handler(CommandHandler("big", big))
    dp.add_handler(CommandHandler("small", small))
    dp.add_handler(CommandHandler("stop_big_small", stop_big_small))
    dp.add_handler(uh)

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(inline_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
