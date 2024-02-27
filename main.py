from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import escape_markdown
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

import os
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


def start(update, context):
  keyboard = [
            [InlineKeyboardButton("⚙️ Paramétres ⚙️", callback_data="settings")],
            [InlineKeyboardButton("🎬 Commencer 🎬", callback_data="starting")]
  ]

  reply_markup = InlineKeyboardMarkup(keyboard)
  update.message.reply_text("Que voulez vous faire ?", reply_markup=reply_markup)

def startButton(update, context):
  query = update.callback_query

  chat_id = query.message.chat_id
  print(chat_id)

  if query.data == "settings" :
    print("Settings selected")

  elif query.data == "starting" :
    print("Starting selected")

def main():
  updater = Updater(BOT_TOKEN, use_context=True)

  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CallbackQueryHandler(startButton))

  # dp.add_handler(MessageHandler(Filters.text, handle_message))
  # dp.add_error_handler(error)

  updater.start_polling()
  updater.idle()

print("Bot started")
main()
