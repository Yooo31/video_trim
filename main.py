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

    if query.data == "settings":
      chat_id = query.message.chat_id
      context.bot.send_message(chat_id=chat_id, text="Quelle est la nouvelle durée de chaque vidéo ?")
      context.user_data["state"] = "WAITING_FOR_TIMING"
      return "WAITING_FOR_TIMING"

    elif query.data == "starting":
      chat_id = query.message.chat_id
      context.bot.send_message(chat_id=chat_id, text="Envoyer l'URL de la vidéo")
      context.user_data["state"] = "WAITING_FOR_URL"
      return "WAITING_FOR_URL"

def handle_text(update, context):
    state = context.user_data.get("state")
    print(state)

    if state == "WAITING_FOR_TIMING":
      timing = update.message.text
      chat_id = update.message.chat_id
      context.bot.send_message(chat_id=chat_id, text=f"La durée de chaque vidéo a été paramétrée à {timing}")
      context.user_data["state"] = None

    elif state == "WAITING_FOR_URL":
      url = update.message.text
      chat_id = update.message.chat_id
      context.bot.send_message(chat_id=chat_id, text=f"La vidéo a été téléchargée à partir de l'URL suivante : {url}")
      context.user_data["state"] = None

    else:
      update.message.reply_text("Veuillez choisir une option à partir des boutons ci-dessus.")

def main():
  updater = Updater(BOT_TOKEN, use_context=True)

  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CallbackQueryHandler(startButton))

  dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

  # dp.add_handler(MessageHandler(Filters.text, handle_message))
  # dp.add_error_handler(error)

  updater.start_polling()
  updater.idle()

print("Bot started")
main()
