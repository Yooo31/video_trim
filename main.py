from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

from process.downloadVideo import VideoDownloader
from process.videoEditor import VideoEditor
from process.videoSender import VideoSender

from dotenv import load_dotenv
import os
import json

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def getInformations():
  with open("informations.json", "r") as file:
    data = json.load(file)
    timing = data["timing"]
    last_url = data["last_url"]
    last_date = data["last_date"]
    title = data["title"]
    author = data["author"]

  return f"Vidéo précédente : \n\n📅 Date : {last_date}\n🔗 URL : {last_url}\n🎬 Durée : {timing} secondes\n🤳 Crédits : {title} | {author}\n\n"

def start(update, context):
  keyboard = [
            [InlineKeyboardButton("⚙️ Paramétres ⚙️", callback_data="settings")],
            [InlineKeyboardButton("🎬 Commencer 🎬", callback_data="starting")],
            [InlineKeyboardButton("❓ Dernière Vidéo ❓", callback_data="last_video")]
  ]

  reply_markup = InlineKeyboardMarkup(keyboard)
  update.message.reply_text("Que voulez vous faire ?", reply_markup=reply_markup)

def startButton(update, context):
    query = update.callback_query

    if query.data == "settings":
      chat_id = query.message.chat_id
      currentTiming = VideoEditor.get_video_timing()

      context.bot.send_message(chat_id=chat_id, text="Quelle est la nouvelle durée de chaque vidéo ? Durée actuelle : " + str(currentTiming) + " secondes.")
      context.user_data["state"] = "WAITING_FOR_TIMING"

      return "WAITING_FOR_TIMING"

    elif query.data == "starting":
      chat_id = query.message.chat_id

      context.bot.send_message(chat_id=chat_id, text="Envoyer l'URL de la vidéo")
      context.user_data["state"] = "WAITING_FOR_URL"

      return "WAITING_FOR_URL"

    elif query.data == "last_video":
      message = getInformations()

      chat_id = query.message.chat_id
      context.bot.send_message(chat_id=chat_id, text=message)

def handle_text(update, context):
    state = context.user_data.get("state")

    if state == "WAITING_FOR_TIMING":
      timing = update.message.text
      chat_id = update.message.chat_id

      if VideoEditor.set_video_timing(timing):
        message = f"La durée de chaque vidéo a été paramétrée à {timing}"
      else:
        message = "La durée de chaque vidéo n'a pas été paramétrée correctement. Veuillez saisir un entier inférieur ou égal à 180."

      context.bot.send_message(chat_id=chat_id,  text= message)
      context.user_data["state"] = None
      start(update, context)

    elif state == "WAITING_FOR_URL":
      url = update.message.text
      chat_id = update.message.chat_id
      downloader = VideoDownloader(url)

      if downloader.validate_url():
        context.bot.send_message(chat_id=chat_id, text="Vidéo valide, téléchargement en cours...")

        try:
          downloader.download_video()
          context.bot.send_message(chat_id=chat_id, text="Vidéo téléchargée avec succès!")
        except Exception as e:
          context.bot.send_message(chat_id=chat_id, text="Une erreur est survenue lors du téléchargement de la vidéo.")

        try:
          VideoEditor.change_format()
        except Exception as e:
          context.bot.send_message(chat_id=chat_id, text="Une erreur est survenue lors du changement du format")

        try:
          VideoEditor.cut_video()
        except Exception as e:
          context.bot.send_message(chat_id=chat_id, text="Une erreur est survenue lors du découpage")

        try:
          VideoSender.send_videos(context.bot, chat_id)
        except Exception as e:
          context.bot.send_message(chat_id=chat_id, text="Une erreur est survenue lors de l'envoie des vidéos")

        try:
          title, author = downloader.get_title_and_author();
          context.bot.send_message(chat_id=chat_id, text="🤳 Crédits: " + title + " | " + author + "\nProvenance : YouTube 📺")
        except Exception as e:
          context.bot.send_message(chat_id=chat_id, text="Une erreur est survenue lors de la récupération des informations")

      else:
        context.bot.send_message(chat_id=chat_id, text="L'URL de la vidéo est invalide. Veuillez saisir une URL valide.")

      context.user_data["state"] = None

    else:
      update.message.reply_text("Veuillez choisir une option à partir des boutons ci-dessous.")
      start(update, context)

def main():
  updater = Updater(BOT_TOKEN, use_context=True)

  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CallbackQueryHandler(startButton))

  dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

  updater.start_polling()
  updater.idle()

print("Bot started")
main()
